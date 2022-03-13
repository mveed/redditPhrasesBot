listFile = open("list.txt", "r")
substrings = []
for lines in listFile:
    str = lines[:-1]
    substrings.append(str)
#print(substrings)
string0 = "asdf"
string1 = "asd the asd"
string2 = "asdtheasd"
string3 = "the is"
string4 = "asd is asd"

print((len(string1.split())))
for s in substrings:
    if s in string0 and len(string0.split()) < 10:
        print("found " + string0)
    if s in string1:
        print("found " + string1)
    if s in string4:
        print("found " + string4)