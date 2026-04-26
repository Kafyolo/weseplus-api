from sqlalchemy.orm import Session
from app.models.audit import AuditLog
import functools

def log_audit(action_name: str):
    """
    Decorator for simple audit logging. 
    Requires the decorated function to receive 'db: Session' and 'current_user' or 'user_id'.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Extract common parameters from kwargs
            db = kwargs.get('db')
            user = kwargs.get('current_user')
            user_id = user.id if user else kwargs.get('user_id')
            
            if db:
                audit_entry = AuditLog(
                    user_id=user_id,
                    action=action_name,
                    metadata_json={"function": func.__name__, "args": str(args), "kwargs": str(kwargs)}
                )
                db.add(audit_entry)
                db.commit()
            
            return result
        return wrapper
    return decorator

async def manual_audit_log(db: Session, action: str, user_id=None, metadata=None):
    audit_entry = AuditLog(
        user_id=user_id,
        action=action,
        metadata_json=metadata
    )
    db.add(audit_entry)
    db.commit()
