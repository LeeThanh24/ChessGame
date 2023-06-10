from tkinter import *
import signUpForm
from python.GamePlay import Menu
from python.Service.UsersService import *
from tkinter import messagebox


def loginForm():
    root = Tk()
    root.title('login')
    root.geometry('925x500+500+300')
    root.configure(bg='#fff')
    root.resizable(False, False)

    # img = PhotoImage(file='images/login.png',master=root)
    # Label(root, image=img, bg='white').place(x=50, y=50)

    frame = Frame(root, width=350, height=350, bg='white')
    frame.place(x=480, y=70)

    heading = Label(frame, text='Player 2', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)

    frame2 = Frame(root, width=350, height=350, bg='white')
    frame2.place(x=100, y=70)
    heading2 = Label(frame2, text='Player 1', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading2.place(x=100, y=5)

    def signIn():
        username = user.get()
        passw = password.get()
        username2 = user2.get()
        passw2 = password2.get()
        print(f"{username} - {passw},{username2}- {passw2}")
        score1= UsersService().findScoreByUsername(username)
        score2= UsersService().findScoreByUsername(username2)
        usersService = UsersService()
        if usersService.checkLogin(username, passw) and usersService.checkLogin(username2,
                                                                                passw2) and username != username2:
            root.destroy()
            Menu.main_menu(username, username2, score1, score2)
        else:
            messagebox.showinfo("Login", "Login failed !")

    def signUpCommand():
        signUpForm.main()

    # username
    def onEnter(e):
        # user.delete(0, 'end')
        pass

    def onLeave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username')

    user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', onEnter)
    user.bind('<FocusOut>', onLeave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    # username 2
    def onEnter2(e):
        # user2.delete(0, 'end')
        pass

    def onLeave2(e):
        name2 = user2.get()
        if name2 == '':
            user2.insert(0, 'Username')

    user2 = Entry(frame2, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    user2.place(x=30, y=80)
    user2.insert(0, 'Username')
    user2.bind('<FocusIn>', onEnter2)
    user2.bind('<FocusOut>', onLeave2)

    Frame(frame2, width=295, height=2, bg='black').place(x=25, y=107)

    # password
    def onEnter(e):
        password.delete(0, 'end')

    def onLeave(e):
        name = password.get()
        if name == '':
            password.insert(0, 'Password')

    password = Entry(frame, show="*", width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    password.place(x=30, y=150)
    password.insert(0, 'Password')
    password.bind('<FocusIn>', onEnter)
    password.bind('<FocusOut>', onLeave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    # password 2
    def onEnter2(e):
        password2.delete(0, 'end')

    def onLeave2(e):
        name2 = password2.get()
        if name2 == '':
            password2.insert(0, 'Password')

    password2 = Entry(frame2, show="*", width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    password2.place(x=30, y=150)
    password2.insert(0, 'Password')
    password2.bind('<FocusIn>', onEnter2)
    password2.bind('<FocusOut>', onLeave2)

    Frame(frame2, width=295, height=2, bg='black').place(x=25, y=177)

    # dont have account , sign up

    Button(width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signIn).place(x=322, y=300)
    label = Label(text="Don't have an account ?", fg='black', bg='white',
                  font=('Microsoft YaHei UI Light', 9, 'bold'))
    label.place(x=350, y=350)

    signUp = Button(width=6, pady=6, text='Sign up', cursor='hand2', fg='#57a1f8', bg='white', border=0,
                    font=('Microsoft YaHei UI Light', 9, 'bold'), command=signUpCommand)
    signUp.place(x=515, y=344)
    root.mainloop()


if __name__ == '__main__':
    loginForm()
