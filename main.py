file = open("document.txt")
print(file.read())
file.close()
# r : lecture
# a : ajout
# w : écriture
# x : création 



with open("file.txt", "w", encoding="utf-8") as document:
    document.write("hello world!")

with open("file.txt", "a", encoding="utf-8") as document:
    document.write("\nhello world again!")