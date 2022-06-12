from tkinter import *
from dataclasses import dataclass
from PIL import ImageTk, Image
from functools import partial
import time
import threading

save_bool = False
accept_bool = False
load_bool = False
power = False
save_settings = False
fnc = False;


def getPower():
    return power

def getLoad(): return load_bool


def checkifsendFnc():
    global fnc
    fnc = True
    return fnc

def checkifaccepted():
    global accept_bool
    accept_bool = True
    return accept_bool


def checkifsaved():
    global save_bool
    save_bool = True
    return save_bool


def checkifloaded():
    global load_bool
    load_bool = True
    return load_bool

def checkifsettingsaved():
    global save_settings
    save_settings = True
    return save_settings


class LampView:
    def __init__(self, root, root_buttons, settings, calculate):
        global save_bool, accept_bool, power, save_settings
        self.settings = settings
        self.settings.readSettings()
        self.calculate = calculate
        self.root = root
        self.root_buttons = root_buttons
        self.lamp_list = []
        self.btn_list = []
        self.delete_bool = False

        self.program_list = []

        self.threads = []

        self.active_mode = 0
        self.k = 0

        self.root_buttons.grid_rowconfigure(0, weight=1)
        self.root_buttons.grid_columnconfigure([0, 1, 2], weight=1)

        self.buttons_left = Frame(self.root_buttons, width=150, height=200)
        self.buttons_center = Frame(self.root_buttons, width=150, height=200)
        self.buttons_right = Frame(self.root_buttons, width=150, height=200)

        self.buttons_left.grid(row=0, column=0, sticky='w')
        self.buttons_center.grid(row=0, column=1, sticky='ew')
        self.buttons_right.grid(row=0, column=2, sticky='e')

        save_bool = True

        img_power_off = Image.open("redpower2.png")
        resized_power_off = img_power_off.resize((100, 100), Image.ANTIALIAS)
        self.power_img_off = ImageTk.PhotoImage(resized_power_off)

        img_power_on = Image.open("greenpower2.png")
        resized_power_on = img_power_on.resize((100, 100), Image.ANTIALIAS)
        self.power_img_on = ImageTk.PhotoImage(resized_power_on)

        img_temp = Image.open("light_bulb.png")
        resized_img = img_temp.resize((50, 50), Image.ANTIALIAS)
        self.lamp_img = ImageTk.PhotoImage(resized_img)

        self.send_btn = Button(self.buttons_left, text="SEND",
                               command=partial(self.settings.sendThrotle, self.lamp_list))
        self.send_btn.grid(row=1, column=0, padx=50, pady=10)

        self.sendthread = threading.Thread(target=self.settings.sendThrotle, args=[self.lamp_list])

        self.send_fnc = Button(self.buttons_left, text="SEND FNC",
                               command=partial(self.settings.sendFnc, self.lamp_list))
        self.send_fnc.grid(row=2, column=0, padx=50, pady=(10, 25))

        self.power_btn = Button(self.buttons_center, image=self.power_img_off, highlightthickness=0, bd=0)
        self.power_btn.bind("<Button-1>", self.power_check)
        self.power_btn.grid(row=0, column=0, padx=(20, 5))

        self.cont_btn = Button(self.buttons_right, text="Continuous Mode", command=self.contMode)
        self.cont_btn.grid(row=0, column=0, padx=25, pady=(20, 10))
        self.prog_btn = Button(self.buttons_right, text="Programming Mode", command=self.progMode)
        self.prog_btn.grid(row=1, column=0, padx=25, pady=(10, 10))
        self.func_name = Entry(self.buttons_right, width=10)
        self.func_name.grid(row=2, column=0, padx=25, pady=(10, 2))
        self.func_label = Label(self.buttons_right, text="Scene name").grid(row=3, column=0, padx=25, pady=(2, 20))

        self.save_btn2 = Button(self.buttons_left, text="SAVE",
                                command=partial(self.settings.save, self.lamp_list, self.program_list,
                                                self.func_name.get(), self.active_mode))
        self.save_btn2.grid(row=0, column=0, padx=50, pady=(25, 10))
        self.rightClickMenuConfig()
        self.contMode()
        self.update()
