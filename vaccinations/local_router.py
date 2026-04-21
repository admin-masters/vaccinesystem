class LocalSqliteRouter:
    """
    Local-only router for the single-file SQLite demo setup.

    The app still uses explicit `.using("masters")` / `.using("patients")`
    calls in many places. All aliases point to the same SQLite file locally,
    so we allow relations across aliases while keeping migrations on the
    default connection.
    """

    def db_for_read(self, model, **hints):
        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"
