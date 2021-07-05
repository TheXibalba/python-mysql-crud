# IMPORTING PYTHON LIBRARIES
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import mysql.connector

color = "#FEF7DC"
label_color = "#78DEC7"
btn_color = "#39A2DB"
window = Tk()

# TkInter Configuration

window.title("MySQL CRUD Operations")
window.geometry("650x400")
window.config(padx=40, pady=50, bg=color)


frame = Frame(window, width=500, borderwidth=10)

frame.grid(row=4, column=0, columnspan=4, pady=(20, 0))

# Style Object
style = Style()


style.configure('W.TButton', font=('calibri', 10, 'bold'),
                bg=btn_color)

style.configure('W.Label', font=("calibri", 12, 'bold'),
                background=label_color)


def clear_frame():
    for widgets in frame.winfo_children():
        widgets.destroy()


# CONNECTING TO THE DATABASE

try:
    con = mysql.connector.connect(
        host='localhost', user='root', password='', database='jupyter')
except:
    print("Error connecting to the database!")

else:
    print("Database has been created successfully!")

cursor = con.cursor()

# DATABASE OPERATIONS

def create():
    cursor.execute("CREATE TABLE IF NOT EXISTS students (name varchar(50), roll int(10))")
    messagebox.showinfo(title="CREATE COMMAND",message="Student Table was created successfully!")


def insert():
    name = name_input.get().title()
    st_roll = roll_input.get()
    if st_roll.isdigit() and int(st_roll) > 0:
        roll = int(st_roll)
        if name != "" and roll != "":
            try:
                cursor.execute(
                    f"INSERT INTO students values('{name}','{roll}')")
                affected_rows = cursor.rowcount
                print(f"Rows affected: {affected_rows}")
                if affected_rows is not None:
                    con.commit()
                    messagebox.showinfo(title="INSERT Operation",
                                        message="Data has been inserted successfully!")
                    name_input.delete(0, END)
                    roll_input.delete(0, END)
                else:
                    messagebox.showerror(title="INSERT ERROR!",
                                         message="An error has occurred!")
            except Exception:
                messagebox.showerror(
                    title="INSERT ERROR!", message="Duplicate values are not allowed!")

        else:
            messagebox.showerror(title="INSERT ERROR!",
                                 message="Empty values are not allowed!")
    else:
        messagebox.showerror(title="INSERT ERROR!",
                             message="ROLL number is invalid!")


def read():
    clear_frame()
    i = 6
    roll = search_input.get()
    cursor.execute(f"SELECT * FROM students WHERE roll='{roll}' ORDER BY roll")
    row = cursor.fetchone()
    if row is not None:
        table_heading = Label(frame, text="Student Name:",
                              style="W.Label", width=20, background="#F5A962")
        table_heading1 = Label(frame, text="Roll:",
                               style="W.Label", width=5, background="#F5A962")
        table_heading.grid(pady=5, column=0, row=5)
        table_heading1.grid(pady=5, column=1, row=5)

        display_label = Label(
            frame, text=f"{row[0]}", style="W.Label", background="#FFF9B0")
        display_label1 = Label(
            frame, text=f"{row[1]}", style="W.Label", background="#FFF9B0")
        display_label.grid(pady=(2, 0), row=i, column=0)
        display_label1.grid(pady=(2, 0), row=i, column=1)
    else:
        messagebox.showerror(title="READ ERROR!", message="No data found!")
        print(row)


