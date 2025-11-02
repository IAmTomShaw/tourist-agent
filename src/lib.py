import datetime

def _to_rfc3339(val, default_dt):
  if not val:
    return default_dt.isoformat() + "Z"

  if isinstance(val, datetime.datetime):
    if val.tzinfo is None:
      return val.isoformat() + "Z"
    return val.astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

  if isinstance(val, datetime.date):
    dt = datetime.datetime(val.year, val.month, val.day)
    return dt.isoformat() + "Z"

  if isinstance(val, str):
    return datetime.datetime.fromisoformat(val.replace("Z", "+00:00")).astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

  raise TypeError(f"Unsupported date value: {type(val)}")
