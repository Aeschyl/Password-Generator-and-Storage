import random
import string
import sqlite3
from tkinter import Label, Button, Tk, Entry

win = Tk()
win.title("Password Generator & Password Storage (COMPLETELY LOCAL)")
win.geometry("800x600")


def human_readable_password():
    word = " "
    while len(word) < 5:
        word = str.rstrip(random.choice(open('words.txt', 'r').readlines()))
    number = random.randint(10, 999)
    symbol = random.choice(['!', '#', '$', '_'])

    # password
    password_result_label.config(text=f"Your password is {word}{number}{symbol}")


def nonsense_password():
    # word
    limit = random.randint(6, 10)
    count = 0
    word = ""
    while count < limit:
        letter = random.choice(string.ascii_letters)
        word = word + letter
        count += 1

    # number and symbol
    number = random.randint(10, 999)
    symbol = random.choice(['!', '#', '$', '_'])

    # password
    password_result_label.config(text=f"Your password is {word}{number}{symbol}")


def store_password():
    connection = sqlite3.connect('passwords.db')

    cursor = connection.cursor()

    if not password_input.get() == "" and not key_input.get() == "":
        cursor.execute("INSERT INTO Passwords VALUES (:place, :password)",
                       {
                           'place': key_input.get(),
                           'password': password_input.get()
                       }

                       )

    connection.commit()


def retrieve_passwords():
    connection = sqlite3.connect('passwords.db')

    cursor = connection.cursor()

    cursor.execute("SELECT *, oid FROM Passwords")
    passwords = cursor.fetchall()

    print_passwords = ''
    for i in passwords:
        print_passwords += str(i[2]) + str("\t") + str(i[0]) + str("\t\t") + str(i[1]) + """

"""

    if not passwords:
        retrieved_passwords_label.configure(text="There are no passwords saved :/")
    else:
        retrieved_passwords_label.configure(text=print_passwords)

    connection.commit()


def delete():
    connection = sqlite3.connect('passwords.db')

    cursor = connection.cursor()

    try:
        cursor.execute("DELETE from Passwords WHERE oid = " + str(delete_input.get()))
    except sqlite3.OperationalError:
        pass

    connection.commit()

    retrieved_passwords_label.configure(text=" ")


header_label = Label(win, text="Welcome to the Password Generator!", font=10, fg="blue").grid(column=0, columnspan=2, row=0, pady=10)

human_readable_button = Button(win, text="Human Readable Password", command=human_readable_password)
human_readable_button.grid(column=0, row=1, ipadx=30, pady=10, ipady=10)

nonsense_button = Button(win, text="Nonsense Password", command=nonsense_password)
nonsense_button.grid(column=1, row=1, ipadx=30, pady=10, ipady=10)

password_result_label = Label(win, text=" ")
password_result_label.grid(column=0, row=2, pady=10)

space_label = Label(win, text=" ").grid(column=0, row = 3)

# ---------------------------------------------------------------------------------------------------------------

store_label = Label(win, text="Store your password!", font=10, fg="green").grid(column=0, columnspan=2, row=4)

password_label = Label(win, text="Password: ").grid(column=0, row=5)

password_input = Entry(win, width=25)
password_input.grid(column=1, row=5, pady=10)

key_label = Label(win, text="Place where you use it: ").grid(column=0, row=6)

key_input = Entry(win, width=25)
key_input.grid(column=1, row=6, pady=10)

save_button = Button(win, text="Save", command=store_password)
save_button.grid(column=0, columnspan=2, row=7, ipadx=100, pady=10)

space_label_2 = Label(win, text=" ").grid(column=0, row=9)

# ------------------------------------------------------------------------------------------------------

delete_label = Label(win, text="Enter the id to delete").grid(column=0, row=10)

delete_input = Entry(win, width=25)
delete_input.grid(column=1, columnspan=1, row=10)

retrieve_button = Button(win, text="Delete!", command=delete)
retrieve_button.grid(column=0, columnspan=2, row=11, ipadx=100, pady=10)

space_label_3 = Label(win, text=" ").grid(column=0, row=12)

# ------------------------------------------------------------------------------------------------------

retrieve_button = Button(win, text="Retrieve your passwords!", command=retrieve_passwords)
retrieve_button.grid(column=0, columnspan=2, row=13, ipadx=100, pady=10)

retrieved_passwords_label = Label(win, text=" ")
retrieved_passwords_label.grid(column=0, row=14)


win.mainloop()