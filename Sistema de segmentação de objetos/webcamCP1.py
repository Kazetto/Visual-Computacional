import cv2
import os,sys, os.path
import numpy as np
import math


url = ''


def image_da_webcam(img):
         
    #modificando a escala de cor para RGB e para HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #PRECISA ARRUMAR A MASK 
   
    
    #definindo o intervalo de mascara de cor
    image_lower_hsv = np.array([0, 190, 50])
    image_upper_hsv = np.array([10, 255, 255])

    
    #mask-
    mask_red = cv2.inRange(img_hsv, image_lower_hsv, image_upper_hsv)
    contornos_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    mask_red = cv2.cvtColor(mask_red, cv2.COLOR_GRAY2RGB) 
    
    
     
    
    #definindo o intervalo de mascara de cor
    image_lower_green = np.array([71, 255, 49])
    image_upper_green = np.array([105, 255, 205])
   
    
    #mask-
    mask_green = cv2.inRange(img_hsv, image_lower_green, image_upper_green)
    contornos_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    mask_green = cv2.cvtColor(mask_green, cv2.COLOR_GRAY2RGB) 
    

    
    mask_final = mask_green + mask_red
    contornos_all = contornos_red + contornos_green
    
    contornos_final = mask_final.copy()
    
    cv2.drawContours(contornos_final, contornos_all, -1, [0, 0, 255], 5);  
    
    
    
     # Cópia da máscara para ser desenhada "por cima"

   
    try:
    
        cnt = contornos_all[0]
        cnt2 = contornos_all[1]

        M = cv2.moments(cnt)
        print( M )
        M2 = cv2.moments(cnt2)
        print( M2 )


        # Calculo das coordenadas do centro de massa

        try:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cx2 = int(M2['m10']/M2['m00'])
            cy2 = int(M2['m01']/M2['m00'])
            area1 = cv2.contourArea(contornos_all[0])
            area2 = cv2.contourArea(contornos_all[1])

            textArea1 = (area1, "pixeis");
            textArea2 = (area2, "pixeis");

    # print("Area do circulo da esquerda:", Area2)

            print("Circulo Direita: ",cx, cy)
            print("Circulo Esquerda: ",cx2, cy2)
            size = 20
            color = (255,128,0)
            color_reta = (0,255,0)
    
            cv2.line(contornos_final,(cx - size,cy),(cx + size,cy),color,5)
            cv2.line(contornos_final,(cx,cy - size),(cx, cy + size),color,5)


    #Circulo Esquerda
            cv2.line(contornos_final,(cx2 - size,cy2),(cx2 + size,cy2),color,5)
            cv2.line(contornos_final,(cx2,cy2 - size),(cx2, cy2 + size),color,5)

    # Para escrever vamos definir uma fonte 

            font = cv2.FONT_HERSHEY_SIMPLEX
            text = cy , cx
            origem2 = (0,40)

            font = cv2.FONT_HERSHEY_SIMPLEX
            text2 = cy2 , cx2
            origem = (400,300)

            origem3 = (230,250)
            origem4 = (300,100)
            cv2.putText(contornos_final, str(text), origem, font,1,(200,50,0),2,cv2.LINE_AA)
            cv2.putText(contornos_final, str(text2), origem2, font,1,(200,50,0),2,cv2.LINE_AA)

            cv2.putText(contornos_final, str(textArea1), origem3, font,1,(200,50,0),2,cv2.LINE_AA)
            cv2.putText(contornos_final, str(textArea2), origem4, font,1,(200,50,0),2,cv2.LINE_AA)     
            
            #Linha Ponto a ponto
            cv2.line(contornos_final,(cx2,cy2),(cx,cy),color_reta,5)
   
        
    #Definindo o Angulo da reta
            tan = (cy-cy2)/(cx-cx2)*(180/math.pi)

            font = cv2.FONT_HERSHEY_SIMPLEX
            text = "O angulo possui aprox.: "+f'{tan:.2f}'+" GRAUS"
            origem = (15,450)
            cv2.putText(contornos_final, str(text), origem, font,1,(255,255,255),2,cv2.LINE_AA)

        except ZeroDivisionError:
         M = 0 
    except IndexError:
        for x in [2]: 
            print("Precisa de ter pelos menos de 2 objetos")

    
    
    return contornos_final

cv2.namedWindow("preview")
camera = 0
vc = cv2.VideoCapture(0)
#vc = cv2.VideoCapture(url)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame)


    
    cv2.imshow("preview", img)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
