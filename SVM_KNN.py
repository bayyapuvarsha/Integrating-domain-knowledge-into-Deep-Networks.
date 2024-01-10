
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename
import pandas as pd 
import os
import cv2
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier

main = tkinter.Tk()
main.title("Integrating Domain Knowledge Into Deep Networks for Lung Ultrasound With Applications to Lung Cancer")
main.geometry("2000x2000")

global filename
global classifier
global svm_er, knn_er
global X, Y
global X_train, X_test, y_train, y_test
global pca

def uploadDataset():
    global filename
    filename = filedialog.askdirectory(initialdir=".")
    text.delete('1.0', END)
    text.insert(END,filename+" loaded\n");
    
    
def splitDataset():
    global X, Y
    global X_train, X_test, y_train, y_test
    global pca
    text.delete('1.0', END)
    X = np.load('features/X.txt.npy')
    Y = np.load('features/Y.txt.npy')
    X = np.reshape(X, (X.shape[0],(X.shape[1]*X.shape[2]*X.shape[3])))

    pca = PCA(n_components = 100)
    X = pca.fit_transform(X)
    print(X.shape)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    text.insert(END,"Total CT Scan Images Found in dataset : "+str(len(X))+"\n")
    text.insert(END,"Train split dataset to 80% : "+str(len(X_train))+"\n")
    text.insert(END,"Test split dataset to 20%  : "+str(len(X_test))+"\n")


def executeSVM():
    global classifier
    global svm_er
    text.delete('1.0', END)
    cls = svm.SVC() 
    cls.fit(X_train, y_train)
    predict = cls.predict(X_test)
    svm_er = 1 - (accuracy_score(y_test,predict))
    classifier = cls
    text.insert(END,"SVM Error Rate : "+str(svm_er)+"\n")

def executeKNN():
    global knn_er
    cls = KNeighborsClassifier(n_neighbors = 2) 
    cls.fit(X_train, y_train)
    predict = cls.predict(X_test)
    knn_er= 1 - accuracy_score(y_test,predict)
    text.insert(END,"KNN Error Rate : "+str(knn_er)+"\n")
    

def predictDisease():
    filename = filedialog.askopenfilename(initialdir="testSamples")
    img = cv2.imread(filename)
    img = cv2.resize(img, (64,64))
    im2arr = np.array(img)
    im2arr = im2arr.reshape(64,64,3)
    im2arr = im2arr.astype('float32')
    im2arr = im2arr/255
    test = []
    test.append(im2arr)
    test = np.asarray(test)
    test = np.reshape(test, (test.shape[0],(test.shape[1]*test.shape[2]*test.shape[3])))
    test = pca.transform(test)
    predict = classifier.predict(test)[0]
    msg = ''
    if predict == 0:
        msg = "Uploaded CT Scan is Normal"
    if predict == 1:
        msg = "Uploaded CT Scan is Abnormal"
    img = cv2.imread(filename)
    img = cv2.resize(img, (400,400))
    cv2.putText(img, msg, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 255), 2)
    cv2.imshow(msg, img)
    cv2.waitKey(0)    

def graph():
    height = [svm_er, knn_er]
    bars = ('SVM Error Rate','KMeans Error Rate')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()

font = ('times', 14, 'bold')
title = Label(main, text='Integrating Domain Knowledge Into Deep Networks for Lung Ultrasound With Applications to Lung Cancer')
title.config(bg='deep sky blue', fg='white')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 12, 'bold')
text=Text(main,height=20,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=50,y=110)
text.config(font=font1)


font1 = ('times', 13, 'bold')
uploadButton = Button(main, text="Upload Lung Cancer Dataset", command=uploadDataset)
uploadButton.place(x=50,y=500)
uploadButton.config(font=font1)  

readButton = Button(main, text="Read & Split Dataset to Train & Test", command=splitDataset)
readButton.place(x=350,y=500)
readButton.config(font=font1) 

svmButton = Button(main, text="Execute SVM Algorithms", command=executeSVM)
svmButton.place(x=50,y=550)
svmButton.config(font=font1) 

kmeansButton = Button(main, text="Execute KNN Algorithm", command=executeKNN)
kmeansButton.place(x=350,y=550)
kmeansButton.config(font=font1) 

predictButton = Button(main, text="Predict Lung Disease", command=predictDisease)
predictButton.place(x=50,y=600)
predictButton.config(font=font1)

graphButton = Button(main, text="Error Rate Graph", command=graph)
graphButton.place(x=350,y=600)
graphButton.config(font=font1) 

main.config(bg='LightSteelBlue3')
main.mainloop()
