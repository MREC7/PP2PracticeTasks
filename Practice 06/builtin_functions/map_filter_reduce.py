from functools import reduce
nums = [1,2,3,4,5]
print(list(map(lambda x: x*2, nums)))
print(list(filter(lambda x: x%2==0, nums)))
print(reduce(lambda a,b: a+b, nums))