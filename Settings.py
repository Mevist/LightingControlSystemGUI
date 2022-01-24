from dataclasses import dataclass
from functools import partial
from tkinter import messagebox
from tkinter import *
import json
import os
import serial
import time
from LampView import *


##Stores default settings and define read write methods for files##
@dataclass
class Settings:
    filename: str = "testjson.json"
    ip: str = "192.168.1.1"
    port : str = 'COM7'
    baudrate: int = 115200
    timeout: float = .1
    fnc_dir: str = os.getcwd()


    json_list = []
    json_file = 0
    json_fnc = []

    port_flag = False
    arduino = serial.Serial(port,baudrate,timeout = timeout,write_timeout=5)

    def getProgramList(self):
        self.loadFunction(self.fnc_dir)
        return self.json_fnc

    def connecToPort(self):
        try:
            self.arduino.port = self.port
            self.arduino.baudrate = self.baudrate
            self.arduino.timeout = self.timeout
            self.arduino.open()
        except Exception as e:
            print(e)
            messagebox.showinfo("Error","Invalid port")
            self.port_flag = True

    def loadFunction(self,filedir):
        if filedir != "":
            self.fnc_dir = filedir
            try:
                with open(self.fnc_dir,'r') as f:
                    self.json_fnc = json.loads(f.read())
            except Exception as e:
                print(e)
            checkifloaded()

    def sendPowerCmd(self):
        # if not self.arduino.isOpen():
        #     self.connecToPort()

        if getPower():
            self.arduino.write(bytes("<1>", 'utf-8'))
        elif getPower() == False:
            self.arduino.write(bytes("<->",'utf-8'))
            self.arduino.write(bytes("<0>",'utf-8'))

    def sendThrotle(self,lamp_list):
        # if not self.port_flag:
        #     if not self.arduino.isOpen():
        #         self.connecToPort()

        if getPower():
                i=0
                for obj in lamp_list:
                    templevel = str(self.convertLevel(obj.Level))
                    tempdir = str(self.checkLevel(obj.Level))
                    cmd = "<t 1 " + str(obj.Address) + " " + templevel + " " + tempdir + ">"
                    i+=1
                    self.arduino.flushInput()
                    self.arduino.flushOutput()
                    self.arduino.write(bytes(cmd, 'utf-8'))
                    time.sleep(0.01)

    def sendCmd(self,lamp_list):
        # if not self.arduino.isOpen():
        #     self.connecToPort()

        if getPower():
            for x in range(1,3):
                self.arduino.write(bytes("<->", 'utf-8'))
            for obj in lamp_list:
                self.arduino.flushInput()
                self.arduino.flushOutput()
                if obj.Pulse:
                    cmd_conf = "<w " + str(obj.Address) + " 113 " + str(obj.PulseD) + ">"
                    self.arduino.write(bytes(cmd_conf, 'utf-8'))
                    cmd_conf2 = "<w " + str(obj.Address) + " 114 " + str(obj.PulseS) + ">"
                    self.arduino.flushInput()
                    self.arduino.flushOutput()
                    self.arduino.write(bytes(cmd_conf2, 'utf-8'))
                elif obj.Blink:
                    cmd_conf = "<w " + str(obj.Address) + " 115 " + str(obj.BlinkD) + ">"
                    self.arduino.write(bytes(cmd_conf, 'utf-8'))

    def sendFnc(self,lamp_list):
        # if not self.arduino.isOpen():
        #     self.connecToPort()
        checkifsendFnc()
        if getPower():
            self.sendCmd(lamp_list)
            for obj in reversed(lamp_list):
                time.sleep(obj.FuncD)
                self.arduino.flushInput()
                self.arduino.flushOutput()
                if  obj.Pulse:
                    cmd = "<F " + str(obj.Address) + " 1 1>"
                    self.arduino.write(bytes(cmd, 'utf-8'))
                elif obj.Blink:
                    cmd = "<F " + str(obj.Address) + " 2 1>"
                    self.arduino.write(bytes(cmd, 'utf-8'))
                else:
                    templevel = str(self.convertLevel(obj.Level))
                    tempdir = str(self.checkLevel(obj.Level))
                    cmd = "<t 1 " + str(obj.Address) + " " + templevel + " " + tempdir +">"
                    self.arduino.write(bytes(cmd, 'utf-8'))

    def convertLevel(self,obj_level):
        if 0 <= obj_level <= 126:
            return obj_level
        elif 126 < obj_level <= 253:
            return obj_level - 127

    def checkLevel(self,obj_level):
        if  0 <= obj_level <= 126:
            return 0
        elif 126 < obj_level <= 253:
            return 1

    def sendAddrConfig(self,old_adr,new_adr):
        cmd = f'<w {old_adr} 1 {new_adr} >'
        self.arduino.write(bytes(cmd, 'utf-8'))

    def save(self,lamp_list,program_list,fnc_name,active_mode):
        if active_mode:
            temp_array = []
            temp_str = f'{fnc_name}.json'
            for obj in program_list:
                json_obj = {"Name": obj.Name,
                            "Address": obj.Address,
                            "Level": obj.Level,
                            "Pulse": obj.Pulse,
                            "Blink": obj.Blink,
                            "Active":obj.Active,
                            "PulseD":obj.PulseD,
                            "PulseS":obj.PulseS,
                            "BlinkD":obj.BlinkD,
                            "FuncD":obj.FuncD}
                temp_array.append(json_obj)
            with open(temp_str,'w') as f:
                y=json.dumps(temp_array)
                f.write(y)
        else:
            self.saveToFileActive(lamp_list)


    def saveSettings(self,e_filename,e_comports,e_baudrate,e_ipaddress):
        json_obj = {"File name" : e_filename,
                    "COM port" : e_comports,
                    "Baudrate" : e_baudrate,
                    "Ip address" : e_ipaddress}
        with open("Settings.json", 'w') as f:
            y=json.dumps(json_obj)
            f.write(y)
        self.readSettings()
        self.port_flag = True
        self.connecToPort()
        checkifsettingsaved()

    def readSettings(self):
        with open("Settings.json", 'r') as f:
            json_temp = json.loads(f.read())
            self.filename = json_temp["File name"]
            self.port = json_temp["COM port"]
            self.baudrate = json_temp["Baudrate"]
            self.ip = json_temp["Ip address"]


    def readFile(self):
        try:
            with open(self.filename, 'r') as f:
                json_temp = json.loads(f.read())
                for item in json_temp:
                    print(item)
        except Exception as e:
            print(e)

    def readFileToList(self):
        if getLoad():
            self.json_file = self.json_file
        else:
            try:
                with open(self.filename, 'r') as f:
                    json_temp = json.loads(f.read())
                    self.json_file = json_temp
                    self.json_list = json_temp
            except Exception as e:
                print(e)
                f = open(self.filename, 'w')
                f.close()

    def saveToFileReduced(self,lamp_list):
        temp_array = []
        for obj in lamp_list:
            json_obj = {"Name": obj.Name,
                        "Address": obj.Address,
                        "Level": obj.Level,
                        "Pulse": obj.Pulse,
                        "Blink": obj.Blink,
                        "Active": obj.Active,
                        "PulseD": obj.PulseD,
                        "PulseS": obj.PulseS,
                        "BlinkD": obj.BlinkD,
                        "FuncD": obj.FuncD}
            temp_array.append(json_obj)
        with open(self.filename, 'w') as f:
            y = json.dumps(temp_array)
            f.write(y)
        checkifsaved()


    def saveToFileActive(self,lamp_list):
        with open(self.filename) as f:
            json_temp = json.loads(f.read())
            if len(json_temp) == len(lamp_list):
                for file_obj in json_temp:
                    for var_obj in lamp_list:
                        if file_obj["Name"] == var_obj.Name:
                            file_obj["Address"] = var_obj.Address
                            file_obj["Level"] = var_obj.Level
                            file_obj["Pulse"] = var_obj.Pulse
                            file_obj["Blink"] = var_obj.Blink
                            file_obj["PulseD"] = var_obj.PulseD
                            file_obj["PulseS"] = var_obj.PulseS
                            file_obj["BlinkD"] = var_obj.BlinkD
                            y = json.dumps(json_temp)
                            with open(self.filename, 'w') as f:
                                f.write(y)
                print("----------------")

    def saveToFile(self, e_name, e_address):
        flag_name = False
        flag_address = False
        self.readFileToList()

        ##Setting up  flags##

        if len(e_name.get()) == 0:
            flag_name = True
            messagebox.showinfo("showinfo", "Blank name")

        if (self.checkId(e_address.get())):
            flag_address = True
            messagebox.showinfo("Show info", "Object address must be in range from 1 to 127")

        if isinstance(self.json_file, list):
            self.json_list = self.json_file

            for obj in self.json_file:
                if obj["Name"] == e_name.get():
                    messagebox.showinfo("show info", "Object with this name exists")
                    flag_name = True
                    break
                elif obj["Address"] == int(e_address.get()):
                    messagebox.showinfo("show info", "Object with this address exists")
                    flag_address = True
                    break
                else: pass

        if not (flag_name or flag_address):
            json_obj = {"Name": e_name.get(),
                        "Address": int(e_address.get()),
                        "Level": 0,
                        "Pulse": False,
                        "Blink": False,
                        "Active": False,
                        "PulseD": 30,
                        "PulseS": 1,
                        "BlinkD": 5,
                        "FuncD": 0}
            self.json_list.append(json_obj)
            y = json.dumps(self.json_list)
            checkifsaved()
            with open(self.filename, 'w') as f:
                f.write(y)

    def checkId(self, adr,):
        try:
            if (int(adr) >= 1 and int(adr) <= 127):
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return True

    def deleteFile(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            self.json_list = []
            self.json_file = 0
            checkifsaved()

        else:
            messagebox.showinfo("show info", "File does not exist")
