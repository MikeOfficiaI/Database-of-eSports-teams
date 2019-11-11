def display():
    """
    Author: Иртикеев М.Н.
    Основное Меню
    """
    # first part
    import tkinter as tk
    class scrollFrame(tk.Frame):
        def __init__(self, parent, *args, **kw):
            """
            Author: Михайлов к.В.
            Описание класса
            """
            tk.Frame.__init__(self, parent, *args, **kw)
            vgScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
            vgScroll.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
            canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vgScroll.set, bg="grey")
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
            vgScroll.config(command=canvas.yview)
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)
            self.interior = interior = tk.Frame(canvas)
            interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)
            def _configure(event):
                """
                Author: Сафронов А.М.
                Работа со скролом: настройка прокрутки
                """
                size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
                canvas.config(scrollregion="0 0 %s %s" % size)
                if interior.winfo_reqwidth() != canvas.winfo_width():
                    canvas.config(width=interior.winfo_reqwidth())

            interior.bind('<Configure>', _configure)

            def _configure(event):
                """
                Author: Иртикеев М.Н.
                Работа со скролом: настройка прокрутки в поле
                """
                if interior.winfo_reqwidth() != canvas.winfo_width():
                    canvas.itemconfigure(interior_id, width=canvas.winfo_width())
            canvas.bind('<Configure>', _configure)

    class MainWindow:
        def __init__(self, base):
            """
            Author: Михайлов К.В.
            Описание класса
            """
            self.base = base  # main.readData()
            self.nn = []
            self.im = tk.Label(root)
            self.flagSort = 0
            self.currSort = ""
            self.im.place(x=0, y=0, relwidth=1, relheight=1)
            self.frame_all = tk.Frame(self.im)
            self.scrollF = scrollFrame(self.frame_all)
            self.frameSorting = tk.Frame(self.frame_all)
            self.frameAddition = tk.Frame(self.frame_all)
            self.frameSearching = tk.Frame(self.frame_all)
            self.frameExit = tk.Frame(self.frame_all)
            self.sequence = [0, 2, 1, 3, 5, 6, 4]
            self.width = [12, 8, 9, 9, 2, 16, 16]

            class skip:
                def __init__(self, name):
                    """
                    Author: Сафронов А.М.
                    Работа с кнопками: прокрутка
                    """
                    self.Name = name
                    self.first = -1
                    self.j = 9
                    self.focus = self.Name[self.first:self.j]
                    self.flag = 0
                    self.flagButScroll = 0

                def cancelSkip(self):
                    """
                    Author: Иртикеев М.Н.
                    Работа с кнопками: отмена
                    """
                    self.flagButScroll = 1

                def scroll(self, but):
                    """
                    Author: Михайлов К.В.
                    Работа с кнопками: прокрутка
                    """
                    self.flagButScroll = 0
                    self.first = -1
                    self.j = 9

                    def change():
                        if (self.j < len(self.Name) or self.first == -1):
                            self.first = self.first + 1
                            self.j = self.j + 1
                            self.focus = self.Name[self.first:self.j]
                    change()
                    but["text"] = self.focus

                    def flagPlus():
                        """
                        Author: Сафронов А.М.
                        Буфферная функция
                        """
                        self.flag = self.flag + 1

                    self.flag = self.j
                    while (self.flag < len(self.Name)):
                        but["text"] = self.focus
                        flagPlus()
                        if (self.flagButScroll != 0):
                            break
                        root.after(300, change())
                        but["text"] = self.focus
                        but.update()
                    self.flag = 0
                    root.after(1000)
                    self.focus = self.Name[0:10]
                    but["text"] = self.focus
                    but.update()

                def getName(self):
                    """
                    Author: Иртикеев М.Н.
                    Буфферная функция
                    """
                    return self.Name

                def setName(self, name):
                    """
                    Author: Михайлов К.В.
                    Буфферная функция
                    """
                    self.Name = name

            def change(i, j):
                """
                Author: Сафронов А.М.
                Работа в БД
                """
                self.base[i][self.sequence[j]] = self.entry[j][i].get()
                self.entry[j][i].delete(0, tk.END)
                self.entry[j][i].grid_forget()
                DataBase.writeData(self.base)
                self.nn[j][i].grid(row=i, column=j + 1)
            self.exit = tk.Button(self.frameExit, text="Exit", command=root.destroy, bg="white", fg="black", width=13, height=4)
            self.pSkip = []
            self.pos = []
            self.entry = []
            self.spacePos = tk.Button(self.frameSorting, width=10, relief="flat", state="disabled")
            for j in range(7):
                self.pos.append(tk.Button(self.frameSorting, width=self.width[self.sequence[j]], text=DataBase.unfield[self.sequence[j]]))
                toP = []
                pToSkip = []
                toEntr = []
                i = 0
                while (i < len(self.base)):
                    toEntr.append(
                        tk.Entry(self.scrollF.interior, width=self.width[self.sequence[j]], bg="white", fg="black"))
                    pToSkip.append(skip(self.base[i][self.sequence[j]]))
                    toP.append(tk.Button(self.scrollF.interior, width=self.width[self.sequence[j]]))
                    i = i + 1
                self.entry.append(toEntr)
                self.pSkip.append(pToSkip)
                self.nn.append(toP)
                i = 0
                while (i < len(self.base)):
                    self.entry[j][i - 1].bind("<Return>", lambda event, i=i, j=j: change(i - 1, j))
                    self.nn[j][i - 1].bind("<Enter>", lambda event, i=i, j=j: self.pSkip[j][i - 1].scroll(self.nn[j][i - 1]))
                    self.nn[j][i - 1].bind("<Leave>", lambda event, i=i, j=j: self.pSkip[j][i - 1].cancelSkip())
                    self.nn[j][i - 1].bind("<Button-1>", lambda event, i=i, j=j: self.butChange(i - 1, j))
                    i = i + 1
            self.addSpace = tk.Label(self.frameAddition, width=12)
            self.add = tk.Button(self.frameAddition, text="Add", bg="white", fg="black")
            self.addNameGame = tk.Entry(self.frameAddition, width=self.width[self.sequence[0]])
            self.addTeam = tk.Entry(self.frameAddition, width=self.width[self.sequence[1]])
            self.addCap = tk.Entry(self.frameAddition, width=self.width[self.sequence[2]])
            self.addYear = tk.Entry(self.frameAddition, width=self.width[self.sequence[3]])
            self.addPlayer1 = tk.Entry(self.frameAddition, width=self.width[self.sequence[4]])
            self.addPlayer2 = tk.Entry(self.frameAddition, width=self.width[self.sequence[5]])
            self.addAge = tk.Entry(self.frameAddition, width=self.width[self.sequence[6]] * 2)
            self.init_widget()

        def init_widget(self):
            """
            Author: Иртикеев М.Н.
            Объекты в классе главного меню
            """
            self.spacePos.grid(row=0, column=0)
            for i in range(7):
                self.pos[i].bind('<ButtonRelease-1>',
                                 lambda event, i=i: self.sortDisp(event, DataBase.unfield[self.sequence[i]]))
                self.pos[i].grid(row=0, column=i + 1)
            self.exit.grid()
            self.frame_all.place(x=10, y=5, width=1291, height=1500)
            self.exit.bind('<ButtonRelease-1>')
            self.frameSorting.grid(row=0, column=0)
            self.scrollF.grid(row=1, column=0)
            self.frameAddition.grid(row=4, column=0)
            self.frameSearching.grid(row=6, column=0)
            self.frameExit.grid(row=5, column=1)

            def outputBase():
                """
                Author: Михайлов К.В.
                Запись
                """
                self.outB = tk.Button(self.frameSearching, text="Load to file", bg="white", fg="black", width=13,
                                      height=4)
                self.outB.bind("<Button-1>", lambda event: DataBase.outBase(self.base))
                self.outB.grid(row=1, column=10)

            outputBase()

            def searchBut():
                """
                Author: Сафронов А.М.
                Поиск
                """
                self.sea = tk.Button(self.frameSearching, text="Search", bg="white", fg="black", width=13, height=4)
                self.sea.bind("<Button-1>", lambda event: self.search())
                self.sea.grid(row=1, column=1)

            def init():
                """
                Author: Иртикеев М.Н.
                Работа с кнопками: возвращение в гл. меню
                """
                self.sea = tk.Button(self.frameSearching, text="Return", bg="white", fg="black")
                self.sea.bind("<Button-1>", lambda event: self.__init__(DataBase.readData()))
                self.sea.grid(row=1, column=1)

            if (self.base != DataBase.readData()):
                init()
            else:
                searchBut()
            self.add.bind('<ButtonRelease-1>', lambda event: self.buttAdd(event))
            self.addSpace.grid(row=0, column=0)
            self.addNameGame.grid(row=0, column=1)
            self.addTeam.grid(row=0, column=2)
            self.addCap.grid(row=0, column=3)
            self.addYear.grid(row=0, column=4)
            self.addPlayer1.grid(row=0, column=5)
            self.addPlayer2.grid(row=0, column=6)
            self.addAge.grid(row=0, column=7)
            self.add.grid(row=0, column=8)
            self.buttSort()

        def buttSort(self):
            self.deleting = []

            def deleteBase(i):
                """
                Author: Михайлов К.В.
                Удаление информации
                """
                del self.base[i]
                DataBase.writeData(self.base)
                self.__init__(self.base)

            for j in range(7):
                i = 0
                while (i < len(self.base)):
                    if (j == 0):
                        self.deleting.append(tk.Button(self.scrollF.interior, text="Delete", width=self.width[0]))
                        self.deleting[-1].bind('<Button-1>', lambda event, i=i: deleteBase(i))
                        self.deleting[-1].grid(row=i, column=0)
                    self.pSkip[j][i].setName(self.base[i][self.sequence[j]])
                    self.nn[j][i]["text"] = self.pSkip[j][i].getName()[0:10]
                    self.nn[self.sequence[j]][i].grid(row=i, column=self.sequence[j] + 1)
                    i = i + 1
        def butChange(self, i, j):
            self.nn[j][i].grid_forget()
            self.entry[j][i].grid(row=i, column=j + 1)

        def buttAdd(self, event):
            """
            Author: Сафронов А.М.
            Добавление информации
            """
            a = []
            # appends
            a.append(self.addNameGame.get())
            a.append(self.addCap.get())
            a.append(self.addTeam.get())
            a.append(self.addYear.get())
            a.append(self.addAge.get())
            a.append(self.addPlayer1.get())
            a.append(self.addPlayer2.get())
            flag = 1
            for i in a:
                if (len(i) == 0):
                    flag = 0
            if (flag == 1):
                DataBase.addRecord(self.base, a)
                self.addNameGame.delete(1, tk.END)
                self.addTeam.delete(1, tk.END)
                self.addCap.delete(1, tk.END)
                self.addYear.delete(1, tk.END)
                self.addAge.delete(1, tk.END)
                self.addPlayer1.delete(1, tk.END)
                self.addPlayer2.delete(1, tk.END)
                self.__init__(self.base)
                self.buttAdd()
            self.addNameGame.place(x=100, y=600)
            self.addTeam.place(x=226, y=600)
            self.addCap.place(x=328, y=600)
            self.addYear.place(x=413, y=600)
            self.addPlayer1.place(x=515, y=600)
            self.addPlayer2.place(x=674, y=600)
            self.addAge.place(x=833, y=600)

        def sortDisp(self, event, newSort):
            if (self.currSort == newSort):
                self.flagSort = (self.flagSort + 1) % 2
            else:
                self.flagSort = 1
            self.base = DataBase.sort(newSort, self.flagSort)
            self.currSort = newSort
            self.buttSort()

        def search(self):
            def end():
                """
                Author: Иртикеев М.Н.
                Поиск
                """
                b = self.entryTop2.get()
                d = self.entryTop4.get()
                self.__init__(DataBase.search(b, d))
                self.Top.destroy()

            self.Top = tk.Toplevel(bg="aqua")
            self.label = tk.Label(self.Top, text="Max age", bg="aqua")
            self.label.grid(row=2, column=0)
            self.entryTop2 = tk.Entry(self.Top, width=10)
            self.entryTop2.grid(row=3, column=0)
            self.label = tk.Label(self.Top, text="Max years of creation", bg="aqua")
            self.label.grid(row=6, column=0)
            self.entryTop4 = tk.Entry(self.Top, width=10)
            self.entryTop4.grid(row=7, column=0)
            self.end = tk.Button(self.Top, text="Search.", bg="green")
            self.end.bind("<Button-1>", lambda event: end())
            self.end.grid(row=8, column=0)

    root = tk.Tk()
    from importlib.machinery import SourceFileLoader

    DataBase = SourceFileLoader("DataBase.py", "../Library/DataBase.py").load_module()
    root.title("Games Date Base")
    root.geometry('800x480')
    root.configure(bg='#555')
    root.resizable(False, False)
    window = MainWindow(DataBase.readData())
    root['bg'] = "blue"
    root.mainloop()

display()