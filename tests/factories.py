import uuid

def unique_username(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def unique_email(prefix="emp"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"
