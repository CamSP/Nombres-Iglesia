"""
Created on Sun Dec 20 22:35:17 2020

@author: Camilo
"""
from PIL import Image as im, ImageDraw, ImageFont, ImageTk
import PIL.Image
from tkinter import *
from tkinter import filedialog
from pathlib import Path

import json
import threading
import os


global prev
global adv
global botonExport


#Muestra la previsualización de la imagen de salida
def preview(*args):
    
    #Importa la fuente que se va a utilizar en la imagen
    fnt = ImageFont.truetype('MinionPro-Regular.otf', size = 60)
    #Recibe el string que se escribe en la entrada de texto
    letrero = txt.get()
    #Determina el tamaño que ocupara el texto en la imagen
    end = fnt.getmask(letrero).getbbox()[2] 
    #Se importa el logo de la iglesia
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo2.png') 
    logo = PIL.Image.open(path)

    #Si el tamaño del texto es menor a 1600px, solo se utilizará un renglon
    if end <= 1600:
        #Se crea una imagen con el tamaño que ocupa el texto + el tamaño del logo (112px) + la distancia entre el inicio de la imagen y el inicio del texto (56px)
        img = im.new('RGBA', (end + 168, 112), (255, 0, 0, 0))
        d = ImageDraw.Draw(img)
        #Se crea un rectangulo blanco y se coloca el texto
        d.rectangle(((0, 16), (end+112, 97)), fill = "white")
        d.text((38, 75), letrero, font=fnt, fill='black', anchor = 'ls', align='left')
        #Se ajusta el tamaño del logo (112px) y se dibuja una elipse blanca para que sea un background del logo
        logo = logo.resize((112,112))
        d.ellipse(((end + 56 , 0), (end+ 56 +112, 112)), fill = "white")
        #Se coloca el logo en la imagen
        img.paste(logo, (end + 56, 0), logo)

    
    #Si el tamaño del texto es mayor a 1600px, se utilizarán 2 renglones para mostrar el texto
    else:
        #Se determina la mitad del texto
        mid = int(len(letrero)/2)
        #A partir de la mitad, se cambia el primer espacio (" ") por un salto de linea ("\n")
        for i in range(mid):
            if letrero[mid+i] == " ":
                letrero1 = letrero[:mid+i]
                letrero2 = letrero[mid+i+1:]
                #Se verifica que donde se haga el salto de linea, el renglon superior sea más grande que el inferior, de lo contrario se busca el siguiente espacio (" ")
                if fnt.getmask(letrero1).getbbox()[2] > fnt.getmask(letrero2).getbbox()[2]:
                    break
        #Se obtiene el tamaño del primer renglon (el más grande), para generar el tamaño de la imagen
        end = fnt.getmask(letrero1).getbbox()[2]  
        
        #Se crea una imagen con el tamaño que ocupa el texto + el tamaño del logo (en este caso es más grande [130px]) + la distancia entre el inicio de la imagen y el inicio del texto (56px)
        img = im.new('RGBA', (end + 186 + 65, 130), (255, 0, 0, 0))
        logo = logo.resize((130,130))
        d = ImageDraw.Draw(img)
        #Se crea un rectangulo blanco y se coloca el texto
        d.rectangle(((0, 0), (end+130, 130)), fill = "white")
        d.text((38, 50), letrero1, font=fnt, fill='black', anchor = 'ls',align='left')
        d.text((38, 112), letrero2, font=fnt, fill='black', anchor = 'ls',align='left')
        #Se ajusta el tamaño del logo (130px) y se dibuja una elipse blanca para que sea un background del logo
        d.ellipse(((end + 65 , 0), (end+ 65 +130, 130)), fill = "white")
        #Se coloca el logo en la imagen
        img.paste(logo, (end + 65, 0), logo)

    #Se edita una label para mostrar la imagen
    photo = ImageTk.PhotoImage(img)
    prev.config(image = photo)
    prev.image = photo
    
    #Si el tamaño de la imagen en la horizontal es mayor a 1920px, se muestra una advertencia de la longitud del texto
    if(img.size[0]>1920):
        adv.config(text = "Limite de caracteres recomendados excedido")
    else:
        adv.config(text = "")
        
    #Se retorna la imagen generada
    return img


