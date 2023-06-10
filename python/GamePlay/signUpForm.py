from tkinter import *
from tkinter import messagebox
from python.Service.UsersService import *


def foo ():
    from python.GamePlay.Main import main
    return main()
def main ():
    window = Tk()
    window.title('Sign Up')
    window.geometry('925x500+500+300')
    window.configure(bg='#fff')
    window.resizable(False, False)


    img = PhotoImage(file='../images/signUp.png', master= window)
    Label(window, image=img,border=0, bg='white').place(x=50, y=90)

    frame = Frame(window, width=350, height=390, bg='#fff')
    frame.place(x=480, y=70)

    heading = Label(frame, text='Sign up', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)


    def signUp():
        username = user.get()
        passw = password.get()
        confPass = confirmPassword .get()
        if passw == confPass:
            register = UsersRepository().insertUser(username= username,password=passw)
            # screen = Tk()
            # screen.title('App')
            # screen.geometry('925x500+500+300')
            # screen.config(bg='white')
            # Label(screen, text='Hello everyone', bg='#fff', font=('Calibri(Body)', 50, 'bold')).pack(expand=True)
            messagebox.showinfo('Sign up','Succesfully sign up')

            window.withdraw()

    def signInCommand():
            window.withdraw()

            #foo()
            # screen.mainloop()


    # username
    def onEnter(e):
        user.delete(0, 'end')

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


    # password
    def onEnter(e):
        password.delete(0, 'end')


    def onLeave(e):
        name = password.get()
        if name == '':
            password.insert(0, 'Password')


    password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    password.place(x=30, y=150)
    password.insert(0, 'Password')
    password.bind('<FocusIn>', onEnter)
    password.bind('<FocusOut>', onLeave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)


    # confirmPassword
    def onEnter(e):
        confirmPassword.delete(0, 'end')


    def onLeave(e):
        name = confirmPassword.get()
        if name == '':
            confirmPassword.insert(0, 'Confirm password')


    confirmPassword = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    confirmPassword.place(x=30, y=220)
    confirmPassword.insert(0, 'Password')
    confirmPassword.bind('<FocusIn>', onEnter)
    confirmPassword.bind('<FocusOut>', onLeave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

    #Button
    Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0,command= signUp).place(x=35, y=280)
    label = Label(frame, text="Have an account ?", fg='black', bg='white',
                  font=('Microsoft YaHei UI Light', 9, 'bold'))
    label.place(x=90, y=340)

    signIn = Button(frame, width=6,  text='Sign in', cursor='hand2', fg='#57a1f8', bg='white', border=0,
                    font=('Microsoft YaHei UI Light', 9, 'bold'),command=signInCommand)
    signIn.place(x=220, y=339)

    window.mainloop()

if __name__ == '__main__':
    main()