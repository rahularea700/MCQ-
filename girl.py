import tkinter as tk
from tkinter import *
import random
import sqlite3
import time
import json



def convert_dict_to_list(nested_dict):
    nested_list = []
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            nested_list.append(convert_dict_to_list(value))
        else:
            nested_list.append(value)
    return nested_list


def fromJSON(filename):
    fileData = open(filename, "r", encoding="utf-8")
    nested_dict = json.load(fileData)
    nested_list = convert_dict_to_list(nested_dict)
    return nested_list


easyQ = fromJSON("physic.json")
mediumQ = fromJSON("chemistry.json")
hardQ = fromJSON("math.json")


def loginPage(logdata):
    sup.destroy()
    global login
    login = Tk()
    login.title("MCQ Software")
    user_name = StringVar()
    password = StringVar()

    login_canvas = Canvas(login, width=720, height=420, bg="#101357")
    login_canvas.pack(fill="both", expand=True)

    login_frame = Frame(login_canvas, bg="white")
    login_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    # login_frame.pack(fill="both", expand=True)

    heading = Label(login_frame, text="Login your account", fg="black", bg="white")
    heading.config(font='Georgia 40')
    heading.place(relx=0.31, rely=0.21)

    # USER NAME
    ulabel = Label(login_frame, text="Username", fg='black', bg='white', font=("Georgia", 15))
    ulabel.place(relx=0.21, rely=0.4)
    uname = Entry(login_frame, bg='#d3d3d3', fg='black', textvariable=user_name, font=(50))
    uname.config(width=42)
    uname.place(relx=0.31, rely=0.4)

    # PASSWORD
    plabel = Label(login_frame, text="Password", fg='black', bg='white', font=("Georgia", 15))
    plabel.place(relx=0.215, rely=0.5)
    pas = Entry(login_frame, bg='#d3d3d3', fg='black', textvariable=password, font=(50))
    pas.config(width=42)
    pas.place(relx=0.31, rely=0.5)

    def check():
        for a, b, c, d in logdata:
            if b == uname.get() and c == pas.get():
                menu()
                break
        else:
            error = Label(login_frame, text="Wrong Username or Password!", fg='black', bg='white')
            error.place(relx=0.37, rely=0.7)

    # LOGIN BUTTON
    log = Button(login_frame, text='Login', padx=5, pady=5, width=5, command=check, font=(55))
    log.configure(width=15, height=1, activebackground="#33B5E5", relief=FLAT)
    log.place(relx=0.4, rely=0.6)

    login.mainloop()


