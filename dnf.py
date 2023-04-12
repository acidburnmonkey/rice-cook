import os

def dnf():

    programs = []

    with open('data.txt', 'r+') as f:
        for line in f:
            programs.append(line.strip())

    print(programs)


print(os.getcwd()) 