def read_all():
    clear_frame()
    i = 6
    cursor.execute(f"SELECT * FROM students")
    rows = cursor.fetchall()
    print(rows)
    if len(rows) != 0:
        table_heading = Label(frame, text="Student Name:",
                              style="W.Label", width=20, background="#F5A962")
        table_heading1 = Label(frame, text="Roll:",
                               style="W.Label", width=5, background="#F5A962")
        table_heading.grid(pady=5, column=0, row=5)
        table_heading1.grid(pady=5, column=1, row=5)
        for row in rows:

            display_label = Label(
                frame, text=f"{row[0]}", style="W.Label", background="#FFF9B0")
            display_label1 = Label(
                frame, text=f"{row[1]}", style="W.Label", background="#FFF9B0")
            display_label.grid(pady=(2, 0), row=i, column=0)
            display_label1.grid(pady=(2, 0), row=i, column=1)
            print(row)
            i += 1
    else:
        messagebox.showerror(title="READ ERROR!", message="No data found!")


def update():
    new_name = new_name_input.get().title()
    st_roll = update_roll_input.get()
    if st_roll.isdigit() and int(st_roll) > 0:
        roll = int(st_roll)
        cursor.execute(
            f"UPDATE students SET name='{new_name}' WHERE roll='{roll}'")
        affected_rows = cursor.rowcount
        print(f"Rows affected: {affected_rows}")

        if affected_rows != 0:
            con.commit()
            messagebox.showinfo(title="UPDATE Operation",
                                message="Data has been updated successfully!")
            update_roll_input.delete(0, END)
            new_name_input.delete(0, END)
        else:
            messagebox.showerror(title="UPDATE ERROR!",
                                 message="Invalid ROLL number!")
    else:
        messagebox.showerror(title="UPDATE ERROR!",
                             message="Invalid ROLL number!")


def delete():
    roll = delete_input.get()
    cursor.execute(f"DELETE FROM students WHERE roll='{roll}'")
    affected_rows = cursor.rowcount
    print(f"Rows affected: {affected_rows}")

    if affected_rows != 0:
        con.commit()
        messagebox.showinfo(title="DELETE Operation",
                            message="The entry has been deleted successfully!")
        delete_input.delete(0, END)
    else:
        messagebox.showerror(title="DELETE ERROR!",
                             message="Data was not found!")


# GRAPHICAL USER INTERFACE:
name_label = Label(text="Student Name: ", style="W.Label")
name_label.grid(row=0, column=0)

name_input = Entry()
name_input.grid(row=0, column=1)

roll_label = Label(text="Roll number: ", style="W.Label")
roll_label.grid(row=0, column=2, padx=5)

roll_input = Entry()
roll_input.grid(row=0, column=3)

add_btn = Button(text="Add Student", command=insert, style="W.TButton")
add_btn.grid(row=0, column=4, padx=5)

delete_label = Label(text="Delete a student: ", style="W.Label")
delete_label.grid(row=1, column=0, pady=(10, 0))

delete_input = Entry()
delete_input.grid(row=1, column=1, pady=(10, 0))

delete_button = Button(text="Delete", command=delete,
                       width=10, style="W.TButton")
delete_button.grid(row=1, column=2, pady=(10, 0))


update_label = Label(text="Update(Enter Roll): ", style="W.Label")
update_label.grid(row=2, column=0, pady=(10, 0))

update_roll_input = Entry()
update_roll_input.grid(row=2, column=1, pady=(10, 0))


new_name_label = Label(text="New Name: ", style="W.Label")
new_name_label.grid(row=2, column=2, pady=(10, 0))

new_name_input = Entry()
new_name_input.grid(row=2, column=3, pady=(10, 0))

update_button = Button(text="Update", command=update,
                       width=10, style="W.TButton")
update_button.grid(row=2, column=4, pady=(10, 0))


search_label = Label(text="Search(Enter Roll): ", style="W.Label")
search_label.grid(row=3, column=0, pady=(10, 0))

search_input = Entry()
search_input.grid(row=3, column=1, pady=(10, 0))

search_button = Button(text="Search", command=read,
                       width=10, style="W.TButton")
search_button.grid(row=3, column=2, pady=(10, 0))

search_button = Button(text="Display all", command=read_all,
                       width=10, style="W.TButton")
search_button.grid(row=3, column=3, pady=(10, 0))
create()

window.mainloop()
