from tkinter import *
from functools import partial
import tkinter.ttk as ttk

import serial.tools.list_ports
from tkinter import filedialog


class NavBar:
    def __init__(self, root, settings):
        self.settings = settings
        self.root = root
        self.my_menu = Menu(self.root)
        root.config(menu=self.my_menu)
        self.settings_menu = Menu(self.my_menu)
        self.file_menu = Menu(self.my_menu)
        self.file_fnc_name = ""

        self.configWidgets_Settings()
        self.configWidgets_File()

    def add_obj(self):
        self.configWidgets_AddObj()

    def edit_settings(self):
        self.configSettings_Edit()

    def empty_btn(self):
        pass

    def uptade_settings_entries(self):
        temp_fn = self.e_filename.get()
        temp_comport = self.e_comports.get()
        temp_baudrate = self.e_baudrate.get()
        temp_ip = self.e_ipaddress.get()
        self.settings.saveSettings(temp_fn,temp_comport,temp_baudrate,temp_ip)

    def configWidgets_Settings(self):
        self.my_menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Add object...", command=self.add_obj)
        self.settings_menu.add_command(label="Edit settings", command=self.edit_settings)

    def load_fnc(self):
        self.configWidgets_LoadFnc()

    def configWidgets_File(self):
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load File", command=self.load_fnc)

    def configSettings_Edit(self):
        self.top = Toplevel()
        self.top.attributes('-topmost', 'true')
        self.e_filename = Entry(self.top, width=30)
        self.e_ipaddress = Entry(self.top, width=30)
        self.e_baudrate = Entry(self.top, width=30)
        self.e_comports = ttk.Combobox(self.top, values=self.get_serialports(), width=30)

        self.top.title("Add light")

        label_name = Label(self.top, text="Main file name:  ").grid(row=0, column=0, padx=10, pady=10)
        self.e_filename.grid(row=0, column=1, padx=10, pady=10)
        self.e_filename.insert(0, self.settings.filename)

        label_name = Label(self.top, text="COM Port: ").grid(row=1, column=0, padx=10, pady=10)
        self.e_comports.grid(row=1, column=1, padx=10, pady=10)
        self.e_comports.insert(0, self.settings.port)

        label_name = Label(self.top, text="Baud rate: ").grid(row=2, column=0, padx=10, pady=10)
        self.e_baudrate.grid(row=2, column=1, padx=10, pady=10)
        self.e_baudrate.insert(0, self.settings.baudrate)

        label_name = Label(self.top, text="IP Address: ").grid(row=3, column=0, padx=10, pady=10)
        self.e_ipaddress.grid(row=3, column=1, padx=10, pady=10)
        self.e_ipaddress.insert(0, self.settings.ip)

        self.save_settings_btn = Button(self.top, text="SAVE", command=self.uptade_settings_entries)
        self.save_settings_btn.grid(row=4, column=1, padx=10, pady=10)

    def get_serialports(self):
        return serial.tools.list_ports.comports()

    def combobox_event(self, event=None):
        print("Event widget: ", event.widget.get())

    def configWidgets_LoadFnc(self):
        self.top = Toplevel()
        self.top.attributes('-topmost', 'true')
        self.top.title("Load Function")
        self.e_fncfile = Entry(self.top, width=30)
        self.e_fncfile.grid(row=0, column=1)
        self.label = Label(self.top, text="File name: ").grid(row=0, column=0)

        self.dir_btn = Button(self.top, text="...", width=2, height=1, command=self.choose_path)
        self.dir_btn.grid(row=0, column=2)

        self.load_btn = Button(self.top, text="LOAD", command=partial(self.settings.loadFunction, self.file_fnc_name))
        self.load_btn.grid(row=1, column=0)

    def choose_path(self):
        self.file_fnc_name = filedialog.askopenfilename(initialdir=self.settings.fnc_dir,
                                                        title="Select file",
                                                        filetypes=(("*.json", "*.json"), ("all files", "*.*")))
        temp_split_str = self.settings.fnc_dir.split('\\')
        temp_str = temp_split_str[-1]
        for x in temp_split_str:
            print(x)
        self.e_fncfile.insert(0, self.file_fnc_name[self.file_fnc_name.rfind(temp_str) + 1 + len(temp_str):])
        self.load_btn.config(command=partial(self.settings.loadFunction, self.file_fnc_name))

    def configWidgets_AddObj(self):
        self.top = Toplevel()
        self.top.attributes('-topmost', 'true')
        self.e_address = Entry(self.top, width=30)
        self.e_name = Entry(self.top, width=30)
        self.temp = Entry(self.top, width=30)
        self.top.title("Add light")

        label_name = Label(self.top, text="Name:  ").grid(row=0, column=0, padx=10, pady=10)
        self.e_name.grid(row=0, column=1, padx=10, pady=10)

        label_address = Label(self.top, text="Address:  ").grid(row=1, column=0, padx=10, pady=10)
        self.e_address.grid(row=1, column=1, padx=10, pady=10)

        label_temp = Label(self.top, text="Temp:  ").grid(row=2, column=0, padx=10, pady=10)
        self.temp.grid(row=2, column=1, padx=10, pady=10)

        self.save_btn = Button(self.top, text="SAVE",
                               command=partial(self.settings.saveToFile, self.e_name, self.e_address)).grid(row=3,column=0,padx=10,pady=10)
        self.read_btn = Button(self.top, text="READ", command=self.settings.readFile).grid(row=3, column=1, padx=10,pady=10)
        self.delete_btn = Button(self.top, text="DELETE", command=self.settings.deleteFile).grid(row=3, column=2,padx=10,pady=10)
