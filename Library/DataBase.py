field = {"Game":0, "Team":1, "Captain":2, "Year":3, "Age":4, "Player1":5, "Player2":6}
unfield = {0:"Game", 1:"Team", 2:"Captain", 3:"Year", 4:"Age", 5:"Player1", 6:"Player2"}


def readData():
    """
    Author: Иртикеев М.Н.
    Читает базу
    """
    import pickle as pi
    fin = open('../Data/data.pi', 'rb')
    data = pi.load(fin)
    return data


def addRecord(data,d):
    """
    Author: Иртикеев М.Н.
    Добавляет запись
    """
    data.append(d)
    writeData(data)


def posMore( vvod , vivod):
    """
    Author: Сафронов А.М.
    Ищет по множеству параметров
    """
    flag = 0
    i = 0
    games = readData()
    print(vvod)
    for a in games:
        isInVivod = 0
        for c in vivod:
            if (c == a):  
                isInVivod = 1
        if (not(isInVivod)):
            while (i < len(vvod)):
                for b in a:
                    if (flag != i+1):
                        print(b,vvod[i],b==vvod[i])
                        if (b == vvod[i]):
                            flag+=1
                i+=1
                if (flag == len(vvod)):
                    vivod.append(a)
                    print(a)
                    flag = 0
            i = 0
            flag = 0


def search(b,d):
    """
    Author: Иртикеев М.Н.
    Поиск в промежутке
    """
    baseOut = []
    base = readData()
    
    a = 1
    if (a > 0):
        if (len(baseOut) == 0):
            for e in base:
                if (int(e[4]) > a):
                    baseOut.append(e)
        else:
            base = []
            for e in baseOut:
                if (int(e[4]) > int(a)):
                    base.append(e)
        baseOut = base
        
    if (len(b) > 0):
        if (len(baseOut) == 0):
            for e in base:
                if (int(e[4]) < int(b)):
                    baseOut.append(e)
        else:
            base = []
            for e in baseOut:
                if (int(e[4]) < int(b)):
                    base.append(e)
        baseOut = base
        
    c = 1

    if (c > 0):
        if (len(baseOut) == 0):
            for e in base:
                if (int(e[3]) > c):
                    baseOut.append(e)
        else:
            base = []
            for e in baseOut:
                if (int(e[3]) > c):
                    base.append(e)
        baseOut = base

    if (len(d) > 0):
        if ( len(baseOut) == 0):
            for e in base:
                if (int(e[3]) < int(d)):
                    baseOut.append(e)
        else:
            base = []
            for e in baseOut:
                if (int(e[3]) < int(d)):
                    base.append(e)
        baseOut = base
    return baseOut

def outBase( data ):
    """
    Author: Михайлов к.В.
    Выводит базу
    """
    fin = open('../Output/base.txt', 'w')
    for a in data:
        for b in a:
            print(b, file=fin)
        print(file=fin)
    fin.close()
	
def writeData( data ):
    """
    Author: Михайлов к.В.
    Печатает дату
    """
    import pickle as pi
    fin = open('../Data/data.pi', 'wb')
    pi.dump(data, fin)

	
def sort( vvod , order ):
    """
    Author: Сафронов А.М.
    Сортирует
    """
    output = []
    priority = []
    nombers = {}
    games = readData()
    if (vvod in field):
        for a in games:
            if (vvod == "Цена"):
                priority.append(int(a[field[vvod]]))
            else:
                priority.append(a[field[vvod]])
        priority = sorted(priority)
        i = 0
        for a in games:
            i = 0
            while ( a[field[vvod]] != str(priority[i]) or i in nombers):
                i+=1
            nombers[i]=a
        if (order == 1):
            j = 0
            while (j < len(nombers)):
                output.append(nombers[j])
                j+=1      
        else:
            if (order == 0):
                j = len(nombers) - 1
                while (j > -1):
                    output.append(nombers[j])
                    j-=1  
            else:
                print("Incorrect input")
    else:
        print("Incorrect input")
    return output
	
def pos( vvod ):
    """
    Author: Михайлов к.В.
    Поиск по параметрам
    """
    i = 0  
    j = 0
    lis = [] 
    vivod = []
    while (j < len(vvod)):
        if (vvod[j] == '|'):
            lis.append(vvod[i:j])
            posMore(lis,vivod)
            lis = []     
            i = j+1
        if  (vvod[j] == '&'):
            lis.append(vvod[i:j])
            i = j+1
        j+= 1
    lis.append(vvod[i:j]) 
    posMore(lis,vivod)
    for a in vivod:
        for b in a:
            print(b)   
        print()
