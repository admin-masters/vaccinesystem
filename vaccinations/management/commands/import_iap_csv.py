from __future__ import annotations
import csv
import re
from pathlib import Path
from typing import Optional

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from vaccinations.models import ScheduleVersion, Vaccine, VaccineDose


TIME_PATTERN = re.compile(
	r"(?P<num1>\d+(?:\.\d+)?)\s*(?P<unit1>day|days|week|weeks|month|months|year|years)?"
	r"(?:\s*[-–]\s*(?P<num2>\d+(?:\.\d+)?)\s*(?P<unit2>day|days|week|weeks|month|months|year|years)?)?",
	re.IGNORECASE,
)


def _normalize(s: str) -> str:
	return re.sub(r"\s+", " ", s or "").strip().lower()


def _sex_from_text(s: str | None) -> Optional[str]:
	if not s:
		return None
	s = s.strip().lower()
	if s.startswith("f") or "girl" in s:
		return "F"
	if s.startswith("m") or "boy" in s:
		return "M"
	return None


def _to_days(value: float, unit: str) -> int:
	unit = unit.lower()
	if unit.startswith("day"):
		return int(round(float(value)))
	if unit.startswith("week"):
		return int(round(float(value) * 7))
	if unit.startswith("month"):
		return int(round(float(value) * 30))
	if unit.startswith("year"):
		return int(round(float(value) * 365))
	raise ValueError(f"Unknown unit: {unit}")


def parse_time_period(period: str) -> tuple[int, Optional[int]]:
	"""
	Returns (min_offset_days, max_offset_days or None)
	Rules:
	  - 'At birth' => 0
	  - '16 - 18 months' => (16*30, 18*30)
	  - single '6 weeks' => (6*7, None)
	"""
	if not period:
		raise ValueError("Time period empty")
	p = period.strip().lower()
	if p in {"at birth", "birth", "0 days", "0 day", "0"}:
		return (0, None)
	m = TIME_PATTERN.search(period)
	if not m:
		raise ValueError(f"Unrecognized time period: {period}")
	num1, unit1 = m.group("num1"), m.group("unit1") or "days"
	min_days = _to_days(float(num1), unit1)
	if m.group("num2") and m.group("unit2"):
		max_days = _to_days(float(m.group("num2")), m.group("unit2"))
	else:
		max_days = None
	return (min_days, max_days)


def infer_vaccine_group(vaccines_label: str) -> str:
	"""
	Heuristic to group rows into vaccines:
	  - 'IPV booster' -> 'IPV'
	  - 'DTwP 1' -> 'DTwP'
	  - 'MMR-2' -> 'MMR'
	  - fallback: full text up to '('
	"""
	s = vaccines_label.strip()
	s_no_paren = s.split("(")[0].strip()
	# Remove trailing dose numbers or 'booster'
	s_no_booster = re.sub(r"\bbooster\b", "", s_no_paren, flags=re.IGNORECASE).strip()
	s_no_num = re.sub(r"[-\s]*\d+$", "", s_no_booster).strip()
	return s_no_num or s


