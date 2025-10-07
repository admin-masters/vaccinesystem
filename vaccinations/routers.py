# vaccinations/routers.py
MASTERS_MODELS = {
    "ScheduleVersion","Vaccine","VaccineDose",
    "Partner","FieldRepresentative","Clinic","Doctor",
    "VaccineEducationPatient","VaccineEducationDoctor",
    "UiString","UiStringTranslation","OauthState",
}

PATIENTS_MODELS = {"Parent","Child","ChildDose","ChildShareLink"}

class MasterPatientRouter:
    def db_for_read(self, model, **hints):
        n = model.__name__
        if n in MASTERS_MODELS: return "masters"
        if n in PATIENTS_MODELS: return "patients"
        return None

    db_for_write = db_for_read

    def allow_relation(self, obj1, obj2, **hints):
        # allow all ORM relations in Python; DB will not enforce cross‑DB FKs
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name is None: return None
        name = model_name[0].upper() + model_name[1:]
        if name in MASTERS_MODELS:  return db == "masters"
        if name in PATIENTS_MODELS: return db == "patients"
        return None
