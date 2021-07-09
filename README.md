# Face-recognizer
Description: A face recognizer made with OpenCV and Tkinter.

#Dependecies
First you must install the dependencies from the command console.
-OpenCV  -> pip install opencv-python , pip install --user opencv-contrib-python
-imutils -> pip install imutils
-numpy   -> pip install numpy
-Pillow  -> pip install Pillow

#Functioning
To use the recognizer, you must create a folder called "data" in the same directory where the files of this program are located.
Then change the variable "personName" by the name of the person to recognize.
Now, you must run the file "Face_recognizer.py" and the magic begins.
There are four buttons that you need to press in order:

1. Captura de rostros button -> It will take 200 photos of the person's face and store them in a folder with their name in the "data" directory. You can create it yourself, although the program can do it automatically if it doesn't exist.

2. Entrenamiento button -> A loading bar will appear, and both the photos of the person and the corresponding labels will be collected (this will serve to identify each person with each face). Then a model will be trained and saved in a file with the name "modeloLBPHFace.xml"

3. Reconocimiento button -> For it to work you must enter a phone number on the left side of the interface and click on "accept", then click on the corresponding button and if it is recognized from the people with whom the model has been trained, the program will send a message to whatsapp alerting you.
