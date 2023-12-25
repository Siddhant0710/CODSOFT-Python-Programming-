from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add():
    t_string = t_field.get()
    if len(t_string)==0:
        messagebox.showinfo('Error','Field Empty')
    else:
        tasks.append(t_string)
        the_cursor.execute('insert into Tasks values (?)',(t_string,))
        update()
        t_field.delete(0,'end')

def update():
    clear()
    for task in tasks:
        task_listbox.insert('end', task)

def delete():
    try:
        value = task_listbox.get(task_listbox.curselection())
        if value in tasks:
            tasks.remove(value)
            update()
            the_cursor.execute('delete from tasks where title = ?',(value,))
    except:
        messagebox.showinfo('Error','No Task Selected.')

def delete_all():
    message_box = messagebox.askyesno('Delete All','Are you sure you want to delete all?')
    if message_box == True:
        while(len(tasks)!=0):
            tasks.pop()
        the_cursor.execute('delete from tasks')
        update()
        messagebox.showinfo('Delete All', 'All tasks deleted')

def clear():
    task_listbox.delete(0,'end')

def close():
    print(tasks)
    window.destroy()

def retrieve():
    while(len(tasks)!=0):
        tasks.pop()
    for row in the_cursor.execute('select Title from Tasks'):
        tasks.append(row[0])

#main

if __name__ == "__main__":
    window = Tk()
    window.title("To-Do List")
    window.geometry("750x750")
    window.resizable(0,0)
    window.configure(bg="#B5E5CF")

    connection = sql.connect('ListOfTasks.db')
    the_cursor = connection.cursor()
    the_cursor.execute('create table if not exists tasks(title text)')

    tasks=[]

    function_frame = Frame(window, bg="black")
    function_frame.pack(side="top", expand=True, fill="both")

    task_label = Label(function_frame, text = "Enter Task: ", font = ("arial","14","bold"), background="black", foreground="white")
    task_label.place(x=20, y=30)

    t_field = Entry(function_frame, font=("arial","14"), width=42, foreground="black", background="white")
    t_field.place(x=180, y=30)

    add_button = Button(function_frame, text="Add Task", width=15, bg="#D4AC0D", font=("arial", "14", "bold"), command= add)
    delete_button = Button(function_frame, text="Delete Task", width=15, bg="#D4AC0D", font=("arial", "14", "bold"), command= delete)
    delete_all_button = Button(function_frame, text="Delete All Tasks", width=15, bg="#D4AC0D", font=("arial", "14", "bold"), command= delete_all)
    exit_button = Button(function_frame, text="Exit", width=52, bg="#D4AC0D", font=("arial", "14", "bold"), command= close)

    add_button.place(x=18, y=80)
    delete_button.place(x=240, y=80)
    delete_all_button.place(x=460, y=80)
    
    task_listbox = Listbox(function_frame, width=57, height=7, font="bold", selectmode='SINGLE', background='WHITE', foreground='BLACK', selectbackground="#D4AC0D", selectforeground="BLACK")

    task_listbox.place(x=17, y=140)

    retrieve()
    update()
    window.mainloop()
    connection.commit()
    the_cursor.close()
