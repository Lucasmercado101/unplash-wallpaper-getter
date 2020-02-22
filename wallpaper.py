# set a random image from unsplash as a wallpaper
import ctypes
import datetime
import requests

def getTimeStamp():
    dateToday = datetime.datetime.today()
    today = str(datetime.date.today())
    hour = str(dateToday.hour)
    sec = str(dateToday.second)
    return f'{today} {hour} - {sec}'

def getWallpaper(url):
    unsplash = r'https://source.unsplash.com/' + url
    # daily
    # weekly
    # featured/
    # all those + ?{KEYWORD},{KEYWORD} or resolution
    r = requests.get(unsplash)
    
    timeStamp = getTimeStamp()

    savePath = r'G:\BACKUP\JOHNGM\Desktop\Games\Temp & trash\python wp\python_logo'

    fullPath = f'{savePath} {timeStamp}.bmp'

    with open(fullPath,'wb') as f: 
        f.write(r.content) 

    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, fullPath , 0)