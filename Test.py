from datetime import datetime, timedelta
a = datetime.now()
b = a - timedelta(days=5)
print(b)