def signUpPage():
    root.destroy()
    global sup
    sup = Tk()
    sup.title("MCQ Software")
    fname = StringVar()
    uname = StringVar()
    passW = StringVar()
    country = StringVar()

    sup_canvas = Canvas(sup, width=720, height=440, bg="#101357")
    sup_canvas.pack(fill="both", expand=True)
    # Wherever the canvas is packed, the fill="both", expand=True parameter has been passed to auto resize itself
    # the main Frame on maximize.

    sup_frame = Frame(sup_canvas, bg="white")
    sup_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    heading = Label(sup_frame, text="Sign Up and Log in ", fg="black", bg="white", font=("Georgia", 70))
    heading.config(font='Georgia 40')
    heading.place(relx=0.33, rely=0.2)

    # full name
    flabel = Label(sup_frame, text="Full Name", fg='black', bg='white', font=("Georgia", 15))
    flabel.place(relx=0.21, rely=0.4)
    fname = Entry(sup_frame, bg='#d3d3d3', fg='black', textvariable=fname, font=(50))
    fname.config(width=42)
    fname.place(relx=0.31, rely=0.4)

    # username
    ulabel = Label(sup_frame, text="Username", fg='black', bg='white', font=("Georgia", 15))
    ulabel.place(relx=0.21, rely=0.5)
    user = Entry(sup_frame, bg='#d3d3d3', fg='black', textvariable=uname, font=50)
    user.config(width=42)
    user.place(relx=0.31, rely=0.5)

    # password
    plabel = Label(sup_frame, text="Password", fg='black', bg='white', font=("Georgia", 15))
    plabel.place(relx=0.215, rely=0.6)
    pas = Entry(sup_frame, bg='#d3d3d3', fg='black', textvariable=passW, font=(50))
    pas.config(width=42)
    pas.place(relx=0.31, rely=0.6)

    # country
    clabel = Label(sup_frame, text="Country", fg='black', bg='white', font=("Georgia", 15))
    clabel.place(relx=0.215, rely=0.7)
    c = Entry(sup_frame, bg='#d3d3d3', fg='black', textvariable=country, font=(50))
    c.config(width=42)
    c.place(relx=0.31, rely=0.7)

    def addUserToDataBase():
        fullname = fname.get()
        username = user.get()
        password = pas.get()
        country = c.get()

        conn = sqlite3.connect('quiz.db')
        create = conn.cursor()
        create.execute('CREATE TABLE IF NOT EXISTS userSignUp(FULLNAME text, USERNAME text,PASSWORD text,COUNTRY text)')
        create.execute("INSERT INTO userSignUp VALUES (?,?,?,?)", (fullname, username, password, country))
        conn.commit()
        create.execute('SELECT * FROM userSignUp')
        z = create.fetchall()
        print(z)
        #        L2.config(text="Username is "+z[0][0]+"\nPassword is "+z[-1][1])
        conn.close()
        loginPage(z)

    def gotoLogin():
        conn = sqlite3.connect('quiz.db')
        create = conn.cursor()
        conn.commit()
        create.execute('SELECT * FROM userSignUp')
        z = create.fetchall()
        loginPage(z)

    # signup BUTTON
    sp = Button(sup_frame, text='Sign up', padx=5, pady=5, width=5, command=addUserToDataBase, font=(55))
    sp.configure(width=15, height=1, activebackground="#33B5E5", relief=FLAT)
    sp.place(relx=0.4, rely=0.8)

    log = Button(sup_frame, text='Log in', padx=5, pady=5, width=5, command=gotoLogin, bg="white", font=(40))
    log.configure(width=16, height=1, activebackground="#33B5E5", relief=FLAT)
    log.place(relx=0.4, rely=0.9)

    sup.mainloop()


def menu():
    login.destroy()
    global menu
    menu = Tk()
    menu.title("MCQ Software")

    menu_canvas = Canvas(menu, width=720, height=440, bg="#101357")
    menu_canvas.pack(fill="both", expand=True)

    menu_frame = Frame(menu_canvas, bg="white")
    menu_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    wel = Label(menu_canvas, text=' W E L C O M E  T O  O U R  P O R T A L ', fg="white", bg="#101357", font=(70))
    wel.config(font=('Broadway 30'))
    wel.place(relx=0.1, rely=0.02)

    level = Label(menu_frame, text='Select your Subject !!', bg="white", font=("Georgia 30"))
    level.config(font=('Georgia 35'))
    level.place(relx=0.25, rely=0.2)

    var = IntVar()
    easyR = Radiobutton(menu_frame, text='Physics', bg="white", font=("Georgia 25"), value=1, variable=var)
    easyR.place(relx=0.25, rely=0.4)

    mediumR = Radiobutton(menu_frame, text='Chemistry', bg="white", font=("Georgia 25"), value=2, variable=var)
    mediumR.place(relx=0.25, rely=0.5)

    hardR = Radiobutton(menu_frame, text='Maths', bg="white", font=("Georgia 25"), value=3, variable=var)
    hardR.place(relx=0.25, rely=0.6)

    def navigate():

        x = var.get()
        print(x)
        if x == 1:
            menu.destroy()
            easy()
        elif x == 2:
            menu.destroy()
            medium()

        elif x == 3:
            menu.destroy()
            difficult()
        else:
            pass

    letsgo = Button(menu_frame, text="Let's Go", bg="white", font=("Georgia 20"), command=navigate)
    letsgo.place(relx=0.25, rely=0.8)
    menu.mainloop()


