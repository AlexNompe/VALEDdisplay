mylist = eval(input())
print([i for i in range(1, len(mylist)) if i not in mylist])