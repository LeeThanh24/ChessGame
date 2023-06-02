from tkinter import *
import signUpForm
import main
def loginForm ():
    root = Tk()
    root.title('login')
    root.geometry('925x500+500+300')
    root.configure(bg='#fff')
    root.resizable(False, False)

    img = PhotoImage(file='images/login.png',master=root)
    Label(root, image=img, bg='white').place(x=50, y=50)

    frame = Frame(root, width=350, height=350, bg='white')
    frame.place(x=480, y=70)

    heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)


    def signIn():
        username = user.get()
        passw = password.get()

        if username == 'admin' and passw == '1234':
            root.destroy()
            main.main_menu()
            # screen = Tk()
            # screen.title('App')
            # screen.geometry('925x500+500+300')
            # screen.config(bg='white')
            # Label(screen, text='Hello everyone', bg='#fff', font=('Calibri(Body)', 50, 'bold')).pack(expand=True)
            #
            # screen.mainloop()

    def signUpCommand():
        signUpForm.main()




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

    # dont have account , sign up

    Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signIn).place(x=35, y=204)
    label = Label(frame, text="Don't have an account ?", fg='black', bg='white',
                  font=('Microsoft YaHei UI Light', 9, 'bold'))
    label.place(x=75, y=270)

    signUp = Button(frame, width=6, pady=6, text='Sign up', cursor='hand2', fg='#57a1f8', bg='white', border=0,
                    font=('Microsoft YaHei UI Light', 9, 'bold'),command= signUpCommand)
    signUp.place(x=245, y=264)
    root.mainloop()

if __name__ == '__main__':
    loginForm()
