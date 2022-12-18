from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesnocancel, showinfo
from tkinter.ttk import Combobox
import os

Txt = None

def new_file():
    global Txt
    root.title("Untitled - Notepad")
    Txt = None
    txt_area.delete(1.0,END)

def open_file():
    global Txt
    Txt = askopenfilename(initialdir=os.getcwd(), 
        title='Select File', filetypes=(('Text File', '*.txt')
        ,('All File','*.*')))
    if Txt == '':
        Txt = None
    else:
        root.title(os.path.basename(Txt) + ' - Notepad')
        t = open(Txt, 'r')
        txt_area.delete(1.0,END)
        txt_area.insert(1.0,t.read())
        t.close()

def save_file():
    global Txt
    if Txt == None:
        Txt = asksaveasfilename(initialfile = 'Untitled.txt', 
        defaultextension = '.txt', filetypes = [('All Files', 
        '*.*'), ('Text Documents', '*.txt')])
        if Txt == "":
            Txt = None
        else:
            t = open(Txt, 'w')
            t.write(txt_area.get(1.0, END))
            t.close()
            root.title(os.path.basename(Txt) + ' - Notepad')
    else:
        t = open(Txt, 'w')
        t.write(txt_area.get(1.0, END))
        t.close()

def saveas_file():
    global Txt
    Txt = asksaveasfilename(initialfile = 'Untitled.txt', 
        defaultextension = '.txt', filetypes = [('All Files', 
        '*.*'), ('Text Documents', '*.txt')])
    if Txt == "":
        Txt = None
    else:
        root.title(os.path.basename(Txt) + ' - Notepad')
        t = open(Txt, 'w')
        t.write(txt_area.get(1.0, END))
        t.close()

def exit_file():
    global Txt
    content1 = txt_area.get(1.0,END)
    if Txt == None:
        if len(content1)>0:
            answer = askyesnocancel('Notepad', 
                'Do you want to save changes to Untitled?')
            if answer == True:
                save_file()
                root.destroy()
            elif answer == False:
                root.destroy()
            else:
                pass
        else:
            root.destroy()
    else:
        t = open(Txt, 'r')
        content2 = str(t.read())
        if content2 != content1:
            answer = askyesnocancel('Notepad', 
                f'Do you want to save changes to {Txt}?')
            if answer == True:
                save_file()
                root.destroy()
            elif answer == False:
                root.destroy()
            else:
                pass
        else:
            root.destroy()

def selectall():
    txt_area.tag_add('sel', '1.0', 'end')

def clearall():
    txt_area.delete(1.0, END)

def helpme():
    showinfo('Help', 'We will contact you soon')

def aboutus():
    showinfo('About this Notepad', 'This Notepad is made by Sudipta Ambal')

def to_dark():
    root.config(bg="#282c34")
    txt_area.config(bg="#3a3e45",fg="white")
    tool.config(bg="#282c34",fg="white")
    status_bar.config(bg="#282c34",fg="white")
    Mymenu.entryconfig(3, label='Light Mode', command=to_light)

def to_light():
    root.config(bg="#f0f0f0")
    txt_area.config(bg="white",fg="black")
    tool.config(bg="#f0f0f0",fg="black")
    status_bar.config(bg="#f0f0f0",fg="black")
    Mymenu.entryconfig(3, label='Dark Mode', command=to_dark)

root = Tk()
root.geometry('800x500')
root.resizable(False,False)
root.title('Untitled - Notepad')
root.config(bg="#f0f0f0")
root.iconbitmap("notepad.ico")

# MENU #
Mymenu = Menu(root)
root.config(menu=Mymenu)
Mymenu.config(bg="#f0f0f0")

# SCROLL BAR #
scroll = Scrollbar(root)
scroll.pack(side=RIGHT,fill=Y)

# TOOL BAR #
tool = Label(root)
tool.pack(side=TOP,fill=X)

# STATUS BAR #
status_bar = Label(root, text ='Status Bar')
status_bar.pack(side=BOTTOM,fill=X)

# TEXT EDITOR #
txt_area = Text(root, yscrollcommand=scroll.set)
txt_area.config(wrap='word', relief=FLAT)
txt_area.pack(fill=BOTH, expand=True, padx=5)
scroll.config(command=txt_area.yview)

## Fonts ##
font_list  = font.families()
font_var = StringVar()
font_box = Combobox(tool, width = 25, textvariable=font_var,
    state='readonly')
font_box['values'] = font_list
font_box.current(font_list.index('Arial'))
font_box.grid(row=0,column=0,padx=5)

## Fontsize ##
size_list = tuple(range(8,80,2))
size_var = IntVar()
size_box = Combobox(tool, width=15, textvariable=size_var,)
size_box['values'] = size_list
size_box.current(2)
size_box.grid(row=0,column=1,padx=5)



####
current_font = 'Arial'
current_size = 12

def font_change(e):
    global current_font
    current_font = font_var.get()
    txt_area.config(font=(current_font,current_size))

def size_change(e):
    global current_size
    current_size = size_var.get()
    txt_area.config(font=(current_font,current_size))

font_box.bind("<<ComboboxSelected>>",font_change)
size_box.bind("<<ComboboxSelected>>",size_change)

txt_area.configure(font=('Arial',12))


#


text_changed = False

def changed(e):
    global text_changed
    if txt_area.edit_modified():    #hecks if any character is added or not
        text_changed= True
        words = len(txt_area.get(1.0, 'end-1c').split())    #it even counts new line character so end-1c subtracts one char
        characters = len(txt_area.get(1.0,'end-1c'))
        status_bar.config(text=f' Words: {words} Characters : {characters}')
    txt_area.edit_modified(False)
txt_area.bind('<<Modified>>',changed)


# FILE MENU #
file = Menu(Mymenu,tearoff=False)
Mymenu.add_cascade(label='File' ,menu=file)
file.add_command(label='New', command=new_file)
file.add_command(label='Open', command=open_file)
file.add_command(label='Save', command=save_file)
file.add_command(label='Save As', command=saveas_file)
file.add_separator()
file.add_command(label='Exit', command=exit_file)

# EDIT MENU #
edit = Menu(Mymenu,tearoff=False)
Mymenu.add_cascade(label='Edit' ,menu=edit)
edit.add_command(label='Cut', accelerator='Ctrl+X', command=lambda:txt_area.event_generate("<Control x>"))
edit.add_command(label='Copy', accelerator='Ctrl+X', command=lambda:txt_area.event_generate("<Control c>"))
edit.add_command(label='Paste', accelerator='Ctrl+V', command=lambda:txt_area.event_generate("<Control v>"))
edit.add_separator()
edit.add_command(label='Select All', accelerator='Ctrl+A', command=selectall)
edit.add_command(label='Clear All', command=clearall)

# DARK/LIGHT MENU #
Mymenu.add_cascade(label='Dark Mode', command=to_dark)

# HELP MENU #
Mymenu.add_cascade(label='Help' ,command=helpme)

# ABOUT MENU #
Mymenu.add_cascade(label='About' ,command=aboutus)


root.mainloop()