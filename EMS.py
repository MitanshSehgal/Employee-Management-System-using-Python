import sqlite3
import customtkinter
from tkinter import messagebox, END
from tkinter import ttk

# Database Connection
db = sqlite3.connect("Employee.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS EMPLOYEES (Employee_ID INTEGER PRIMARY KEY, Name TEXT, Age INTEGER, Role TEXT)")
db.commit()

# App Window
app = customtkinter.CTk()
app.title("Employee Management System")
app.geometry("800x500")
app.config(bg="#17043d")

# Fonts
font1 = ("Arial", 20, "bold")
font2 = ("Arial", 15, "bold")
font3 = ("Arial", 12, "bold")

# Frame
frame1 = customtkinter.CTkFrame(app, fg_color="#FFFFFF")
frame1.place(x=350, y=0, width=450, height=500)

# Labels & Entry Boxes
id_label = customtkinter.CTkLabel(app, text="ID:", font=font1)
id_label.place(x=20, y=20)
id_entry = customtkinter.CTkEntry(app, font=font2, width=200)
id_entry.place(x=140, y=20)

name_label = customtkinter.CTkLabel(app, text="Name:", font=font1)
name_label.place(x=20, y=80)
name_entry = customtkinter.CTkEntry(app, font=font2, width=200)
name_entry.place(x=140, y=80)

age_label = customtkinter.CTkLabel(app, text="Age:", font=font1)
age_label.place(x=20, y=140)
age_entry = customtkinter.CTkEntry(app, font=font2, width=200)
age_entry.place(x=140, y=140)

role_label = customtkinter.CTkLabel(app, text="Role:", font=font1)
role_label.place(x=20, y=200)
role_entry = customtkinter.CTkEntry(app, font=font2, width=200)
role_entry.place(x=140, y=200)

# Treeview Style
style = ttk.Style()
style.configure("mystyle.Treeview", font=font3, rowheight=50)
style.configure("mystyle.Treeview.Heading", font=font2)
style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])

# Treeview
tv = ttk.Treeview(frame1, columns=("1", "2", "3", "4"), show="headings", style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.heading("2", text="Name")
tv.heading("3", text="Age")
tv.heading("4", text="Role")
tv.pack()

def insert():
    try:
        if not (id_entry.get() and name_entry.get() and age_entry.get() and role_entry.get()):
            messagebox.showerror("Error", "Please Enter All The Data.")
            return
        
        cursor.execute("INSERT INTO EMPLOYEES VALUES (?, ?, ?, ?)",
                       (int(id_entry.get()), name_entry.get(), int(age_entry.get()), role_entry.get()))
        db.commit()
        messagebox.showinfo("Inserted", "Employee Has Been Inserted.")
        display_data()
        clear()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Employee ID already exists.")
    except ValueError:
        messagebox.showerror("Error", "Invalid Age or ID format.")

def clear():
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    role_entry.delete(0, END)

def fetch():
    cursor.execute("SELECT * FROM EMPLOYEES")
    return cursor.fetchall()

def display_data():
    tv.delete(*tv.get_children())
    for row in fetch():
        tv.insert("", END, values=row)

def delete():
    if not id_entry.get():
        messagebox.showerror("Error", "Please enter an Employee ID to delete.")
        return
    cursor.execute("DELETE FROM EMPLOYEES WHERE Employee_ID=?", (int(id_entry.get()),))
    db.commit()
    messagebox.showinfo("Deleted", "Employee Has Been Deleted.")
    display_data()
    clear()

def get_data(event):
    try:
        clear()
        selected_row = tv.focus()
        data = tv.item(selected_row)
        row = data.get("values", [])
        if row:
            id_entry.insert(0, row[0])
            name_entry.insert(0, row[1])
            age_entry.insert(0, row[2])
            role_entry.insert(0, row[3])
    except IndexError:
        pass

def update():
    try:
        if not (id_entry.get() and name_entry.get() and age_entry.get() and role_entry.get()):
            messagebox.showerror("Error", "Please Enter All The Data.")
            return
        cursor.execute("UPDATE EMPLOYEES SET Name=?, Age=?, Role=? WHERE Employee_ID=?",
                       (name_entry.get(), int(age_entry.get()), role_entry.get(), int(id_entry.get())))
        db.commit()
        messagebox.showinfo("Updated", "Employee's details have been updated.")
        display_data()
    except ValueError:
        messagebox.showerror("Error", "Invalid Age or ID format.")

tv.bind("<ButtonRelease-1>", get_data)

display_data()

# Buttons
save_button = customtkinter.CTkButton(app, command=insert, text="Save", font=font1, width=120)
save_button.place(x=70, y=250)

update_button = customtkinter.CTkButton(app, command=update, text="Update", font=font1, width=127)
update_button.place(x=200, y=250)

clear_button = customtkinter.CTkButton(app, command=clear, text="Clear", font=font1, width=120)
clear_button.place(x=70, y=300)

delete_button = customtkinter.CTkButton(app, command=delete, text="Delete", font=font1, width=140)
delete_button.place(x=200, y=300)

app.mainloop()