def add(text):
    f = open("log.txt", "a")
    f.write(text)
    f.close()

def clear():
    open('log.txt', 'w').close()

f = open("log.txt", "r")
print(f.read())