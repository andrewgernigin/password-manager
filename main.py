from tkinter import *
from tkinter import messagebox
import password_generator as pwg
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_generator = pwg.PasswordGenerator()
    password_entry.delete(0, END)
    password = password_generator.generate_password()
    pyperclip.copy(password)
    password_entry.insert(0, password)
    del password_generator


# ---------------------------- SAVE PASSWORD ------------------------------- #

def add_password():
    website = website_entry.get().title()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Error", message="All fields are required before saving.")
    else:
        try:
            with open("data.json", "r") as file:
                # Read old data
                data = json.load(file)
                if website in data:
                    if messagebox.askyesno(title="Warning",
                                           message=f"You already have a password saved for {website}. "
                                                   f"Do you want to overwrite existing password?"):
                        # Updating old data with new data
                        data.update(new_data)
                    else:
                        return
                else:
                    data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                # create json file and save new_data to it
                json.dump(new_data, file, indent=4)
        else:
            with open("data.json", "w") as file:
                # Save updated data
                json.dump(data, file, indent=4)
        finally:
            # Clear entry fields and return focus to website entry
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# ---------------------------- SEARCH FILE ------------------------------- #
def find_password():
    website = website_entry.get().title()
    if len(website) == 0:
        messagebox.showwarning(title="Error", message="You must enter a website in order to search.")
    else:
        try:
            with open("data.json", "r") as file:
                # open file and read contents to a dictionary
                data = json.load(file)
        except FileNotFoundError:
            # if no json file exists
            messagebox.showwarning(title="Error", message="No Data File Found.")
        else:
            if website in data:
                # Everything worked. Give em the goods
                username = data[website]["username"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {password}")
            else:
                messagebox.showwarning(title="Error", message="No details for that website exist.")


# ---------------------------- UI SETUP ------------------------------- #

# main window and canvas with logo
window = Tk()
window.title("Password Manager")
# window.geometry("300x300")
window.config(padx=30, pady=30)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0, )

# website label and entry
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry = Entry()
website_entry.grid(column=1, row=1, sticky=EW, pady=2, padx=2)
website_entry.focus()

# add search button
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky=EW, pady=2, padx=2)

# username label and entry
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
username_entry = Entry(width=35)
username_entry.grid(column=1, row=2, columnspan=2, sticky=EW, pady=2, padx=2)
username_entry.insert(0, "example@email.com")

# password label and entry
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky=EW, pady=2, padx=2)

# generate password button
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3, sticky=EW, pady=2, padx=2)

# add password button
add_password_button = Button(text="Add", width=36, command=add_password)
add_password_button.grid(column=1, row=4, columnspan=2, sticky=EW, pady=2, padx=2)

window.mainloop()
