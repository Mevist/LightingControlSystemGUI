from LampView import *
from tkinter import messagebox
from LampView import *

class Calculate:
    def __init__(self,root, bigroot):
        self.root = root
        self.bigroot = bigroot

        self.pulse_m = BooleanVar()
        self.pulse_btn = Checkbutton(self.root, text="Pulse", variable=self.pulse_m, onvalue=True, offvalue=False,
                                     command=self.setPulseMode)
        self.pulse_btn.deselect()
        self.pulse_btn.grid(row=0, column=0,pady=10)

        self.pulse_delay = Entry(self.root, width= 15,text="pd")
        self.pulse_delay.insert(0, "Pulse delay: ")
        self.pulse_delay.bind('<FocusIn>', self.onEntryclick)
        self.pulse_delay.bind('<FocusOut>', self.onFocusout)
        self.pulse_delay.config(fg='grey',justify = 'center')
        self.pulse_delay.grid(row=0,column=1,pady=10)

        self.pulse_step = Entry(self.root, width=15,text="ps")
        self.pulse_step.insert(0, "Pulse step: ")
        self.pulse_step.bind('<FocusIn>', self.onEntryclick)
        self.pulse_step.bind('<FocusOut>', self.onFocusout)
        self.pulse_step.config(fg='grey', justify='center')
        self.pulse_step.grid(row=1, column=1,pady=10)
