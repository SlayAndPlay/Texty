from tkinter import * 
from tkinter.ttk import *
from tkinter import font, colorchooser
from tkinter import filedialog
from tkinter import messagebox
import tempfile
import os, sys, subprocess
from sh import lp


# Functionality

def statusbar_state(event):
    if textarea.edit_modified():
        word_len=len(textarea.get(0.0,END).split())                     # Split returns as list.
        characters=len(textarea.get(0.0,'end-1c').replace(' ',''))      # Len will return count of items.
        status_bar.config(text=f"Characters: {characters} | Word Count: {word_len}")
    textarea.edit_modified(0)


fontSize=12
fontStyle="Arial"
url=''
def font_style(event):
    global fontStyle
    fontStyle = font_family_var.get()
    textarea.config(font=(fontStyle,fontSize))
    
def font_size(event):
    global fontSize
    fontSize = size_var.get()
    textarea.config(font=(fontStyle,fontSize))
    
def bold_text():
    text_property=font.Font(font=textarea["font"]).actual()
    if text_property['weight']=="normal":
        textarea.config(font=(fontStyle,fontSize,"bold"))
    if text_property['weight']=='bold':
        textarea.config(font=(fontStyle,fontSize,"normal"))
    
def italic_text():
    text_property=font.Font(font=textarea["font"]).actual()
    if text_property['slant'] == "roman":
        textarea.config(font=(fontStyle,fontSize,"italic"))
    if text_property['slant'] == "italic":
        textarea.config(font=(fontStyle,fontSize,"roman"))
        
def underline_text():
    text_property=font.Font(font=textarea["font"]).actual()
    if text_property['underline'] == 0:
        textarea.config(font=(fontStyle,fontSize,'underline'))
    if text_property['underline'] == 1:
        textarea.config(font=(fontStyle,fontSize))

def strikethru_text():
    text_property=font.Font(font=textarea["font"]).actual()
    if text_property['overstrike'] == 0:
        textarea.config(font=(fontStyle,fontSize,'overstrike'))
    if text_property['overstrike'] == 1:
        textarea.config(font=(fontStyle,fontSize))
        
def new_file(event=None):
    global url
    url=''
    textarea.delete(0.0,END)
    
def open_file(event=None):
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd,title="Select File",filetypes=(('Text File','txt'),('All Files','*.*')))
    if url !='':
        data=open(url,'r')   
        textarea.insert(0.0,data.read())
    root.title("Texty" +" - "+ os.path.basename(url))
    
def save_file(event=None):
    if url =='':
        save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt'),('All Files','*.*')))
        if save_url is None:
            pass
        else:
            content=textarea.get(0.0,END)
            save_url.write(content)
            save_url.close()
    else:
        content=textarea.get(0.0,END)
        file=open(url,'w')
        file.write(content)
        
def save_as_file(event=None):
    save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt'),('All Files','*.*')))
    if save_url is None:
        pass
    else:
        content=textarea.get(0.0,END)
        save_url.write(content)
        save_url.close()
    if url != '':
        os.remove(url)
        
def printsheet(event=None):
    file=tempfile.mktemp('.txt')
    open(file,'w').write(textarea.get(1.0,END))
    if sys.platform=="win32":
        os.startfile(file,'print')
    else:
        open("temp.txt",'w').write(textarea.get(1.0,END))
        lp("temp.txt")    
    
    

def minimize_window(event=None):
    root.wm_state('iconic')   
    
def exit_window(event=None):
    if textarea.edit_modified():
        result=messagebox.askyesnocancel("Warning","Do you want to save changes made?")
        if result:
            if url!='':
                # THE COMMANDS BELOW ARE ANOTHER METHOD THAT WORK
                # content=textarea.get(0.0,END)
                # file=open(url,'w')
                # file.write(content)
                # root.destroy()
                save_file()
                root.destroy()
            else:
                # THE COMMANDS BELOW ARE ANOTHER METHOD THAT WORK 
                # content=textarea.get(0.0,END)
                # save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt'),('All Files','*.*')))
                # save_url.write(content)
                # save_url.close()
                # root.destroy()
                save_file()
                root.destroy()
        elif result==0:
            root.destroy()
        else:
            pass
    else:
        root.destroy()

    
def color_select():
    color=colorchooser.askcolor()
    textarea.config(fg=color[1])

def align_right(): 
    data=textarea.get(0.0,END)
    textarea.tag_config('right',justify=RIGHT)
    textarea.delete(0.0,END)
    textarea.insert(INSERT, data, 'right')

def align_center():
    data=textarea.get(0.0,END)
    textarea.tag_config('center',justify=CENTER)
    textarea.delete(0.0,END)
    textarea.insert(INSERT, data, 'center')
    
def align_left():
    data=textarea.get(0.0,END)
    textarea.tag_config('left',justify=LEFT)
    textarea.delete(0.0,END)
    textarea.insert(INSERT, data, 'left')
    
def change_theme(bg_color,fg_color):
    textarea.config(bg=bg_color,fg=fg_color)
    
