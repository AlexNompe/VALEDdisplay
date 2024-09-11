f = open(r"C:\Users\AlexN\AppData\Local\Dealt_with\en_us.txt", 'r')
lines = f.readlines()
mystr = "\\n".join([line.strip() for line in lines])
print('"'+mystr+'")')