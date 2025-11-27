from app.db.models.audit_log import AuditLog

# Helper function to automate feilds which can be auto-fetched!
def create_audit_log(db, actor, action, object_type, object_id, payload):
    audit = AuditLog(
        actor=actor,
        action=action,
        object_type=object_type,
        object_id=object_id,
        payload=payload,
    )
    db.add(audit)
    return audit