class Command(BaseCommand):
	help = "Import IAP schedule CSV into ScheduleVersion, Vaccine, VaccineDose"

	def add_arguments(self, parser):
		parser.add_argument("csv_path", type=str)
		parser.add_argument("--schedule-code", required=True)
		parser.add_argument("--schedule-name", required=True)
		parser.add_argument("--set-current", action="store_true", default=False)
		parser.add_argument("--replace", action="store_true", default=False)

	def handle(self, *args, **opts):
		csv_path = Path(opts["csv_path"])
		if not csv_path.exists():
			raise CommandError(f"CSV not found: {csv_path}")

		schedule_code = opts["schedule_code"]
		schedule_name = opts["schedule_name"]

		with transaction.atomic():
			sv, created = ScheduleVersion.objects.get_or_create(
				code=schedule_code,
				defaults={"name": schedule_name, "is_current": opts["set_current"]},
			)
			if not created:
				sv.name = schedule_name
				if opts["set_current"]:
					sv.is_current = True
				sv.save(update_fields=["name", "is_current"])

			if opts["replace"]:
				VaccineDose.objects.filter(schedule_version=sv).delete()
				Vaccine.objects.filter(schedule_version=sv).delete()

			# Load rows
			with csv_path.open(newline="", encoding="utf-8-sig") as f:
				reader = csv.DictReader(f)
				headers = {h.lower().strip(): h for h in reader.fieldnames or []}

				def col(name: str) -> str:
					for k in headers:
						if k == name.lower():
							return headers[k]
					# allow some flexible names
					aliases = {
						"time period": ["time", "period", "age", "time_period"],
						"vaccines": ["vaccine", "dose", "label", "vaccines"],
						"booster yes/no": ["booster", "booster yes/no"],
						"previous vaccine": ["previous", "previous vaccine", "previous dose"],
						"eligible sex": ["sex", "eligible sex"],
					}
					for key, al in aliases.items():
						if name.lower() == key:
							for a in al:
								if a in headers:
									return headers[a]
					raise CommandError(f"Column '{name}' not found in CSV headers: {list(headers)}")

				c_time = col("time period")
				c_vacc = col("vaccines")
				c_boost = col("booster yes/no")
				c_prev = headers.get("previous vaccine") or headers.get("previous") or col("previous vaccine")
				c_sex = headers.get("eligible sex")

				# First pass: create vaccines & doses (previous_dose deferred)
				vaccine_map: dict[str, Vaccine] = {}
				dose_by_label: dict[str, VaccineDose] = {}
				sequence_index: dict[int, int] = {}  # vaccine_id -> seq

				for row in reader:
					vacc_label = (row.get(c_vacc) or "").strip()
					time_str = (row.get(c_time) or "").strip()
					booster_str = (row.get(c_boost) or "").strip()
					sex_str = (row.get(c_sex) or "").strip() if c_sex else ""

					if not vacc_label or not time_str:
						continue

					min_days, max_days = parse_time_period(time_str)
					is_booster = booster_str.lower().startswith("y")

					group_name = infer_vaccine_group(vacc_label)
					group_code = re.sub(r"[^a-z0-9]+", "-", group_name.lower()).strip("-")[:50]

					vac = vaccine_map.get(group_code)
					if not vac:
						vac, _ = Vaccine.objects.get_or_create(
							schedule_version=sv,
							code=group_code,
							defaults={"name": group_name},
						)
						vaccine_map[group_code] = vac
						sequence_index[vac.id] = 0

					sequence_index[vac.id] += 1
					seq = sequence_index[vac.id]

					vd = VaccineDose.objects.create(
						schedule_version=sv,
						vaccine=vac,
						sequence_index=seq,
						dose_label=vacc_label,  # use the row label as display
						eligible_sex=_sex_from_text(sex_str),
						min_offset_days=min_days,
						max_offset_days=max_days,
						is_booster=is_booster,
						previous_dose=None,  # link in second pass
					)
					dose_by_label[_normalize(vacc_label)] = vd

				# Second pass: link 'previous_dose'
				# Re-open CSV because DictReader is exhausted
			f = csv_path.open(newline="", encoding="utf-8-sig")
			try:
				reader2 = csv.DictReader(f)
				for row in reader2:
					vacc_label = (row.get(c_vacc) or "").strip()
					prev_label = (row.get(c_prev) or "").strip()
					if not vacc_label or not prev_label:
						continue
					vd = dose_by_label.get(_normalize(vacc_label))
					prev_vd = dose_by_label.get(_normalize(prev_label))
					if vd and prev_vd:
						VaccineDose.objects.filter(pk=vd.id).update(previous_dose=prev_vd)
			finally:
				f.close()

		self.stdout.write(self.style.SUCCESS(f"Imported schedule '{sv.code}' successfully."))


