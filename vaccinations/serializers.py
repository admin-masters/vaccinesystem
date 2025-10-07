from __future__ import annotations
from rest_framework import serializers
from .models import Child, ChildDose
from .utils import status_code_for, today

class ChildDoseSerializer(serializers.ModelSerializer):
    vaccine_name = serializers.CharField(source="dose.vaccine.name", read_only=True)
    dose_label = serializers.CharField(source="dose.dose_label", read_only=True)
    status_code = serializers.SerializerMethodField()

    class Meta:
        model = ChildDose
        fields = ["id","vaccine_name","dose_label","given_date","due_date","due_until_date","status_code"]

    def get_status_code(self, obj: ChildDose) -> str:
        return status_code_for(obj.due_date, obj.due_until_date, obj.given_date)
class ChildCardSerializer(serializers.ModelSerializer):
    doses = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = ["id", "child_name", "date_of_birth", "gender", "state", "doses"]

    def get_doses(self, child: Child):
        t = today()
        qs = (child.doses
              .select_related("dose__vaccine")
              .filter(due_date__isnull=False, due_date__lte=t)
              .order_by("dose__vaccine__name","dose__sequence_index"))
        return ChildDoseSerializer(qs, many=True).data
