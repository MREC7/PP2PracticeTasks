#*args and **kwargs allow functions to accept a unknown number of arguments.
def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")

'''If you do not know how many keyword arguments will be passed into your function, add two asterisks ** before the parameter name.
This way, the function will receive a dictionary of arguments and can access the items accordingly:
'''
def my_function1(**kid):
  print("His last name is " + kid["lname"])

my_function1(fname = "Tobias", lname = "Refsnes") 