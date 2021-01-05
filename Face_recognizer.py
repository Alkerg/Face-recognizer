import cv2
import os
import imutils
import time
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from whatsapp import enviar_whatsapp,countW

#------------------CREATION OF THE PATH TO COLLECT INFORMATION AND VARIABLES----------------------
# Change to the name of the person to recognize
personName = "User"
# Change to the path where you have stored Data
dataPath = os.getcwd()
dataPathData = os.getcwd() + "\\" + "data"
personPath = dataPath + "\\" + "data" '\\' + personName

# Variables for training
peopleList = os.listdir(dataPathData)
labels = []
facesData = []
label = 0

# Variables for facial recognition
imagePaths = os.listdir(dataPathData)
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# If the folder does not exist, it is created
if not os.path.exists(personPath):
	print('Carpeta creada: ',personPath)
	os.makedirs(personPath)

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# Launch the Haarcascades face detector
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
count = 0
mostrar_solo_imagen = True
reconocer_cara = False
numeroTelefono = ""

#------------------ACTION FUNCTIONS ON THE RECOGNITION BUTTON AND BUTTON TO ACTIVATE RECOGNITION----------------------
def boton_captura():
    global mostrar_solo_imagen
    mostrar_solo_imagen = False

def boton_reconocimiento():
    global reconocer_cara
    global mostrar_solo_imagen
    mostrar_solo_imagen = False
    reconocer_cara = True
    
#------------------FUNCTION THAT UPDATES THE PHONE NUMBER----------------------
def boton_aceptar():
    global numeroTelefono
    numeroNuevo = entryNumero.get()
    numeroTelefono = numeroNuevo

#------------------FUNCTION TO DETECT FACE WITH GREEN FRAME----------------------
def detectar_cara(img):
    faces = faceClassif.detectMultiScale(img, 1.2, 5)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#------------------FUNCTION TO RECOGNIZE A PERSON AND SHOW THEIR NAME IN A BOX----------------------
def reconocer_con_nombre(img,faces,result):
    countW = 0
    for (x, y, w, h) in faces:
        if result[1] < 70:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
            enviar_whatsapp(imagePaths[result[0]],numeroTelefono)
        else:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img,'Desconocido'.format(imagePaths[result[0]]),(x,y-20),2,1.1,(255,0,0),1,cv2.LINE_AA)

#------------------FUNCTION THAT SHOWS THE FACE TRACKING ON THE SCREEN AND SAVES THE PHOTOS----------------------
def captura_rostro_guarda():
    global mostrar_solo_imagen
    global count
    # Read every frame of the video
    ret,frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Resize each frame
    frame =  imutils.resize(frame, width=640)
    # Turns them to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()	
    faces = faceClassif.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        # Draw the rectangle around the face
        detectar_cara(rgb)
        rostro = auxFrame[y:y+h ,x:x+w]
        # We will store all faces of the same size
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(personPath + '/rostro_{}.jpg'.format(count),rostro)
        count = count + 1
        if count >= 200:
            mostrar_solo_imagen = True
            lframe.after(10,mostrar_en_lframe)
            return
    # Show what the camera captures on screen
    prevImg = Image.fromarray(rgb)
    imgTk = ImageTk.PhotoImage(image = prevImg)
    lframe.imgTk = imgTk
    lframe.configure(image = imgTk)
    lframe.after(10,captura_rostro_guarda)