#
        self.blink_m = BooleanVar()
        self.blink_btn = Checkbutton(self.root, text="Blink", variable=self.blink_m, onvalue=True, offvalue=False,
                                     command=self.setBlinkMode)
        self.blink_btn.deselect()
        self.blink_btn.grid(row=3, column=0,pady=10)

        self.blink_delay = Entry(self.root, width=15,text="bd")
        self.blink_delay.insert(0, "Blink delay: ")
        self.blink_delay.bind('<FocusIn>', self.onEntryclick)
        self.blink_delay.bind('<FocusOut>', self.onFocusout)
        self.blink_delay.config(fg='grey', justify='center')
        self.blink_delay.grid(row=3, column=1,pady=10)

        self.fnc_delay = Entry(self.root, width=15, text="fd")
        self.fnc_delay.insert(0, "Function delay: ")
        self.fnc_delay.bind('<FocusIn>', self.onEntryclick)
        self.fnc_delay.bind('<FocusOut>', self.onFocusout)
        self.fnc_delay.config(fg='grey', justify='center')
        self.fnc_delay.grid(row=4, column=1, pady=10)

        self.fnc_label = Label(self.root,text="Insert function delay")
        self.fnc_label.grid(row=4, column=0, pady=10)

        self.acceptBtn = Button(self.root, text="Accept", command = self.accept)
        self.acceptBtn.grid(row = 5, column=1)

        test_str = "0 | - | - | - | 25 | - | - | - | 50 | - | - | - | 75 | - | - | - | 100 "
        self.my_label = Label(self.root, text=test_str)
        self.my_label.grid(row=6, column=0, columnspan=2, padx=25,pady=(25,5))

        self.level = Scale(self.root, from_=0, to=253,showvalue=0, orient=HORIZONTAL,length = 250, command=self.giveValue)
        self.bigroot.bind("<MouseWheel>",self.mouseWheel)
        self.level.grid(row=7,column=0,columnspan=2,padx=25,pady=(5,5))
        self.level.set(0)

    def accept(self):
        if (self.pulse_m.get()) or (self.blink_m.get()):
            checkifaccepted()

    def giveValue(self,var):
        return self.level.get()

    def onReturn(self):
        self.root.focus_set()

    def givePDvalue(self):
        v = self.pulse_delay.get()
        try:
            v = int(v)
        except ValueError:
            if v != "\x08" and v != "":
                messagebox.showinfo("show info", "Value is not time in miliseconds")
                self.pulse_delay.delete(0, 'end')
                self.pulse_delay.insert(0,'')
                self.pulse_delay.insert(0, "Pulse delay: ")
                self.pulse_delay.config(fg='grey')
                self.onReturn()
                return 0
        if v > 0 and v < 255:
            return v
        else:
            messagebox.showinfo("show info", "Value is to high, maximum value is 255")
            self.pulse_delay.delete(0, 'end')
            self.pulse_delay.insert(0, '')
            self.pulse_delay.insert(0, "Pulse delay: ")
            self.pulse_delay.config(fg='grey')
            self.onReturn()
            return 0

    def givePSvalue(self):
        v = self.pulse_step.get()
        try:
            v = int(v)
        except ValueError:
            if v != "\x08" and v != "":
                messagebox.showinfo("show info", "Value is not time in miliseconds")
                self.pulse_step.insert(0, '')
                self.pulse_step.insert(0, "Pulse step: ")
                self.pulse_step.config(fg='grey')
                self.onReturn()
                return 0
        if v > 0 and v < 255:
            return v
        else:
            messagebox.showinfo("show info", "Value is to high, maximum value is 255")
            self.pulse_step.delete(0, 'end')
            self.pulse_step.insert(0, '')
            self.pulse_step.insert(0, "Pulse step: ")
            self.pulse_step.config(fg='grey')
            self.onReturn()
            return 0

    def giveBDvalue(self):
            v = self.blink_delay.get()
            try:
                v = int(v)
            except ValueError:
                if v != "\x08" and v != "":
                    messagebox.showinfo("show info", "Value is not time in miliseconds")
                    self.blink_delay.insert(0, '')
                    self.blink_delay.insert(0, "Blink delay: ")
                    self.blink_delay.config(fg='grey')
                    self.onReturn()
                    return 0
            if v > 0 and v < 255:
                return v
            else:
                messagebox.showinfo("show info", "Value is to high, maximum value is 255")
                self.blink_delay.delete(0, 'end')
                self.blink_delay.insert(0, '')
                self.blink_delay.insert(0, "Blink delay: ")
                self.blink_delay.config(fg='grey')
                self.onReturn()
                return 0

    def giveFDvalue(self):
        v = self.fnc_delay.get()
        try:
            v = int(v)
        except ValueError:
            if v != "\x08" and v != "":
               # messagebox.showinfo("show info", "Value is not time in miliseconds")
                messagebox.showinfo("show info", "Value not defined,setting no delay")
                self.fnc_delay.delete(0, 'end')
                self.fnc_delay.insert(0,'0')
                self.fnc_delay.insert(0, "Function delay: ")
                self.fnc_delay.config(fg='grey')
                self.onReturn()
                return "setdef"
        if v > 0 and v < 255:
            return v
        else:
            messagebox.showinfo("show info", "Value is to high, maximum value is 255")
            self.fnc_delay.delete(0, 'end')
            self.fnc_delay.insert(0, '')
            self.fnc_delay.insert(0, "Function delay: ")
            self.fnc_delay.config(fg='grey')
            self.onReturn()
            return "setdef"


    def mouseWheel(self,event):
        if event.delta == -120:
            self.level.set(self.level.get() - 1)
        elif event.delta == 120:
            self.level.set(self.level.get() + 1)

    def getPulseMode(self):
        return self.pulse_m.get()

    def setPulseMode(self):
        self.blink_btn.deselect()

    def getBlinkMode(self):
        return self.blink_m.get()

    def setBlinkMode(self):
        self.pulse_btn.deselect()


    def onEntryclick(self,event):
        if (self.pulse_delay.cget('fg') == 'grey') and (event.widget['text'] == "pd"):
            self.pulse_delay.delete(0,'end')
            self.pulse_delay.insert(0,'')
            self.pulse_delay.config(fg='black')
        elif (self.pulse_step.cget('fg') == 'grey') and (event.widget['text'] == "ps"):
            self.pulse_step.delete(0,'end')
            self.pulse_step.insert(0,'')
            self.pulse_step.config(fg='black')
        elif (self.blink_delay.cget('fg') == 'grey') and (event.widget['text'] == "bd"):
            self.blink_delay.delete(0,'end')
            self.blink_delay.insert(0,'')
            self.blink_delay.config(fg='black')
        elif (self.fnc_delay.cget('fg') == 'grey') and (event.widget['text'] == "fd"):
            self.fnc_delay.delete(0, 'end')
            self.fnc_delay.insert(0, '')
            self.fnc_delay.config(fg='black')

    def onFocusout(self,event):
        if self.pulse_delay.get() == '':
            self.pulse_delay.insert(0,"Pulse delay: ")
            self.pulse_delay.config(fg='grey')
        elif self.pulse_step.get() == '':
            self.pulse_step.insert(0,"Pulse step: ")
            self.pulse_step.config(fg='grey')
        elif self.blink_delay.get() == '':
            self.blink_delay.insert(0,"Blink delay: ")
            self.blink_delay.config(fg='grey')
        elif self.fnc_delay.get() == '':
            self.fnc_delay.insert(0,"Function delay: ")
            self.fnc_delay.config(fg='grey')