def toolbarFunc():
    if show_toolbar.get()==0:
        tool_bar.pack_forget()
    if show_toolbar.get()==1:
        textarea.pack_forget()
        tool_bar.pack(fill=X)
        textarea.pack(fill=BOTH,expand=1)

def statusbarFunc():
    if show_statusbar.get()==0:
        status_bar.pack_forget()
    else:
        status_bar.pack()
     
def find():
    
    # functionality
    
    def find_words():
        textarea.tag_remove('match',1.0,END)
        start_pos='1.0'
        word=findEntryField.get()
        if word:
            while 1: 
                
                start_pos=textarea.search(word,start_pos,stopindex=END)
                if not start_pos:
                    break
                end_pos=f'{start_pos}+{len(word)}c'
                textarea.tag_add('match',start_pos,end_pos)
            
                textarea.tag_config('match',foreground="red",background="yellow")
                start_pos=end_pos
    
    def replace_text():
        word=findEntryField.get()
        replacWord=replaceEntryField.get()
        content=textarea.get(1.0,END)
        new_content=content.replace(word,replacWord)
        textarea.delete(1.0,END)
        textarea.insert(1.0,new_content)
    
    # GUI
    
    root1=Toplevel()
    
    root1.title("Find")
    root1.geometry("450x250+650+400")
    root1.resizable(0,0)
    
    labelFrame=LabelFrame(root1,text="Find/Replace")
    labelFrame.pack(pady=40)
    
    findLabel=Label(labelFrame,text="Find")
    findLabel.grid(row=0,column=0,padx=5,pady=5)
    findEntryField=Entry(labelFrame)
    findEntryField.grid(row=0,column=1,padx=5,pady=5)
    
    replaceLabel=Label(labelFrame,text="Replace")
    replaceLabel.grid(row=1,column=0,padx=5,pady=5)   
    replaceEntryField=Entry(labelFrame)
    replaceEntryField.grid(row=1,column=1,padx=5,pady=5)
    
    findButton=Button(labelFrame,text="FIND",command=find_words)
    replaceButton=Button(labelFrame, text="REPLACE",command=replace_text)
    findButton.grid(row=2,column=0,padx=5,pady=5)
    replaceButton.grid(row=2,column=2,padx=5,pady=5)
    def doSomething():
        textarea.tag_remove('march',1.0,END)
        root1.destroy
    root1.protocol('WM_DELETE_WINDOW',doSomething)
    root1.mainloop()
        

# Window Settings
root=Tk()
root.title("Texty")
root.geometry('1200x720+270+200')
menubar = Menu(root)
root.config(menu=menubar)


# Menu configuration

# file menu
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
newImage=PhotoImage(file="new.png")
filemenu.add_command(label="New",accelerator="Command+N",image=newImage,compound=LEFT,command=new_file)
openImage=PhotoImage(file="open.png")
filemenu.add_command(label="Open",accelerator="Command+O",image=openImage,compound=LEFT,command=open_file)
saveImage=PhotoImage(file="save.png")
filemenu.add_command(label="Save",accelerator="Command+S",image=saveImage,compound=LEFT,command=save_file)
save_asImage=PhotoImage(file="save_as.png")
filemenu.add_command(label="Save As",accelerator="Command+Option+S",image=save_asImage,compound=LEFT,command=save_as_file)
printImage=PhotoImage(file="print.png")
filemenu.add_command(label="Print",accelerator="Command+P",image=printImage,compound=LEFT,command=printsheet)
filemenu.add_separator()
exitImage=PhotoImage(file="exit.png")
filemenu.add_command(label="Exit",accelerator="Command+Q",image=exitImage,compound=LEFT,command=exit_window)


# toolbar

tool_bar=Label(root)
tool_bar.pack(side=TOP, fill=X)

font_families=font.families()
font_family_var=StringVar()
fontfamily_dropdown=Combobox(tool_bar,width=30,values=font_families,state="readonly", textvariable=font_family_var)
fontfamily_dropdown.current(font_families.index("Arial"))
fontfamily_dropdown.grid(row=0,column=0, padx=5)
size_var=IntVar()


fontsize_dropdown=Combobox(tool_bar,width=14,textvariable=size_var,state="readonly",values=tuple(range(8,81)))
fontsize_dropdown.current(4)
fontsize_dropdown.grid(row=0, column=1, padx=5)

fontfamily_dropdown.bind("<<ComboboxSelected>>",font_style)
fontsize_dropdown.bind("<<ComboboxSelected>>",font_size)

boldImage=PhotoImage(file="bold.png")
boldButtton=Button(tool_bar,image=boldImage,command=bold_text)
boldButtton.grid(row=0,column=2, padx=5)

italicImage=PhotoImage(file="italic.png")
italicButtton=Button(tool_bar,image=italicImage,command=italic_text)
italicButtton.grid(row=0,column=3, padx=5)

underlineImage=PhotoImage(file="underline.png")
underlineButtton=Button(tool_bar,image=underlineImage,command=underline_text)
underlineButtton.grid(row=0,column=4, padx=5)