def easy():
    global e
    e = Tk()
    e.title("MCQ Software")
    easy_canvas = Canvas(e, width=720, height=440, bg="#101357")
    easy_canvas.pack(fill="both", expand=True)

    easy_frame = Frame(easy_canvas, bg="white")
    easy_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(120, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            easy_frame.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return -1
        else:
            return 0

    global score
    score = 0


    answer = [
        " A car slowing down as it approaches a traffic light",
        "Ampere",
        "Energy is conserved in all physical processes.",
        "Glass",
        "Newton's third law states that for every action, there is an equal and opposite reaction."
    ]
    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    ques = Label(easy_frame, text=easyQ[x][0], font="Georgia 19", bg="white")
    ques.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    a = Radiobutton(easy_frame, text=easyQ[x][1], font="Georgia 18", value=easyQ[x][1], variable=var, bg="white")
    a.place(relx=0.5, rely=0.42, anchor=CENTER)

    b = Radiobutton(easy_frame, text=easyQ[x][2], font="Georgia 18", value=easyQ[x][2], variable=var, bg="white")
    b.place(relx=0.5, rely=0.52, anchor=CENTER)

    c = Radiobutton(easy_frame, text=easyQ[x][3], font="Georgia 18", value=easyQ[x][3], variable=var, bg="white")
    c.place(relx=0.5, rely=0.62, anchor=CENTER)

    d = Radiobutton(easy_frame, text=easyQ[x][4], font="Georgia 18", value=easyQ[x][4], variable=var, bg="white")
    d.place(relx=0.5, rely=0.72, anchor=CENTER)

    li.remove(x)

    timer = Label(e)
    timer.place(relx=0.8, rely=0.84, anchor=CENTER)              ######################################## per question timer

    def display():

        if len(li) == 1:
            e.destroy()
            showMark(score)
        if len(li) == 2:
            nextQuestion.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            ques.configure(text=easyQ[x][0])

            a.configure(text=easyQ[x][1], value=easyQ[x][1])

            b.configure(text=easyQ[x][2], value=easyQ[x][2])

            c.configure(text=easyQ[x][3], value=easyQ[x][3])

            d.configure(text=easyQ[x][4], value=easyQ[x][4])

            # ..........................................................................
            def goBack():
                nonlocal x
                if len(li) == len(easyQ):
                    return  # If it's the first question, cannot go back

                li.append(x)  # Add the current question back to the list
                x = li[-2]  # Get the previous question index

                # Update question and options
                ques.configure(text=easyQ[x][0])
                a.configure(text=easyQ[x][1], value=easyQ[x][1])                         #####################################################      back
                b.configure(text=easyQ[x][2], value=easyQ[x][2])
                c.configure(text=easyQ[x][3], value=easyQ[x][3])
                d.configure(text=easyQ[x][4], value=easyQ[x][4])

                li.remove(x)  # Remove the previous question from the list

            back_button = Button(easy_frame, text="Previous", font="Georgia 17", command=goBack)
            back_button.place(relx=0.1, rely=0.82, anchor=CENTER)
            # ..........................................................................

            li.remove(x)
            print(li)
            y = countDown()
            if y == -1:
                display()

    def calc():
        global score
        if (var.get() in answer):
            score += 1
        display()
    # def man():
    #     global score
    #     if(var.get() in answer):
    #         score -= 1
    #         display()

    submit = Button(easy_frame, command=calc, text="Submit", font=24) ###########################################################submit
    submit.place(relx=0.5, rely=0.82, anchor=CENTER)

    nextQuestion = Button(easy_frame, command=display, text="Next", font=24) ####################################################next
    nextQuestion.place(relx=0.87, rely=0.82, anchor=CENTER)

    # backQuestion=Button(easy_frame,command=man, text="back",font=24)
    # backQuestion.place(relx=0.25, rely=0.82, anchor=CENTER)


    y = countDown()
    if y == -1:
        display()
    e.mainloop()


def medium():
    global m
    m = Tk()
    m.title("MCQ Software")
    med_canvas = Canvas(m, width=720, height=440, bg="#101357")
    med_canvas.pack(fill="both", expand=True)

    med_frame = Frame(med_canvas, bg="white")
    med_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(120, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            med_frame.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return (-1)
        else:
            return 0

    global score
    score = 0


    answer = [
        "Chlorine",
        "7",
        "Combustion of gasoline",
        "Helium",
        "H2O"
    ]

    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    ques = Label(med_frame, text=mediumQ[x][0], font="Georgia 19", bg="white")
    ques.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    a = Radiobutton(med_frame, text=mediumQ[x][1], font="Georgia 18", value=mediumQ[x][1], variable=var, bg="white")
    a.place(relx=0.5, rely=0.42, anchor=CENTER)

    b = Radiobutton(med_frame, text=mediumQ[x][2], font="Georgia 18", value=mediumQ[x][2], variable=var, bg="white")
    b.place(relx=0.5, rely=0.52, anchor=CENTER)

    c = Radiobutton(med_frame, text=mediumQ[x][3], font="Georgia 18", value=mediumQ[x][3], variable=var, bg="white")
    c.place(relx=0.5, rely=0.62, anchor=CENTER)

    d = Radiobutton(med_frame, text=mediumQ[x][4], font="Georgia 18", value=mediumQ[x][4], variable=var, bg="white")
    d.place(relx=0.5, rely=0.72, anchor=CENTER)

    # ........................................................+-
    def goBack():
        nonlocal x
        if len(li) == len(mediumQ):
            return  # If it's the first question, cannot go back

        li.append(x)  # Add the current question back to the list
        x = li[-2]  # Get the previous question index

        # Update question and options
        ques.configure(text=mediumQ[x][0])
        a.configure(text=mediumQ[x][1], value=mediumQ[x][1])                                        ###########################################        back
        b.configure(text=mediumQ[x][2], value=mediumQ[x][2])
        c.configure(text=mediumQ[x][3], value=mediumQ[x][3])
        d.configure(text=mediumQ[x][4], value=mediumQ[x][4])

        li.remove(x)  # Remove the previous question from the list

    back_button = Button(med_frame, text="Previous", font="Georgia 18", command=goBack)
    back_button.place(relx=0.1, rely=0.82, anchor=CENTER)

    # ........................................................

    li.remove(x)

    timer = Label(m)
    timer.place(relx=0.8, rely=0.84, anchor=CENTER)                                    ###############################################perquestion timer

    def display():

        if len(li) == 1:
            m.destroy()
            showMark(score)
        if len(li) == 2:
            nextQuestion.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            ques.configure(text=mediumQ[x][0])

            a.configure(text=mediumQ[x][1], value=mediumQ[x][1])

            b.configure(text=mediumQ[x][2], value=mediumQ[x][2])

            c.configure(text=mediumQ[x][3], value=mediumQ[x][3])

            d.configure(text=mediumQ[x][4], value=mediumQ[x][4])

            li.remove(x)
            print(li)
            y = countDown()
            if y == -1:
                display()

    def calc():
        global score
        if (var.get() in answer):
            score += 1
        display()

    submit = Button(med_frame, command=calc, text="Submit", font=24)
    submit.place(relx=0.5, rely=0.82, anchor=CENTER)

    nextQuestion = Button(med_frame, command=display, text="Next", font=24)
    nextQuestion.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
    m.mainloop()


def difficult():
    global h
    h = Tk()
    h.title("MCQ Software")
    hard_canvas = Canvas(h, width=720, height=440, bg="#101357")
    hard_canvas.pack(fill="both", expand=True)

    hard_frame = Frame(hard_canvas, bg="white")
    hard_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(120, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k) ######################################################################################  TIME
            hard_frame.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return (-1)
        else:
            return 0

    global score
    score = 0


    answer = [
        "3.14",
        "2",
        "Right triangle",
        "8",
        "0"
    ]

    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    ques = Label(hard_frame, text=hardQ[x][0], font="Georgia 19", bg="white")
    ques.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    a = Radiobutton(hard_frame, text=hardQ[x][1], font="Georgia 18", value=hardQ[x][1], variable=var, bg="white")
    a.place(relx=0.5, rely=0.42, anchor=CENTER)

    b = Radiobutton(hard_frame, text=hardQ[x][2], font="Georgia 18", value=hardQ[x][2], variable=var, bg="white")
    b.place(relx=0.5, rely=0.52, anchor=CENTER)

    c = Radiobutton(hard_frame, text=hardQ[x][3], font="Georgia 18", value=hardQ[x][3], variable=var, bg="white")
    c.place(relx=0.5, rely=0.62, anchor=CENTER)

    d = Radiobutton(hard_frame, text=hardQ[x][4], font="Georgia 18", value=hardQ[x][4], variable=var, bg="white")
    d.place(relx=0.5, rely=0.72, anchor=CENTER)
    # ........................................................
    def goBack():
        nonlocal x
        if len(li) == len(hardQ):
            return  # If it's the first question, cannot go back

        li.append(x)  # Add the current question back to the list
        x = li[-2]  # Get the previous question index

        # Update question and options
        ques.configure(text=hardQ[x][0])
        a.configure(text=hardQ[x][1], value=hardQ[x][1])
        b.configure(text=hardQ[x][2], value=hardQ[x][2])
        c.configure(text=hardQ[x][3], value=hardQ[x][3])                                ###############################################################        back
        d.configure(text=hardQ[x][4], value=hardQ[x][4])

        li.remove(x)  # Remove the previous question from the list

    back_button = Button(hard_frame, text="Previous", font="Georgia 18", command=goBack)
    back_button.place(relx=0.1, rely=0.82, anchor=CENTER)
    # ........................................................

    li.remove(x)

    timer = Label(h)
    timer.place(relx=0.8, rely=0.84, anchor=CENTER)                                        #########################################################perquestiontimer

    def display():

        if len(li) == 1:
            h.destroy()
            showMark(score)
        if len(li) == 2:
            nextQuestion.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            ques.configure(text=hardQ[x][0])

            a.configure(text=hardQ[x][1], value=hardQ[x][1])

            b.configure(text=hardQ[x][2], value=hardQ[x][2])

            c.configure(text=hardQ[x][3], value=hardQ[x][3])

            d.configure(text=hardQ[x][4], value=hardQ[x][4])

            li.remove(x)
            print(li)
            y = countDown()
            if y == -1:
                display()

    def calc():
        global score
        if (var.get() in answer):
            score += 1
        display()

    submit = Button(hard_frame, command=calc, text="Submit", font=24)
    submit.place(relx=0.5, rely=0.82, anchor=CENTER)

    nextQuestion = Button(hard_frame, command=display, text="Next", font=24)
    nextQuestion.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
    h.mainloop()


def showMark(mark):
    global sh
    sh = Tk()
    sh.title("MCQ Software")
    show_canvas = Canvas(sh, width=720, height=440, bg="#101357")
    show_canvas.pack(fill="both", expand=True)

    show_frame = Frame(show_canvas, bg="white")
    show_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    st = "Your score is " + str(mark)
    mlabel = Label(show_canvas, text=st, fg="black", font="Georgia,100")
    mlabel.place(relx=0.5, rely=0.2, anchor=CENTER)

    sh.mainloop()


def start():
    global root
    root = Tk()
    root.title("MCQ Software")
    canvas = Canvas(root, width=720, height=440, bg='dark blue')
    canvas.pack(fill="both", expand=1)
    canvas.grid(column=0, row=1)
    ##########################################################################################################
    # frontpagephoto



    img=PhotoImage(file="123.png")
    canvas.create_image(00, 00, image=img, anchor=NW, )

    ###########################################################################################################

    button = Button(root, text='Start', command=signUpPage)
    button.configure(width=102, height=2, activebackground="#33B5E5", relief=RAISED)
    button.grid(column=0, row=2)

    root.mainloop()


if __name__ == '__main__':
    start()
