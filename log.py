def add(text):
    f = open("log.txt", "a")
    f.write(text)
    f.close()

def clear():
    open('log.txt', 'w').close()

def read():
    open('log.txt', 'r').read()