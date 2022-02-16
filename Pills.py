
""" Add/Delete/Get """
def addPills(array):
    fin = open('Pills.txt', 'r')
    for line in fin:
        if (array[0] in line):
            return "уже записанно"
            break
    fin.close()
    fin = open('Pills.txt', 'a')
    for i in range(len(array)):
        print(array[i])
        fin.write(str(array[i]))
        fin.write(", ")
    fin.write('\n')
    fin.close()
    return "Сделанно"

# Delete realized in 2 functions
def deletePill(name):
    fin = open('Pills.txt', 'r')
    i = 1
    for line in fin:
        if(name in line):
            readAndWrite(fin, line)
            return True
            break
        i+=1
    return False


def readAndWrite(fin, lineToDel):
    listOfLines = []
    for line in fin:
        if(line != lineToDel):
            listOfLines.append(line)
    fin.close()
    fin = open("Pills.txt", "w")
    for i in range(len(listOfLines)):
        fin.write(listOfLines[i])
    fin.close()
#Realized in 2 functions



def getThePill(name):
    fin = open('Pills.txt', 'r')
    for line in fin:
        if (name in line):
            return line
            break
    fin.close()
    return "This pills are not listed"

"""End of the Add/Delete/Get section"""


"""Remind section"""
def remind():
    fin = open('Pills.txt', 'r')
    whatToRememberAbout = "Сегодня надо принять "
    for line in fin:
        l = line
        l = l.replace('none', '')
        l = l.replace('\n', '')
        pill = [i for i in l.split(",")]
        whatToRememberAbout = whatToRememberAbout+str(pill[0])+str(pill[1])+" раза "+str(pill[2])+". "
        whatToRememberAbout = whatToRememberAbout.replace("  ", " ")
        whatToRememberAbout = whatToRememberAbout.replace(" .", ".")
    fin.close()
    return whatToRememberAbout

#To say before the eating
def iAmEating():
    fin = open('Pills.txt', 'r')
    rememberAbout = "Хочу напомнить что вам нужно принять "
    for line in fin:
        if("after food" in line or "before food" in line):
            rememberAbout = rememberAbout + line.replace("\n", " ").replace("before food", "перед едой").replace("after food","после еды") + "также "
    rememberAbout += "незабудь запить)"
    if(rememberAbout == "Хочу напомнить что вам нужно принять незабудь запить)"):
        rememberAbout = "Приятного аппетита, никакие таблетки вам пить не нужно."
    fin.close()
    return rememberAbout

"""End of the remind section"""







