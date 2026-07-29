from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0,END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list_a = [random.choice(letters) for _ in range(nr_letters)]

    password_list_b = [random.choice(numbers) for _ in range(nr_symbols)]

    password_list_c = [random.choice(symbols) for _ in range(nr_numbers)]

    password_list = password_list_a+password_list_b+password_list_c

    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0,password)
    pyperclip.copy(password)
# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = website_input.get()

    try:
        with open("data.json") as file:
            data = json.load(file)
            password = data[website]["password"]
            email = data[website]["email"]
    except KeyError:
        messagebox.showinfo(title="Error",message="No Data file found.")
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="Please save password before searching")
    else:
        messagebox.showinfo(title=website,message=f"Email: {email}\nPassword: {password}")
        pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_input.get()
    email = username_input.get()
    password = password_input.get()
    new_data = {website:{
        "email":email,
        "password":password,
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="OOPS",message="Please dont leave any fields empty!")
    else:
        is_ok = messagebox.askyesno(title=website,message=f"Email: {email}\nPassword: {password}\n Are these entered detail correct?")
        if is_ok:
            try:
                with open("data.json","r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                clear()

def clear():
    website_input.delete(0,END)
    password_input.delete(0,END)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20,pady=20)

canvas = Canvas(width=200,height=200)
image_logo = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=image_logo)
canvas.grid(row=0,column=1)

#Labels
website_label = Label(text="Website: ")
website_label.grid(row=1,column=0)

username_label = Label(text="Email/Username: ")
username_label.grid(row=2, column=0)

password_label = Label(text="Password: ")
password_label.grid(row=3, column=0)

#Entry
website_input = Entry(width=35)
website_input.focus_set()
website_input.grid(row=1,column=1,sticky=EW)

username_input = Entry(width=35)
username_input.insert(0,"akashchoudhary2102@gmail.com")
username_input.grid(row=2,column=1,columnspan=2,sticky=EW)

password_input = Entry()
password_input.grid(row=3,column=1,sticky=EW)

#Buttons
search_button = Button(text="Search", command=search_password)
search_button.grid(row=1,column=2,sticky=EW)

generate_pass_btn = Button(text="Generate Password",command=generate_password)
generate_pass_btn.grid(row=3,column=2,sticky=EW)

add_button = Button(text="Add",width=36,command=save_password)
add_button.grid(row=4,column=1,columnspan=2,sticky=EW)

window.mainloop()
