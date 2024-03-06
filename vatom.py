import math 
import keyboard 
import mss.tools 
import numpy as np 
import serial 
import torch


arduino = serial.Serial('COM11', 115200, timeout=0) 
model = torch.hub.load('C:/yolov5', 'custom', path='C:/Users/starr/Documents/aiboi/valo.pt', source='local') 
#model = torch.hub.load('C:/yolov5', 'custom', path='C:/Users/starr/Documents/aiboi/c1.pt', source='local') 

with mss.mss() as sct: 

    dimensions = sct.monitors[1] 
    SQUARE_SIZE = 300  
    monitor = {"top": int((dimensions['height'] / 2) - (SQUARE_SIZE / 2)), 
               "left": int((dimensions['width'] / 2) - (SQUARE_SIZE / 2)), 
               "width": SQUARE_SIZE, 
               "height": SQUARE_SIZE} 
 
  
 
    while True: 

        BRGframe = np.array(sct.grab(monitor)) 
        RGBframe = BRGframe[:, :, [2, 1, 0]] 
        results = model(RGBframe, size=300) 
        model.conf = 0.7 
        enemyNum = results.xyxy[0].shape[0] 
 
        if enemyNum == 0: 
 
            pass 
 
        else: 
 
            distances = [] 
            closest = 1000 
 
            for i in range(enemyNum): 
 
                x1 = float(results.xyxy[0][i, 0]) 
                x2 = float(results.xyxy[0][i, 2]) 
                y1 = float(results.xyxy[0][i, 1]) 
                y2 = float(results.xyxy[0][i, 3]) 
                
                centerX = (x2 - x1) / 2 + x1 
                centerY = (y2 - y1) / 2 + y1 

                distance = math.sqrt(((centerX - 150) ** 2) + ((centerY - 150) ** 2)) 
                distances.append(distance) 
 
                if distances[i] < closest: 
 
                    closest = distances[i] 
 
                    closestEnemy = i 

 
            x1 = float(results.xyxy[0][closestEnemy, 0]) 
            x2 = float(results.xyxy[0][closestEnemy, 2]) 
            y1 = float(results.xyxy[0][closestEnemy, 1]) 
            y2 = float(results.xyxy[0][closestEnemy, 3]) 
 
            Xenemycoord = (x2 - x1) / 2 + x1 
            Yenemycoord = (y2 - y1) / 6 + y1 
 
            difx = int(Xenemycoord - (SQUARE_SIZE / 2))
            dify = int(Yenemycoord - (SQUARE_SIZE / 2))
 
            if keyboard.is_pressed('e'): 
 
                data = str(difx) + ':' + str(dify) 
                arduino.write(data.encode())
            