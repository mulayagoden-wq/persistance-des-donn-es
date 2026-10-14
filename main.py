file = open("document.txt")
print(file.read())
file.close()
# r : lecture
# a : ajout
# w : écriture
# x : création 

with open("file.txt", "x") as document:
    document.write("bana monde entier!")

with open("file.txt", "w") as document:
    document.write("hello world!")

with open("file.txt", "a") as document:
    document.write("\nhello world again!")