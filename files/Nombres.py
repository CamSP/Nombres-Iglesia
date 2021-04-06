"""
Created on Sun Dec 20 22:35:17 2020

@author: Camilo
"""
from PIL import Image as im, ImageDraw, ImageFont, ImageTk
import PIL.Image
from tkinter import *
from tkinter import filedialog
from pathlib import Path
from aerender import AERenderWrapper
import json
import threading
import os

global prev
global adv
global botonExport



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def preview(*args):

    fnt = ImageFont.truetype(resource_path('MinionPro-Regular.otf'), size = 60)
    letrero = txt.get()
    end = fnt.getmask(letrero).getbbox()[2] 
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo2.png') 
    logo = PIL.Image.open(path)

    if end <= 1600:
        tipo = 0
        end = fnt.getmask(letrero).getbbox()[2]  
        
    else:
        tipo = 1
        mid = int(len(letrero)/2)
        for i in range(mid):
            if letrero[mid+i] == " ":
                letrero1 = letrero[:mid+i]
                letrero2 = letrero[mid+i+1:]
                if fnt.getmask(letrero1).getbbox()[2] > fnt.getmask(letrero2).getbbox()[2]:
                    break
        end = fnt.getmask(letrero1).getbbox()[2]  
          
    if tipo == 0:
        img = im.new('RGBA', (end + 168, 112), (255, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        d.rectangle(((0, 16), (end+112, 97)), fill = "white")
        d.text((38, 75), letrero, font=fnt, fill='black', anchor = 'ls', align='left')

        logo = logo.resize((112,112))
        d.ellipse(((end + 56 , 0), (end+ 56 +112, 112)), fill = "white")
        img.paste(logo, (end + 56, 0), logo)
        
    else:
        img = im.new('RGBA', (end + 195, 130), (255, 0, 0, 0))
        logo = logo.resize((130,130))
        d = ImageDraw.Draw(img)
        d.rectangle(((0, 0), (end+130, 130)), fill = "white")
        d.text((38, 50), letrero1, font=fnt, fill='black', anchor = 'ls',align='left')
        d.text((38, 112), letrero2, font=fnt, fill='black', anchor = 'ls',align='left')
        d.ellipse(((end + 65 , 0), (end+ 65 +130, 130)), fill = "white")
        img.paste(logo, (end + 65, 0), logo)
    
    photo = ImageTk.PhotoImage(img)
    prev.config(image = photo)
    prev.image = photo
    
    if(img.size[0]>1920):
        adv.config(text = "Limite de caracteres recomendados excedido")
    else:
        adv.config(text = "")

    return img


def anim(path, text):
    
    rendering.config(text = "Renderizando...")
    botonExport.grid_forget()
    with open("E:\\Iglesia\\Nombres\\nombreAE.json", "r") as f:
        data = json.load(f)
        data["nombre"] = {"name":txt.get()}

    
    with open("E:\\Iglesia\\Nombres\\nombreAE.json", "w") as f:
        json.dump(data, f) 
   
    os.chdir('C:\\Program Files\\Adobe\\Adobe After Effects 2020\\Support Files')
    os.system('aerender.exe -project "E:\\Iglesia\\Nombres\\Texto.aep" -comp "Iglesia_Prueba" -RStemplate "Configuración óptima"  -OMtemplate "Sin pérdida" -output ' + path + '\\' + text + '.avi')
    rendering.config(text = "Render finalizado.")
    botonExport.grid(row=3, column=0)

def creador(*args):
    imagen = preview()
    if imagen.width > 1920:
        img = im.new('RGBA', (imagen.width, 1080), (255, 0, 0, 0))
    else:
        img = im.new('RGBA', (1920, 1080), (255, 0, 0, 0))
        
    img.paste(imagen, (0,  1080-162), imagen)
  

    path = filedialog.askdirectory()
    img.save(path + '/' + txt.get() + '.png')

    t = threading.Thread(target = anim, args= (path, txt.get()), daemon=True)
    t.start()

            
    
    
raiz = Tk()
raiz.title('Nombres y titulos')
miFrame = Frame(raiz)
miFrame.pack(fill='both', expand='true')
nombre = Label(miFrame, text='Nombre/Titulo:', font=('arial', 15))
nombre.grid(row=0, column=0, sticky='w', pady=5, padx=5)
letras = Label(miFrame, text='Previsualización:', font=('arial', 15))
letras.grid(row=1, column=0, sticky='n', pady=5, padx=5)

txt = StringVar()
txt.trace("w", preview)


entNombre = Entry(miFrame, textvariable = txt)
entNombre.grid(row=0, column=1, sticky='w', pady=5, padx=5, ipadx=60)


prev = Label(miFrame)
prev.grid(row = 2, column = 1, sticky = 'w', pady = 5, padx = 5)

adv = Label(miFrame, font=('arial', 15))
adv.grid(row=3, column=1, sticky='n', pady=5, padx=5)
 
rendering = Label(miFrame, font=('arial', 15))
rendering.grid(row=4, column=1, sticky='n', pady=5, padx=5)


botonExport = Button(miFrame, text='Exportar', command=creador)
botonExport.grid(row=3, column=0)
raiz.mainloop()
