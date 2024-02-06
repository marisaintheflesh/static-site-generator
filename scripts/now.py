from datetime import datetime, timezone

now = int(datetime.now(timezone.utc).timestamp())
print(now)