#
    def power_check_noevent(self):
        global power
        if power == False:
            self.power_btn.config(image=self.power_img_off)

        elif power:
            self.power_btn.config(image=self.power_img_on)

    def power_check(self, event):
        global power
        if power == 0:
            power = True
            self.power_btn.config(image=self.power_img_on)

        elif power:
            power = False
            self.power_btn.config(image=self.power_img_off)

        self.settings.sendPowerCmd()

    def createView(self):
        i = 0
        j = 0
        self.settings.readSettings()
        self.lamp_list = []
        self.btn_list = []
        if len(self.settings.json_list) == 0 or self.delete_bool or getLoad():
            for widget in self.root.winfo_children():
                widget.destroy()
                self.btn_list = []
                self.rightClickMenuConfig()
                self.delete_bool = False
        for obj in self.settings.json_list:
            lamp_obj = Light(obj["Name"], obj["Address"], obj["Level"], obj["Pulse"], obj["Blink"], obj["Active"],
                             obj["PulseD"], obj["PulseS"], obj["BlinkD"], obj["FuncD"])
            self.lamp_list.append(lamp_obj)
            btn = Button(self.root, text=obj["Name"], compound="top", image=self.lamp_img)
            btn.bind("<Button-1>", self.onClick)
            btn.bind("<Button-3>",self.rightClickMenu)
            btn.grid(row=i, column=j, padx=5, pady=5)
            self.btn_list.append(btn)
            print(lamp_obj)
            i += 1
            if i > 2:
                i = 0
                j += 1
            if j > 2:
                j = 0
        self.program_list = self.lamp_list

    def checkIfChange(self):
        global save_bool, load_bool, save_settings
        self.settings.readFileToList()

        if save_bool:
            self.createView()
            save_bool = False

        if load_bool:
            self.jsonToClassList(self.settings.getProgramList())
            print("+++++++++++++++++++++++++++++=")
            print(self.program_list)
            load_bool = False

        if save_settings:
            self.settings.readSettings()
            save_settings = False

    def sendThreadThrottle(self,t):
        if not(t.is_alive()):
            t.start()
            t.join()
            #time.sleep(0.1)
        else:
            pass

    def sendThreadFnc(self,t):
        if not(t.is_alive()):
            t.start()
           # t.join()
            #time.sleep(0.1)
        else:
            pass

    def update(self):
        global power,fnc
    #    self.cleanthreads()
    #    self.power_check_noevent()
        self.checkIfChange()
        self.setLampValues()
        if power:
            self.save_btn2.configure(
                command=partial(self.settings.save, self.lamp_list, self.program_list, self.func_name.get(),
                                self.active_mode))
            if accept_bool:
                self.editList()
            if fnc:
                t2 =  threading.Thread(target=self.settings.sendFnc, args=[self.lamp_list],daemon=True)
                self.send_btn.config(command=partial(self.settings.sendThrotle, self.lamp_list))
                self.send_fnc.config(command=partial(self.sendThreadFnc,t2))
                fnc = False
            if self.active_mode == 0:
                t =  threading.Thread(target=self.settings.sendThrotle, args=[self.lamp_list],daemon=True)
                self.sendThreadThrottle(t)
                print(threading.active_count())
                # t = threading.Thread(target=self.settings.sendThrotle, args=[self.lamp_list])
                #self.threads.append(t)
        #print(threading.active_count())
        self.root.after(100, self.update)

    # def setThread(self,t):
    #     t = threading.Thread(target=self.settings.sendFnc, args=[self.program_list])
    #     t.start()

    def jsonToClassList(self, json_fnc):
        i = 0
        self.settings.json_list = json_fnc
        self.createView()
        for obj in json_fnc:
            lamp_obj = Light(obj["Name"], obj["Address"], obj["Level"], obj["Pulse"], obj["Blink"], obj["Active"],
                             obj["PulseD"], obj["PulseS"], obj["BlinkD"], obj["FuncD"])
            self.program_list[i] = lamp_obj
            i += 1

    # def cleanthreads(self):
    #     if self.active_mode and (len(self.threads) > 0):
    #         for thread in self.threads:
    #             thread.terminate()
    #     else:
    #         pass

    def onClick(self, event):
        for obj in self.lamp_list:
            if (obj.Name == event.widget['text']) and (obj.Active == False) and (self.k < 127):
                obj.Active = True
                event.widget.config(bg='yellow')
               # self.btn_list.append(event.widget)
                self.k += 1
                break
            elif (obj.Name == event.widget['text']) and (obj.Active == True):
                obj.Active = False
                event.widget.config(bg='SystemButtonFace')
                self.k -= 1

    def deleteLamp(self,event_text):
        k=0
        j=0
        for obj in self.lamp_list:
            if obj.Name == event_text:
                self.lamp_list.pop(k)
            k+=1

        self.settings.saveToFileReduced(self.lamp_list)
        self.delete_bool = True
    def editClick(self,event_text):
        for obj in self.lamp_list:
            if(obj.Name == event_text):
                self.editWindowConfig(obj)
                self.save_btn_edit_lamp.config(command=partial(self.editLamp,obj))

        if save_bool:
            self.top.destroy()
            self.top.update()


    def editWindowConfig(self,lamp):
        self.top = Toplevel()
        self.top.attributes('-topmost', 'true')
        self.e_address = Entry(self.top, width=30)
        self.temp = Entry(self.top, width=30)
        self.top.title("Edit light")

        self.e_address.insert(0, str(lamp.Address))

        label_address = Label(self.top, text="Address:  ").grid(row=1, column=0, padx=10, pady=10)
        self.e_address.grid(row=1, column=1, padx=10, pady=10)


        self.save_btn_edit_lamp = Button(self.top, text="SAVE",command=partial(self.editLamp, lamp))
        self.save_btn_edit_lamp.grid(row=3,column=0,padx=10, pady=10)

    def rightClickMenuConfig(self):
        self.m = Menu(self.root,tearoff=0)
        self.m.add_command(label="Edit")
        self.m.add_command(label="Delete")

    def rightClickMenu(self,event):
        try:
            self.m.tk_popup(event.x_root,event.y_root)
        finally:
            self.m.grab_release()
            self.m.entryconfig(0, command=partial(self.editClick, event.widget['text']))
            self.m.entryconfig(1,command=partial(self.deleteLamp,event.widget['text']))

    def editLamp(self,lamp):
        k = 0
        for obj in self.lamp_list:
            if obj.Name == lamp.Name:
                self.settings.sendAddrConfig(self.lamp_list[k].Address,self.e_address.get())
                self.lamp_list[k].Address = self.e_address.get()
            k += 1
        self.settings.saveToFileActive(self.lamp_list)
        self.top.destroy()
        self.top.update()

    def setLampValues(self):
        for obj in self.lamp_list:
            if obj.Active:
                obj.Level = self.calculate.giveValue(1)

    def progMode(self):
        self.clearActives()
        self.active_mode = 1
        self.k = 126
        self.prog_btn.config(bg='green')
        self.cont_btn.config(bg='SystemButtonFace')

    def contMode(self):
        self.clearActives()
        self.active_mode = 0
        self.k = 0
        self.cont_btn.config(bg='green')
        self.prog_btn.config(bg='SystemButtonFace')

    def clearActives(self):
        for obj in self.lamp_list:
            obj.Active = False

        for obj in self.btn_list:
            obj.config(bg='SystemButtonFace')



    def editList(self):
        k = 0
        j = 0
        for obj in self.lamp_list:
            if obj.Active:
                temp_lamp = self.checkMode(obj)
                self.lamp_list[k] = temp_lamp
                if self.lamp_list[j].Address == self.program_list[j].Address:
                    self.program_list = self.swap(self.lamp_list, k, j)
                    j += 1
            else:
                pass
            k += 1

    def checkMode(self, lamp):
        global accept_bool
        if self.active_mode and accept_bool and lamp.Active:
            if self.calculate.getPulseMode():
                lamp.Pulse = True
                lamp.Blink = False
                lamp.PulseD = self.calculate.givePDvalue()
                lamp.PulseS = self.calculate.givePSvalue()
                if (self.calculate.giveFDvalue() == "setdef"):
                    lamp.FuncD = 0
                    pass
                else:
                    lamp.FuncD = self.calculate.giveFDvalue()
            elif self.calculate.getBlinkMode():
                lamp.Blink = True
                lamp.Pulse = False
                lamp.BlinkD = self.calculate.giveBDvalue()
                if (self.calculate.giveFDvalue() == "setdef"):
                    lamp.FuncD = 0
                    pass
                else:
                    lamp.FuncD = self.calculate.giveFDvalue()
        accept_bool = False
        return lamp

    def swap(self, lamp_list, pos1, pos2):
        lamp_list[pos1], lamp_list[pos2] = lamp_list[pos2], lamp_list[pos1]
        return lamp_list


@dataclass
class Light:
    Name: str = 'default'
    Address: int = 3
    Level: int = 0
    Pulse: bool = False
    Blink: bool = False
    Active: bool = False
    PulseD: int = 30
    PulseS: int = 1
    BlinkD: int = 5  # 5*100=500 ms
    FuncD: int = 0
