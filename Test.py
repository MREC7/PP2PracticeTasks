import datetime
a = datetime.datetime.now

a.days += a.days - 5
print(a)