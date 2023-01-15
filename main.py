from tkinter import * 
from tkinter.ttk import *
from tkinter import font, colorchooser
from tkinter import filedialog
import os

# Functionality
fontSize=12
fontStyle="Arial"
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
        
def new_file():
    textarea.delete(0.0,END)
    
def open_file():
    url=filedialog.askopenfilename(initialdir=os.getcwd,title="Select File",filetypes=(('Text File','txt'),('All Files','*.*')))
    if url !='':
        data=open(url,'r')   
        textarea.insert(0.0,data.read())
    root.title("Texty" +" - "+ os.path.basename(url))
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

# Window Settings
root=Tk()
root.title("Texty")
root.geometry('1200x720+250+200')
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
filemenu.add_command(label="Save",accelerator="Command+S",image=saveImage,compound=LEFT)
save_asImage=PhotoImage(file="save_as.png")
filemenu.add_command(label="Save As",accelerator="Command+Option+S",image=save_asImage,compound=LEFT)
filemenu.add_separator()
exitImage=PhotoImage(file="exit.png")
filemenu.add_command(label="Exit",accelerator="Command+Q",image=exitImage,compound=LEFT)

# edit menu
editmenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
cutImage=PhotoImage(file="cut.png")
editmenu.add_command(label="Cut", accelerator="Command+X",image=cutImage,compound=LEFT)
copyImage=PhotoImage(file="copy.png")
editmenu.add_command(label="Copy", accelerator="Command+C",image=copyImage,compound=LEFT)
pasteImage=PhotoImage(file="paste.png")
editmenu.add_command(label="Paste", accelerator="Command+V",image=pasteImage,compound=LEFT)
clearImage=PhotoImage(file="clear_all.png")
editmenu.add_command(label="Clear", accelerator="Command+Option+X",image=clearImage,compound=LEFT)
findImage=PhotoImage(file="find.png")
editmenu.add_command(label="Find", accelerator="Command+F",image=findImage,compound=LEFT)

# view menu
show_toolbar=BooleanVar()
show_statusbar=BooleanVar()
statusbarImage=PhotoImage(file="status_bar.png")
toolbarImage=PhotoImage(file="tool_bar.png")
viewmenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
viewmenu.add_checkbutton(label="Tool Bar", variable=show_toolbar, onvalue=1, offvalue=0, image=toolbarImage,compound=LEFT)
viewmenu.add_checkbutton(label="Status Bar", variable=show_statusbar, onvalue=1, offvalue=0, image=statusbarImage,compound=LEFT)

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
themesmenu.add_radiobutton(label="Light Default", image=lightdImage, variable=theme_choice, compound=LEFT)
themesmenu.add_radiobutton(label="Light Plus", image=lightpImage, variable=theme_choice, compound=LEFT)
themesmenu.add_radiobutton(label="Dark", image=darkImage, variable=theme_choice, compound=LEFT)
themesmenu.add_radiobutton(label="Pink", image=pinkImage, variable=theme_choice, compound=LEFT)
themesmenu.add_radiobutton(label="Monokai", image=monokaiImage, variable=theme_choice, compound=LEFT)
themesmenu.add_radiobutton(label="Night Blue", image=nightblueImage, variable=theme_choice, compound=LEFT)

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



root.mainloop() 
