def add(text):
    f = open("log.txt", "a")
    f.write(text+'\n')
    f.close()

def clear():
    open('log.txt', 'w').close()

def read():
    print(open('log.txt', 'r').read())