SHARED_MODELS = {"ScheduleVersion", "Vaccine", "VaccineDose"}

MASTERS_MODELS = {
    "Partner", "FieldRepresentative", "Clinic", "Doctor", "DoctorSessionToken",
    "VaccineEducationPatient", "VaccineEducationDoctor",
    "UiString", "UiStringTranslation", "OAuthState", "OauthState",
}

PATIENTS_MODELS = {"Parent", "Child", "ChildDose", "ChildShareLink"}

SHARED_MODEL_KEYS = {name.replace("_", "").lower() for name in SHARED_MODELS}
MASTERS_MODEL_KEYS = {name.replace("_", "").lower() for name in MASTERS_MODELS}
PATIENTS_MODEL_KEYS = {name.replace("_", "").lower() for name in PATIENTS_MODELS}


def _model_key(model_name=None, hints=None):
    hints = hints or {}
    model = hints.get("model")
    if model is not None:
        return model._meta.object_name.replace("_", "").lower()
    if not model_name:
        return None
    return str(model_name).replace("_", "").lower()


class MasterPatientRouter:
    def db_for_read(self, model, **hints):
        n = model.__name__
        if n in SHARED_MODELS or n in MASTERS_MODELS:
            return "masters"
        if n in PATIENTS_MODELS:
            return "patients"
        return None

    db_for_write = db_for_read

    def allow_relation(self, obj1, obj2, **hints):
        # allow all ORM relations in Python; DB will not enforce cross-DB FKs
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label != "vaccinations":
            return None

        model_key = _model_key(model_name=model_name, hints=hints)
        if not model_key:
            return None

        if model_key in SHARED_MODEL_KEYS:
            return db in {"default", "masters"}
        if model_key in MASTERS_MODEL_KEYS:
            return db == "masters"
        if model_key in PATIENTS_MODEL_KEYS:
            return db == "patients"
        return db == "default"