strikethruImage=PhotoImage(file='strike.png')
strikethruButton=Button(tool_bar,image=strikethruImage,command=strikethru_text)
strikethruButton.grid(row=0,column=5, padx=5)
 
fontcolorImage=PhotoImage(file="font_color.png")
fontcolorButtton=Button(tool_bar,image=fontcolorImage,command=color_select)
fontcolorButtton.grid(row=0,column=6, padx=5)

leftalignImage=PhotoImage(file="left.png")
leftalignButtton=Button(tool_bar,image=leftalignImage,command=align_left)
leftalignButtton.grid(row=0,column=7, padx=5)

centeralignImage=PhotoImage(file="center.png")
centeralignButtton=Button(tool_bar,image=centeralignImage,command=align_center)
centeralignButtton.grid(row=0,column=8, padx=5)

rightalignImage=PhotoImage(file="right.png")
rightalignButtton=Button(tool_bar,image=rightalignImage,command=align_right)
rightalignButtton.grid(row=0,column=9, padx=5)


scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
textarea=Text(root,yscrollcommand=scrollbar.set,font=("arial",12))
textarea.pack(fill=BOTH, expand=1)
scrollbar.config(command=textarea.yview)


status_bar=Label(root, text="Status Bar")
status_bar.pack(side=BOTTOM)


textarea.bind('<<Modified>>',statusbar_state)


# edit menu
editmenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
cutImage=PhotoImage(file="cut.png")
editmenu.add_command(label="Cut", accelerator="Command+x",image=cutImage,compound=LEFT,command=lambda :textarea.event_generate('<Command X>'))
copyImage=PhotoImage(file="copy.png")
editmenu.add_command(label="Copy", accelerator="Command+C",image=copyImage,compound=LEFT,command=lambda :textarea.event_generate('<Command C>'))
pasteImage=PhotoImage(file="paste.png")
editmenu.add_command(label="Paste", accelerator="Command+V",image=pasteImage,compound=LEFT,command=lambda :textarea.event_generate('<Command V>'))
selectImage=PhotoImage(file="select-all.png")
editmenu.add_command(label="Select All", accelerator="Command+A",image=selectImage,compound=LEFT)
clearImage=PhotoImage(file="clear_all.png")
editmenu.add_command(label="Clear", accelerator="Command+Option+X",image=clearImage,compound=LEFT,command=lambda :textarea.delete(0.0,END))
findImage=PhotoImage(file="find.png")
editmenu.add_command(label="Find", accelerator="Command+F",image=findImage,compound=LEFT,command=find)

# view menu
show_toolbar=BooleanVar()
show_statusbar=BooleanVar()
statusbarImage=PhotoImage(file="status_bar.png")
toolbarImage=PhotoImage(file="tool_bar.png")
viewmenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
viewmenu.add_checkbutton(label="Tool Bar", variable=show_toolbar, onvalue=1, offvalue=0, image=toolbarImage,compound=LEFT,command=toolbarFunc)
show_toolbar.set(1)
viewmenu.add_checkbutton(label="Status Bar", variable=show_statusbar, onvalue=1, offvalue=0, image=statusbarImage,compound=LEFT,command=statusbarFunc)
show_statusbar.set(1)
viewmenu.add_command(label="Minimize",accelerator="Command+W",command=minimize_window)

# themes menu
themesmenu=Menu(menubar,tearoff=0)
lightdImage=PhotoImage(file="light_default.png")
lightpImage=PhotoImage(file="light_plus.png")
darkImage=PhotoImage(file="dark.png")
pinkImage=PhotoImage(file="red.png")
monokaiImage=PhotoImage(file="monokai.png")
nightblueImage=PhotoImage(file="night_blue.png")
menubar.add_cascade(label="Themes",menu=themesmenu)
theme_choice=StringVar()
themesmenu.add_radiobutton(label="Light Default", image=lightdImage, variable=theme_choice, compound=LEFT,command=lambda :change_theme("white","black"))
themesmenu.add_radiobutton(label="Light Plus", image=lightpImage, variable=theme_choice, compound=LEFT,command=lambda :change_theme("gray20","white"))
themesmenu.add_radiobutton(label="Dark", image=darkImage, variable=theme_choice, compound=LEFT,command=lambda :change_theme("black","white"))
themesmenu.add_radiobutton(label="Pink", image=pinkImage, variable=theme_choice, compound=LEFT,command=lambda :change_theme("pink","blue"))
themesmenu.add_radiobutton(label="Monokai", image=monokaiImage, variable=theme_choice, compound=LEFT,command=lambda :change_theme("orange","white"))
themesmenu.add_radiobutton(label="Night Blue", image=nightblueImage, variable=theme_choice, compound=LEFT,command=lambda :change_theme("blue","white"))

# Keyboard Bindings

root.bind("<Command-o>",open_file)
root.bind("<Command-n>",new_file)
root.bind("<Command-s>",save_file)
root.bind("<Command-S>",save_as_file)
root.bind("<Command-q>",exit_window)
root.bind("<Command-m>",minimize_window)
root.bind("<Command-p>",printsheet)





root.mainloop() 
