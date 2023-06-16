a = 1
b = 2
print(globals())
exec("c = a + b", globals())
print(c)
print(globals())