#------------------FUNCTION THAT TRAINS AND CREATES A PREDICTION MODEL----------------------
def entrenar_modelo():
    global label
    global labels
    global face_recognizer
    progresCount = 0
    barraProgreso = ttk.Progressbar(root, orient = HORIZONTAL, length = 200, mode = "determinate")
    barraProgreso.place(x = 250, y = 45)

    progresoLabel = Label(root,text = "")
    progresoLabel.place(x = 335, y = 70)

    for nameDir in peopleList:
        personPath = dataPathData + '/' + nameDir
        print('Leyendo las imágenes')
        for fileName in os.listdir(personPath):
            print('Rostros: ', nameDir + '/' + fileName)
            labels.append(label)
            facesData.append(cv2.imread(personPath + '/' + fileName, 0))

            barraProgreso["value"] = int((progresCount/200) * 100)
            root.update_idletasks()
            progresoLabel.config(text = str(barraProgreso["value"]) + "%")
            time.sleep(0.02)
            progresCount += 1

        label = label + 1

    # Method to train the recognizer
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # Entrenando el reconocedor de rostros
    print("Entrenando...")
    face_recognizer.train(facesData, np.array(labels))

    root.update_idletasks()
    progresoLabel.config(text = "Entrenamiento completado")
    progresoLabel.place(x = 270, y =70)
    root.update_idletasks()
    time.sleep(0.02)

    # Storing the obtained model
    face_recognizer.write('modeloLBPHFace.xml')
    print("Modelo almacenado! :)") 
    barraProgreso.destroy()
    progresoLabel.destroy()

    face_recognizer.read('modeloLBPHFace.xml')
    print("Modelo leido")

#------------------FUNCTION THAT SHOWS THE RECOGNITION OF THE PERSON ON THE SCREEN----------------------
def reconocimiento_facial():
    global reconocer_cara
    global imagePaths
    ret,frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy() 
    faces = faceClassif.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces: 
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro) 

        reconocer_con_nombre(rgb,faces,result) 

    prevImg = Image.fromarray(rgb)
    imgTk = ImageTk.PhotoImage(image = prevImg)
    lframe.imgTk = imgTk
    lframe.configure(image = imgTk)
    lframe.after(10,reconocimiento_facial)

#------------------FUNCTION THAT SHOWS WHAT THE CAMERA IS JUST CAPTURING----------------------
def mostrar_en_lframe():
    ret,frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    prevImg = Image.fromarray(rgb)
    imgTk = ImageTk.PhotoImage(image = prevImg)
    lframe.imgTk = imgTk
    lframe.configure(image = imgTk)   

    if mostrar_solo_imagen:
        lframe.after(10,mostrar_en_lframe) # Show the camera in the interface
    elif reconocer_cara:
        reconocimiento_facial() # Facial recognition
    else:
        captura_rostro_guarda() # Capture photos

#------------------GRAPHIC INTERFACE----------------------
root = Tk()
root.title("FACE RECOGNIZER")
root.geometry("680x680")
root.resizable(0,0)
root.config(bg = "#035E7B")
root.iconbitmap("icon.ico")

titleFrame = Label(root, text = "RECONOCIMIENTO FACIAL", font = ("Bauhaus 93",18), bg ="#002E2C", fg = "#EFF1C5", pady = 5).pack(side = TOP,fill=BOTH)

lframe = Label(root)
lframe.pack()

textoLabel = Label(root,text = "Numero de WhatsApp:", font = ("Bahnschrift bold",10), bg ="#035E7B", fg = "White")
textoLabel.place(x = 20, y = 530)

entryNumero = Entry(root)
entryNumero.place(x = 20, y = 560)

botonAceptar = Button(root,text = "Aceptar", width = 7, bg = "#EFF1C5",font = ("Bahnschrift",10),
                    fg = "#464932", activebackground = "#E3E79C", height = 1, command = boton_aceptar)
botonAceptar.place(x = 55, y = 590)


botonCaptura = Button(root,text = "Captura de rostros", width = 30, bg = "#EFF1C5",font = ("Bahnschrift",10),
                    fg = "#464932", activebackground = "#E3E79C", height = 2,  command = boton_captura).pack()

botonEntrenamiento = Button(root,text = "Entrenamiento", width = 30, bg = "#EFF1C5",font = ("Bahnschrift",10),
                    fg = "#464932", activebackground = "#E3E79C", height = 2, command = entrenar_modelo).pack()

botonRecnocimiento = Button(root,text = "Reconocimiento de rostros", width = 30, bg = "#EFF1C5",font = ("Bahnschrift",10),
                    fg = "#464932", activebackground = "#E3E79C",height = 2, command = boton_reconocimiento).pack()

mostrar_en_lframe()

root.mainloop()



