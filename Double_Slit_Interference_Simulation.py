import numpy as np
import cv2
import math
font = cv2.FONT_HERSHEY_SIMPLEX

maxSlitDistance=6
maxWavelength=1
maxSlitScreenDistance=6

current_y_co_ordinate = 1
current_x_co_ordinate = 1


def track_mouse(event,x,y,flags,param):    
    global current_y_co_ordinate, current_x_co_ordinate
    if event == cv2.EVENT_MOUSEMOVE:
        current_y_co_ordinate = y  
        current_x_co_ordinate = x              
    #return 1
def interference():    
    global current_y_co_ordinate
    slitDistanceRange = [i/10000 for i in range(1,20000)]
    wavelengthRange = [i for i in range(400,650)]
    nuRange = [i/10000 for i in range(10000,30000)]
    slitScreenDistanceRange = [i for i in range(100,170)]
        
    slitDistance = 5
    wavelength  = 700
    slitScreenDistance = 90
    slab_width_range = [i/1000 for i in range(1,5000)]
    slab_u_range = [i/10000 for i in range(10000,50000)]
    slab_present = "NULL"
    slab_u = 5000
    slab_width = 7
    nu  = 0
    while(slitDistance not in slitDistanceRange):
        slitDistance = float(input("Enter distance between slits (in mm)"))
    while(wavelength not in wavelengthRange):
        wavelength = float(input("Enter wavelength (in nm)"))
    while(slitScreenDistance not in slitScreenDistanceRange):
        slitScreenDistance = float(input("Enter distance between slit and screen (in cm)"))
    while(nu not in nuRange):
        nu = float(input("Enter refractive index of the medium")) 
    while((slab_present!=False) and (slab_present!=True)):
        slb_input = input("Slab? (Y/N)")
        if slb_input=="Y":
            slab_present=True
        if slb_input=="N":
            slab_present=False

    if(slab_present):
        while(slab_u not in slab_u_range):
            slab_u = float(input("Enter slab's refractive index "))
        while(slab_width not in slab_width_range):
            slab_width = float(input("Enter slab's width (in mm) "))

    wavelength = wavelength/nu
    
    slit_intensity = 1

    flaggg = 1

    #parameters
    t = 2 
    win_height = 700
    win_width = 1600      
    d_factor_in_showing = 50
    leftPadding = 50
    IntensityBarWidth = 70
    #slab_present = True
    #slab_u = 5
    #slab_width = 50 #in mm


    #co-ordinates simuulation
    slitDistanceFake = 2
    x_source_1 = leftPadding
    y_source_1 = (win_height//2)-round(d_factor_in_showing*(slitDistanceFake/2))
    x_source_2 = leftPadding
    y_source_2 = (win_height//2)+round(d_factor_in_showing*(slitDistanceFake/2))
    x_screen = win_width-leftPadding*6
    y_screen_1 = 30
    y_screen_2 = win_height - y_screen_1
    y_moving_point = win_height//2


    #co-ordinates graph
    x_axis_1=x_screen+20
    x_axis_2=win_width-20
    x_axis_height=round(0.75*(win_height))
    #############
    flag_for_y_point = 0

    path_difference_to_show = (((win_height//2-y_moving_point) *d_factor_in_showing*(slitDistance/2)) / (win_width-leftPadding))
    thetaFakeMax = math.atan(((win_height//2)-30)/(x_screen-x_source_1)) #in radians

    

    thetaRealMax = 0.1*(math.pi/180) #in radians (10 degrees)
    RealToFaketheta = thetaRealMax/thetaFakeMax    


    #################      begin Real values
    thetaReal = thetaRealMax #in radians  
    pathDifference = slitDistance*math.sin(thetaReal) # in mm
    phaseDifference = ((2*math.pi)/(wavelength*(10**(-6))))*pathDifference #in radians
    ############################# end Real Values
            
    while(True):                        
        img = np.zeros((win_height,win_width,3), np.uint8)     

        #light_lines 
        img = cv2.line(img,(x_source_1,y_source_1),(x_screen,y_moving_point),(0,0,255),1) 
        img = cv2.line(img,(x_source_2,y_source_2),(x_screen,y_moving_point),(0,0,255),1)   
        #middle_line
        img = cv2.line(img,(x_source_2,win_height//2),(x_screen,y_moving_point),(50,50,50),1)   

        #horizontal line
        img = cv2.line(img,(leftPadding,win_height//2),(x_screen,win_height//2),(100,100,100),1)   

        #perpendicular line  

        #for up        
        if y_moving_point<win_height//2:        
            angle_of_line = ((win_height//2-y_moving_point)+(y_source_2-win_height//2))/(x_screen-x_source_2)
            path_difference_to_show = 5*(((win_height//2-y_moving_point) *d_factor_in_showing*(slitDistanceFake/2)) / (win_width-leftPadding))
            #base
            img = cv2.line(img,(x_source_2,y_source_2),(round(x_source_2+path_difference_to_show*math.cos(angle_of_line)),round(y_source_2-path_difference_to_show*math.sin(angle_of_line))),(255,255,255),2)   
            #perpedicular
            img = cv2.line(img,(x_source_1,y_source_1),(round(x_source_2+path_difference_to_show*math.cos(angle_of_line)),round(y_source_2-path_difference_to_show*math.sin(angle_of_line))),(255,255,255),2)   

        #for down       
        if y_moving_point>win_height//2:        
            angle_of_line = ((y_moving_point-win_height//2)+(win_height//2-y_source_1))/(x_screen-x_source_2)
            path_difference_to_show = 5*(((y_moving_point-win_height//2) *d_factor_in_showing*(slitDistanceFake/2)) / (win_width-leftPadding))
            #base
            img = cv2.line(img,(x_source_1,y_source_1),(round(x_source_1+path_difference_to_show*math.cos(angle_of_line)),round(y_source_1+path_difference_to_show*math.sin(angle_of_line))),(255,255,255),2)   
            #perpedicular
            img = cv2.line(img,(x_source_2,y_source_2),(round(x_source_1+path_difference_to_show*math.cos(angle_of_line)),round(y_source_1+path_difference_to_show*math.sin(angle_of_line))),(255,255,255),2)   

        #Calculations
        thetaFake = math.atan(((win_height//2)-y_moving_point)/(x_screen-x_source_1)) #in radians 
        thetaReal = thetaFake*RealToFaketheta #in radians  
        y_actual = slitScreenDistance*(10)*math.tan(thetaReal) #in mm        
        pathDifference = slitDistance*math.sin(thetaReal) + slab_present*(slab_u-nu)*slab_width                         
        phaseDifference = ((2*math.pi)/(wavelength*(10**(-6))))*pathDifference #in radians
        actual_intensity = math.cos(phaseDifference/2)*math.cos(phaseDifference/2)
        fringe_width = (wavelength*(10**(-6))*slitScreenDistance*(10))/slitDistance #in mm
        #################################Strip and Graph#############################################    
        for s in range(y_screen_1,win_height-y_screen_1):            
            y_middle=(win_height)//2                                              
            s_y=y_middle-s
            theta_here=math.atan(s_y/(x_screen-x_source_1))
            theta_here*=RealToFaketheta
            y_actual2 = slitScreenDistance*(10)*math.tan(theta_here) #in mm        
            pathDifference2 = slitDistance*math.sin(theta_here) + slab_present*(slab_u-nu)*slab_width                         
            phaseDifference2 = ((2*math.pi)/(wavelength*(10**(-6))))*pathDifference2
            intensity=255*(math.cos(phaseDifference2/2)**2)
            x_coordinate=x_screen+30
            img=cv2.line(img, (x_coordinate,s),(x_coordinate+40,s),(intensity,intensity,intensity),1)
            distance=x_coordinate+100-intensity/255*40
            #img=cv2.circle(img,(round(distance),s),(255,255,255),1)
            img = cv2.circle(img,(round(distance),s), 1, (255,255,255), -1) 
                      
        #############################################################################

        #Calculations of cursor point -
        thetaFake_c = math.atan(((win_height//2)-current_y_co_ordinate)/(x_screen-x_source_1)) #in radians 
        thetaReal_c = thetaFake_c*RealToFaketheta #in radians  
        y_actual_c = slitScreenDistance*(10)*math.tan(thetaReal_c) #in mm        
        pathDifference_c = slitDistance*math.sin(thetaReal_c)  + slab_present*(slab_u-nu)*slab_width                         # in mm
        phaseDifference_c = ((2*math.pi)/(wavelength*(10**(-6))))*pathDifference_c #in radians
        actual_intensity_c = math.cos(phaseDifference_c/2)*math.cos(phaseDifference_c/2)

       
       
       
       
        #screen
        img = cv2.line(img,(x_screen,y_screen_1),(x_screen,y_screen_2),(100,100,100),10)   



        #source_between_line        
        img = cv2.line(img,(x_source_1,y_source_1),(x_source_2,y_source_2),(100,100,100),2)                   
        #source1
        img = cv2.circle(img,(x_source_1,y_source_1), 7, (255,255,255), -1)    
        #source2
        img = cv2.circle(img,(x_source_2,y_source_2), 7, (255,255,255), -1)


        #y_screen_dot      
        img = cv2.circle(img,(x_screen,y_moving_point), 7, (255,255,255), -1)  

        #intensity bar
        #img = cv2.rectangle(img,(leftPadding,actual_intensity),(leftPadding+IntensityBarWidth,win_height-leftPadding),(0,255,0),3)
        img = cv2.rectangle(img, (leftPadding, round(win_height-leftPadding-150*actual_intensity-20)), (leftPadding+IntensityBarWidth, win_height-leftPadding-20), (round(255*actual_intensity), round(255*actual_intensity), round(255*actual_intensity)), cv2.FILLED)          
        if current_x_co_ordinate>=x_screen+30 and current_x_co_ordinate<=x_screen+70:
            img = cv2.rectangle(img, (leftPadding*2+IntensityBarWidth, round(win_height-leftPadding-150*actual_intensity_c-20)), (2*leftPadding+2*IntensityBarWidth, win_height-leftPadding-20), (round(255*actual_intensity_c), round(255*actual_intensity_c), round(255*actual_intensity_c)), cv2.FILLED)          

        
        #slab if     
        if slab_present:
            img = cv2.rectangle(img, (x_source_1+50, y_source_1-30), (x_source_1+80, y_source_1+30), (135, 135, 135), 1)             

        #text    
        cv2.putText(img, "Screen", (x_screen-30,20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "Source", (x_source_1//2,y_source_1-x_source_1//2), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "d", (x_source_1//2,(win_height//2)), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)                
        cv2.putText(img, "Interference of light", (win_width//3,50), font, 1.5, (255, 255, 255), 1, cv2.LINE_AA)        

        cv2.putText(img, "d = "+str(slitDistance)+" (in mm)", (50,100), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "D = "+str(slitScreenDistance)+" (in cm)", (50,120), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "r = "+str(nu)+"", (50,140), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)     
        cv2.putText(img, "Angle = "+str(round(thetaReal*(180/math.pi),5))+" (in degrees)", (50,160), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)             
        cv2.putText(img, "Path Difference = "+str(round(pathDifference,5))+" (in mm)", (50,180), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA) 
        cv2.putText(img, "Fringe Width = "+str(round(fringe_width,5))+" (in mm)", (50,220), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA) 
        cv2.putText(img, "Intensity", (leftPadding,win_height-40), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)   
        if current_x_co_ordinate>=x_screen+30 and current_x_co_ordinate<=x_screen+70: 
            cv2.putText(img, "Intensity at cursor", (2*leftPadding+IntensityBarWidth,win_height-40), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)     
        
        phaseDifferencetoDisplay = (phaseDifference*(180/math.pi))%360
        if phaseDifferencetoDisplay>180:
            phaseDifferencetoDisplay-=360
        cv2.putText(img, "Phase Difference = "+str(round(phaseDifferencetoDisplay,5))+" (in degrees)", (50,200), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)                             
        cv2.imshow("Interference (Fresnel's Biprism Experiment)", img) 
        cv2.setMouseCallback("Interference (Fresnel's Biprism Experiment)",track_mouse)        
                         


        if flag_for_y_point:
            y_moving_point+=1
        else:
            y_moving_point-=1
    
        if y_moving_point>y_screen_2 or y_moving_point<y_screen_1:
            flag_for_y_point^=1
        
        ##############Strip##################
    
        #####################################
                  
        if cv2.waitKey(5) == ord(' '):
            if cv2.waitKey(0) == ord(' '):
                continue

        if cv2.waitKey(5) == 27:
            cv2.destroyAllWindows()    
            break
if __name__ == '__main__':
    interference()