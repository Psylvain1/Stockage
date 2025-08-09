#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 18:32:14 2025

@author: ssppa
"""

    
#!/usr/local/bin/python3
import numpy as np
from PIL import Image, ImageDraw
import cv2
image_name="reshaped_JL.png"
# Open the input image as numpy array, convert to RGB
img=Image.open(image_name)
npImage=np.array(img)
h,w=img.size
R=h//2-10
a=w//2
b=h//2


blank_image = np.full((h, w, 3), 255, dtype=np.uint8)


#Nail input
print(R)
N=400
print("nombre de nail",N)


Theta=(2*np.pi/N)
angle_list=[]
temp=0

while temp<2*np.pi :
    angle_list.append(temp)
    temp+= Theta
    

Nail_coordinates=[]
for x in angle_list:
    x_pos=a+int(R*np.cos(x))-1
    y_pos=b+int(R*np.sin(x))-1
    Nail_coordinates.append([x_pos,y_pos])
    npImage[x_pos][y_pos][0]=255


Iteration=1200


Path_list=[0]
l=-1
while l <Iteration:  
    l+=1
    print("Iteration number", l)
    Path_vals=[]
    for k in range(0,N+1):
        if k!=l:
            y_1=Nail_coordinates[Path_list[l]][0]
            y_2=Nail_coordinates[k][0]
            
            x_1=Nail_coordinates[Path_list[l]][1]
            x_2=Nail_coordinates[k][1]
            
            if x_1!=x_2:
                axisval=((y_2-y_1)/(x_2-x_1))
            else:
                axisval=0
            
            
            B_origine=int(y_2-axisval*x_2)
            Path_sum=0
            pixel_num=0
            
            
           
            
            if abs(x_1-x_2)>abs(y_1-y_2):
                if y_1==y_2:
                    for i in range(min(x_1,x_2),max(x_1,x_2)+1):
                        Path_sum+=npImage[y_1][i][0]
                        pixel_num+=1
                        #npImage[y_1][i][0]=0
                elif x_1>x_2:    
                    for i in range(x_1,x_2-1,-1): 
                        y_temp=int(i*axisval)+B_origine
                        Path_sum+=npImage[y_temp][i][0]
                        pixel_num+=1
                        #npImage[y_temp][i][0]=0
                       
                elif x_2>x_1:
                    for i in range(x_1,x_2+1):    
                        y_temp=int(i*axisval)+B_origine
                        Path_sum+=npImage[y_temp][i][0]
                        pixel_num+=1
                        #npImage[y_temp][i][0]=0
                        
            else:         
                if axisval!=0:
                    inverse=1/axisval
                else :
                    inverse=0
                if x_1==x_2:
                    for i in range(min(y_1,y_2),max(y_1,y_2)+1):   
                        Path_sum+=npImage[i][x_1][0]
                        pixel_num+=1
                        #npImage[i][x_1][0]=0
                        
                elif y_1>y_2:    
                    for i in range(y_1,y_2-1,-1):
                        x_temp=int((i-B_origine)*(inverse))
                        Path_sum+=npImage[i][x_temp][0]   
                        pixel_num+=1
                        #npImage[i][x_temp][0]=0
                elif y_2>y_1:
                    for i in range(y_1,y_2+1):                  
                        x_temp=int((i-B_origine)*(inverse))
                        Path_sum+=npImage[i][x_temp][0]
                        pixel_num+=1
                        #npImage[i][x_temp][0]=0
            if pixel_num!=0:
                Path_vals.append(Path_sum/pixel_num)
            else:
                Path_vals.append(0)
                

            
    Norm=max(Path_vals)
    
    for i in range (0,len(Path_vals)):
        Path_vals[i]=Path_vals[i]/Norm
    
    
    #top_two_values = np.sort(Path_vals)[-2:][::-1]
    top_two_values = np.sort(Path_vals)[:2][::-1]  # smallest two, reversed

    Min_val= np.argmin(Path_vals)
    if Min_val!=Path_list[l]:
        Path_list.append(Min_val)
    else:
        for i in range(0,len(Path_vals)):
            if Path_vals[i]==top_two_values[0]:
                Path_list.append(i)
    
    
    #String :
        
        
    y_1=Nail_coordinates[Path_list[l+1]][0]
    y_2=Nail_coordinates[Path_list[l]][0]
    
    x_1=Nail_coordinates[Path_list[l+1]][1]
    x_2=Nail_coordinates[Path_list[l]][1]
    
    if x_1!=x_2:
        axisval=((y_2-y_1)/(x_2-x_1))
    else:
        axisval=0
            
    B_origine=int(y_2-axisval*x_2)
    Path_sum=0
    pixel_num=0    
   
    string_val=255
    Penality= 125  #Control how fast pixel are extinct must not be null
    threshold=string_val-Penality
    
    if abs(x_1-x_2)>abs(y_1-y_2):
        if y_1==y_2:
            for i in range(min(x_1,x_2),max(x_1,x_2)+1):
                blank_image[y_1][i]=[0,0,0]    
                if npImage[y_1][i][0]<threshold :
                    npImage[y_1][i][0]=npImage[y_1][i][0]+Penality
                    
                else: 
                    npImage[y_1][i][0]=string_val
                    
        elif x_1>x_2:    
            for i in range(x_1,x_2-1,-1): 
                y_temp=int(i*axisval)+B_origine 
                blank_image[y_temp][i]=[0,0,0]    
                if npImage[y_temp][i][0]<threshold :
                    npImage[y_temp][i][0]=npImage[y_temp][i][0]+Penality
                else: 
                    npImage[y_temp][i][0]=string_val
                
               
        elif x_2>x_1:
            for i in range(x_1,x_2+1):  
                y_temp=int(i*axisval)+B_origine   
                blank_image[y_temp][i]=[0,0,0]    
                if npImage[y_temp][i][0]<threshold :
                    npImage[y_temp][i][0]=npImage[y_temp][i][0]+Penality
                else: 
                    npImage[y_temp][i][0]=string_val
                
    else:         
        if axisval!=0:
            inverse=1/axisval
        else :
            inverse=0
        if x_1==x_2:
            for i in range(min(y_1,y_2),max(y_1,y_2)+1):   
                blank_image[i][x_1]=[0,0,0]    
                if npImage[i][x_1][0]<threshold :
                    npImage[i][x_1][0]=npImage[i][x_1][0]+Penality
                else: 
                    npImage[i][x_1][0]=string_val
                
        elif y_1>y_2:    
            for i in range(y_1,y_2-1,-1):
                x_temp=int((i-B_origine)*(inverse))
                blank_image[i][x_temp]=[0,0,0]    
                if npImage[i][x_temp][0]<threshold :
                    npImage[i][x_temp][0]=npImage[i][x_temp][0]+Penality
                else: 
                    npImage[i][x_temp][0]=string_val
                
        elif y_2>y_1:
            for i in range(y_1,y_2+1):  
                x_temp=int((i-B_origine)*(inverse))
                blank_image[i][x_temp]=[0,0,0]    
                if npImage[i][x_temp][0]<threshold :
                    npImage[i][x_temp][0]=npImage[i][x_temp][0]+Penality
                else: 
                    npImage[i][x_temp][0]=string_val
        
    
      
    cv2.imshow("Image Window", blank_image)
    cv2.waitKey(1)  # Wait 500ms
    
    
        
print(Path_vals)
print(Path_list)

with open("paths.txt", "w") as f:
    for path in Path_list:
        f.write(f"{path},")

"""
print(len(Path_vals))    
print(Path_vals)
print(Nail_coordinates[0])
"""

# Save with alpha
#Image.fromarray(npImage).save('resulttestHiroko.png')
Image.fromarray(blank_image).save("results"+image_name)