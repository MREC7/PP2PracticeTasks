from datetime import datetime, timedelta
a = datetime.now()
print(a - timedelta(days = 5))
print(f"Yesterday: {a - timedelta(days = 1)}\nToday: {a}\nTomorrow: {a + timedelta(days = 1)}")
print(a.replace(microsecond = 0))
b = datetime(2000, 1, 1, 0, 0, 0 ,0)
c = a - b
print(c.total_seconds())