#Renderiza la animación realizada en After Effects
def anim(path, text):
    #Se muestra una label que advierte que se esta renderizando
    rendering.config(text = "Renderizando...")
    #Se esconde el boton de exportar para evitar que se cancele el proceso de renderizado 
    botonExport.grid_forget()
    #Edita un archivo json que lee el proyecto de after effects, edita el campo de texto
    with open("E:\\Iglesia\\Nombres\\nombreAE.json", "r") as f:
        data = json.load(f)
        data["nombre"] = {"name":txt.get()}

    
    with open("E:\\Iglesia\\Nombres\\nombreAE.json", "w") as f:
        json.dump(data, f) 
        
    #Se abre la consola de comandos de windows y se dirige al path donde esta aerender.exe
    os.chdir('C:\\Program Files\\Adobe\\Adobe After Effects 2020\\Support Files')
    #Se coloca el comando en el cmd que ejecuta el render de la animación
    os.system('aerender.exe -project "E:\\Iglesia\\Nombres\\Texto.aep" -comp "Iglesia_Prueba" -RStemplate "Configuración óptima"  -OMtemplate "Sin pérdida con alfa" -output ' + path + '\\' + text + '.avi')
    #Cuando acaba el render se cambia el estado del programa y se muestra de nuevo el boton de exportar
    rendering.config(text = "Render finalizado.")
    botonExport.grid(row=3, column=0)

#Metodo que exporta la imagen y llama al proceso de renderizado
def creador(*args):
    #Se adquiere la imagen que se muestra en la previsualización
    imagen = preview()
    #Se crea una imagen transparente de 1920x1080, pero si el tamaño de la preview es mayor, se adapta el tamaño horizontal de la imagen
    if imagen.width > 1920:
        img = im.new('RGBA', (imagen.width, 1080), (255, 0, 0, 0))
    else:
        img = im.new('RGBA', (1920, 1080), (255, 0, 0, 0))
    #Se pega la imagen de la preview en la imagen transparente creada
    img.paste(imagen, (0,  1080-162), imagen)
  
    #Se pregunta al usuario donde guardar la imagen y la animación
    path = filedialog.askdirectory()
    t = txt.get()
    print(t)
    t = t.replace(":", " - ")
    t = t.replace("?", " - ")
    t = t.replace("¿", " - ")
    t = t.replace("/", " - ")
    t = t.replace('\\', " - ")
    t = t.replace("*", " - ")
    t = t.replace("<", " - ")
    t = t.replace(">", " - ")
    t = t.replace("|", " - ")
    t = t.replace('"', " - ")
    print(t)
    #Se guarda la imagen
    img.save(path + '/' + t + '.png')
    #Se cre un hilo que renderiza la imagen, esto para que el programa no se detenga mientras se renderiza. De esta manera, el usuario puede ir preparando el sig:uiente nombre/titulo a exportar
    #t = threading.Thread(target = anim, args= (path, txt.get()), daemon=True)
    #t.start()

            
    
#Interfaz grafica
raiz = Tk()
#Titulo de la ventana
raiz.title('Nombres y titulos')
#Label que describe que va en el campo de entrada
nombre = Label(raiz, text='Nombre/Titulo:', font=('arial', 15))
nombre.grid(row=0, column=0, sticky='w', pady=5, padx=5)
#Label que explica que es la imagen que se muetra
prev = Label(raiz, text='Previsualización:', font=('arial', 15))
prev.grid(row=1, column=0, sticky='n', pady=5, padx=5)

#Creación del listener del texto de entrada
txt = StringVar()
txt.trace("w", preview)

#Campo de entrada
entNombre = Entry(raiz, textvariable = txt)
entNombre.grid(row=0, column=1, sticky='w', pady=5, padx=5, ipadx=60)

#Label que muestra la previsualización
prev = Label(raiz)
prev.grid(row = 2, column = 1, sticky = 'w', pady = 5, padx = 5)

#Advertencia de tamaño de la iamgen
adv = Label(raiz, font=('arial', 15))
adv.grid(row=3, column=1, sticky='n', pady=5, padx=5)
 
#Label que muestra si se esta renderizando
rendering = Label(raiz, font=('arial', 15))
rendering.grid(row=4, column=1, sticky='n', pady=5, padx=5)

#Botpn para exportar
botonExport = Button(raiz, text='Exportar', command=creador)
botonExport.grid(row=3, column=0)
raiz.mainloop()