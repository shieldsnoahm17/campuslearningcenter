test = "hello there;this is a test;yippy;"
print(test[: test.index(';') ])
test = test[ test.index(';') + 1:]
print(test[: test.index(';') ])
test = test[ test.index(';') + 1:]
print(test[: test.index(';') ])
test = test[ test.index(';') + 1:]
if(len(test) == 0):
    print("we did it!")