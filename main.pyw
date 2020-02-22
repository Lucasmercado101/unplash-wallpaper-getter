# set a random image from unsplash as a wallpaper
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from customTk import *
import ctypes
import datetime
import requests
import re, os

def getTimeStamp():
    dateToday = datetime.datetime.today()
    today = str(datetime.date.today())
    hour = str(dateToday.hour)
    sec = str(dateToday.second)
    return f'{today} {hour} - {sec}'

class RootWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.defaultPath = os.path.realpath(__file__)   
        self.defaultPath, _  = os.path.split(self.defaultPath)
        self.defaultPath += r'/wallpaper '
        self.savePath = self.defaultPath

        self.resizable(False, False)
        self.width, self.height = self.getScreenResolution()

        self.defaultResolution = tk.IntVar()
        self.defaultResolution.set(1)

        self.randomImgVar = tk.IntVar()
        self.randomImgVar.set(1)

        self.mainFont = Font(family='Calibre', size=11)
        self.configure(background=COLORS['Not quite black'], bd=10,
                       bg=COLORS["Lighter Dark"])
        self.title('Get wallpaper from unsplash')
        self.searchBar = darkEntry(self, self.mainFont, placeholder='(random)', imgVar=self.randomImgVar)
        self.searchBar.grid(row=0, column=0, columnspan=3, pady=5, padx=5, ipadx=50)
        self.searchBar.bind('<Key>', func= lambda evt: self.getWallpaperQuery() if evt.keysym == "Return" else False)

        self.getRandom = darkButton(self, 'Get wallpaper', command=self.getWallpaperQuery, font=self.mainFont)
        self.getRandom.grid(row=1, column=1, pady=5)    

        self.resolutionCheckbutton = darkCheckbutton(self, f'Default resolution ({self.width}x{self.height})', 
            variable=self.defaultResolution,
            command=self.changeResolution)
        self.resolutionCheckbutton.grid(row=0, column=4)

        self.randomImg = darkCheckbutton(self, text="Random image", variable=self.randomImgVar, command= self.defRandomImage)
        self.randomImg.grid(row=1, column=4)

        self.weekly = darkButton(self, text='Get weekly', command=self.getWeekly, font=self.mainFont)
        self.weekly.grid(row=1, column=0, padx=7)

        self.daily = darkButton(self, text='Get daily', command=self.getDaily, font=self.mainFont)
        self.daily.grid(row=1, column=3, padx=7)
        
        self.outFolder = darkButton(self, 'Save to folder...', command=self.outputFolder, font=self.mainFont)
        self.outFolder.grid(column=1, row=4, padx=7, columnspan=3)

    def outputFolder(self):
        folder = filedialog.askdirectory()
        if folder:
            folder += r'/wallpaper '
            self.savePath = folder

    def getWallpaper(self, url):
        unsplash = r'https://source.unsplash.com/' + url
        r = requests.get(unsplash)
        print(r.status_code)
        if not r:
            messagebox.showerror("Error", "An error has occurred.")
            return

        timeStamp = getTimeStamp()
        fullPath = f'{self.savePath} {timeStamp}.bmp'

        with open(fullPath,'wb') as f: 
            f.write(r.content) 

        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, fullPath , 0)

    def changeResolution(self):
        self.defaultResolution.set(0)
        resolutionWin = customResolutionWindow(self, self.mainFont)
        self.wait_window(resolutionWin)

    def getScreenResolution(self):
        user32 = ctypes.windll.user32
        width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return width, height
    
    def getWallpaperQuery(self):
        resolution = f'{self.width}x{self.height}'
        randomImage = self.randomImgVar.get() == 1
        if randomImage:
            search =  rf'random/{resolution}'
            self.getWallpaper(search)
        else:
            keywords = ''
            words = self.searchBar.get()
            words = words.strip()
            words = re.sub(' +', ' ', words)
            split = words.split(' ')
            split2 = words.split(',')
            if len(split) >= len(split2):
                keywords = split
            else:
                keywords = split2

            if len(keywords) > 2:
                messagebox.showerror("Error",'Maximum 2 keywords, you entered ' + str(len(split)))
                return

            wallpaperQuery = rf'featured/{resolution}/?{keywords[0]}'
            if len(keywords) == 2:
                wallpaperQuery + f',{keywords[1]}'

            self.getWallpaper(wallpaperQuery)
         
    def defRandomImage(self):
        randomImage = self.randomImgVar.get() == 0
        if randomImage:
            self.searchBar.delete(0, tk.END)
        else:
            self.searchBar.delete(0, tk.END)
            self.searchBar.placeHolderText("FocusOut event")
            self.randomImg.focus_force()
            # self.searchBar.insert(0, '(random)')
    
    def getWeekly(self):
        resolution = f'{self.width}x{self.height}'
        randomImage = self.randomImgVar.get() == 1
        if randomImage:
            query = ""
        else:
            query = self.searchBar.get()
        weekly = rf'{resolution}/weekly?{query}' 
        self.getWallpaper(weekly)
    
    def getDaily(self):
        resolution = f'{self.width}x{self.height}'
        randomImage = self.randomImgVar.get() == 0
        if randomImage:
            query = self.searchBar.get()
        else:
            query = ""
        weekly = rf'{resolution}/daily?{query}' 
        self.getWallpaper(weekly)
        

class customResolutionWindow(tk.Toplevel):

    def __init__(self, root, font):
        tk.Toplevel.__init__(self, root)
        self.wm_geometry("250x75")
        self.mainFont = font
        self.resizable(False, False)
        self.mainWin = root
        self.transient(root)
        self.grab_set()
        self.title('Set resolution')

        self.configure(background=COLORS['Not quite black'], bd=10,
                       bg=COLORS["Lighter Dark"])

        self.widthEntry = darkEntry(self, font=self.mainFont)
        self.widthEntry.place(relx=0, relwidth=0.45)

        self.x = darkText(self, "x", font=self.mainFont, bg=COLORS["Lighter Dark"])
        self.x.place(relx=0.49)

        self.heightEntry = darkEntry(self, font=self.mainFont)
        self.heightEntry.place(relx=0.58, relwidth=0.43)
        self.heightEntry.bind('<Key>', func= lambda evt: self.confirmRes() if evt.keysym == "Return" else False)

        self.confirm = darkButton(self, "Confirm", command=self.confirmRes, font=self.mainFont, anchor='n')
        self.confirm.place(relx=0.38, relwidth=0.25, rely=0.6)

        self.protocol("WM_DELETE_WINDOW", self.setDefault) 

    def confirmRes(self):
        try:
            width = int(self.widthEntry.get())
            height = int(self.heightEntry.get())
        except:
            return
        if width > 1 and height > 1:
            self.mainWin.width = width
            self.mainWin.height = height
            self.mainWin.resolutionCheckbutton.changeText(f'Custom resolution ({self.widthEntry.get()}x{self.heightEntry.get()})')
            self.destroy()

    def setDefault(self):
        self.width, self.height = self.mainWin.getScreenResolution()
        self.mainWin.defaultResolution.set(1)
        self.mainWin.width = self.width
        self.mainWin.height = self.height
        self.mainWin.resolutionCheckbutton.changeText(f'Default resolution ({self.width}x{self.height})')
        self.destroy()

mainWindow = RootWindow()
mainWindow.mainloop()
