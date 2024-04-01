from datetime import datetime, timedelta

CREATE_TIME = (datetime.now() - timedelta(days=3)).isoformat(timespec='minutes')
CLOSE_TIME = (datetime.now() - timedelta(days=1)).isoformat(timespec='minutes')
