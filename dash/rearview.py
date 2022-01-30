import cv2
import threading
import tkinter as tk
from PIL import Image, ImageTk
from gps import *
import csv
from datetime import datetime
import math

cap = cv2.VideoCapture(0)
gpsd = None
header = ['time UTC','lat','lon','alt','spd m/s','spd mph']
#filename = '/home/pi/gpsdata_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv' 
filename = '/media/pi/data/gpsdata_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv' 


def rxGps():
    global gpsd
    x = 0
    gpsd = gps(mode=WATCH_ENABLE)
    while True:
       time.sleep(5)
       #  check for NaN response
       if math.isnan(gpsd.fix.latitude) or math.isnan(gpsd.fix.altitude):
            # print("no data rxd", gpsd.fix.latitude)
            gpsd.next()
       else:
            # log GPS data
            values = (gpsd.utc, gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.speed, gpsd.fix.speed * 2.237)
            print(values)
            gpsd.next()
            with open(filename, "a", encoding='UTF8', newline='') as fo:
                writer = csv.writer(fo)
                if x == 0:
                    writer.writerow(header)
                    x = 1
                writer.writerow(values)

def rearview(window,lmain):
    x = 0
    while True:
        _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.configure(image=imgtk)
        lmain.imgtk = imgtk


def main():
    window = tk.Tk()
    window.configure(width=320, height=280)
    window.attributes('-type', 'dock')
    window.config(background="#000000")
    lmain = tk.Label(window)
    lmain.place(relwidth=1.0, relheight=1.0)
    window.config(cursor="none") # disable the Mouse Pointer
    threading.Thread(target = rearview, args = {window, lmain}, daemon = True).start()
    threading.Thread(target = rxGps, daemon = True).start()
    window.mainloop()


main()

