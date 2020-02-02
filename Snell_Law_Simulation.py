import numpy as np 
import cv2 as cv
from math import *
def snell_anim():
    u_env=1
    u_slab=1.3
    inc_agl=30
    speed=1.5 #speed of animation
    u_env=float(input("Enter refractive index of environment: \n "))
    u_slab=float(input("Enter refractive index of glass slab: \n"))
    inc_agl=float(input("Enter angle of incidence to slab: \n")) #in degres
    inc_agl=(pi/180)*inc_agl
    refr_agl=asin((u_env/u_slab) * sin(inc_agl))
    inc_agl2=inc_agl
    win_ht= 800
    win_wt=1200
    slab_wt=1000
    slab_ht=200
    thic=2 #thickness of border
    x0,y0 =100,0
    u_slab2=u_slab
    count=0
    first_pt=(0,0)
    flag_once_done=False
    flag=1
    #main Loop begins here:
    #while(True):
    refr_agl=asin((u_env/u_slab) * sin(inc_agl))
    img = np.zeros((win_ht,win_wt,3), np.uint8)
    img = cv.rectangle(img, ((win_wt-slab_wt)//2,(win_ht-slab_ht)//2), ((win_wt+slab_wt)//2,(win_ht+slab_ht)//2), (98,81,53),thic)
    font = cv.FONT_HERSHEY_SIMPLEX
    lateral_shift = (slab_wt)*(sin(inc_agl-refr_agl)/cos(refr_agl))
    cv.putText(img, "Refractive Index 1 : "+str(u_env), (win_wt-220,25), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(img, "Refractive Index 2 : "+str(u_slab), (win_wt-220,45), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(img, "Incident Angle : "+str(round((inc_agl*180)/(pi))), (win_wt-220,65), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(img, "Refraction Angle : "+str(round((refr_agl*180)/(pi))), (win_wt-220,85), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(img, "Lateral Shift : "+str(round(lateral_shift))+" pixels", (win_wt-220,105), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)        
    cv.putText(img, "Snell's Law", (225,25), font, 1, (255, 255, 255), 1, cv.LINE_AA)
    lin1_len=0
    init_pt=(x0,y0)
    inc_pt=(0,0)
    #incident line
    while(True):
        pt2=(round(x0 + lin1_len*sin(inc_agl)) , round(y0 + lin1_len*cos(inc_agl)))
        img=cv.line(img,init_pt, pt2, (0,255,0), thic)
        lin1_len+=speed
        if pt2[1]>(win_ht-slab_ht)//2:
            break
        cv.imshow("Snell's Law", img)                
        if cv.waitKey(10) == 27:
            cv.destroyAllWindows()    
            break
    first_pt=inc_pt=(round(x0 + lin1_len*sin(inc_agl)) , round(y0 + lin1_len*cos(inc_agl)))
    lin2_len=0
    img=cv.line(img, (inc_pt[0],inc_pt[1]-50),(inc_pt[0],inc_pt[1]+50),(0,0,255),thic)
    incident_point_x,incident_point_y=inc_pt
    #dotted line of the incidence
    dash_len=10
    strt_pt=inc_pt
    while(True):
        strt_pt=round(strt_pt[0]+dash_len*sin(inc_agl)),round(strt_pt[1]+dash_len*cos(inc_agl))
        end_pt=round(strt_pt[0]+dash_len*sin(inc_agl)),round(strt_pt[1]+dash_len*cos(inc_agl))
        img=cv.line(img, strt_pt, end_pt, (0,255,0), thic//2)
        cv.imshow("Snell's Law", img)      
        strt_pt=round(strt_pt[0]+dash_len*sin(inc_agl)),round(strt_pt[1]+dash_len*cos(inc_agl))
        if(end_pt[1] > win_ht): 
            break
        if cv.waitKey(150) == 27:
            cv.destroyAllWindows()    
            break
    #line inside the slab
    while(True):
        pt2=(round(inc_pt[0] + lin2_len*sin(refr_agl)) , round(inc_pt[1] + lin2_len*cos(refr_agl)))
        img=cv.line(img,inc_pt, pt2, (255,0,0), thic)
        lin2_len+=speed
        if pt2[1]>(win_ht+slab_ht)//2:
            break
        cv.imshow("Snell's Law", img)                
        if cv.waitKey(10) == 27:
            cv.destroyAllWindows()    
            break
    inc_pt=pt2
    lin3_len=0
    img=cv.line(img, (inc_pt[0],inc_pt[1]-50),(inc_pt[0],inc_pt[1]+50),(0,0,255),thic)
    #refracted line
    while(True):
        pt2=(round(inc_pt[0] + lin3_len*sin(inc_agl)) , round(inc_pt[1] + lin3_len*cos(inc_agl)))
        img=cv.line(img,inc_pt, pt2, (0,255,0), thic)
        lin3_len+=speed
        if pt2[1]>win_ht:
            break
        cv.imshow("Snell's Law", img)                
        if cv.waitKey(10) == 27:
            cv.destroyAllWindows()    
            break      
    flag_once_done=1
    if cv.waitKey(0) == ord(' '):
        flag_start_animation=1
####################################################################################################
################################### SECOND ANIMATION ###################################
    while(True):     
        lateral_shift = (slab_wt)*(sin(inc_agl-refr_agl)/cos(refr_agl))   
        #img = cv.line(img,(0,0),(511,511),(255,0,0),5)  
        img = np.zeros((win_ht,win_wt,3), np.uint8)
        #normal to incidence
        img = cv.line(img,(incident_point_x,incident_point_y-50),(incident_point_x,incident_point_y+50),(0,0,255),thic)            
        #slab
        img = cv.rectangle(img, ((win_wt-slab_wt)//2,(win_ht-slab_ht)//2), ((win_wt+slab_wt)//2,(win_ht+slab_ht)//2), (98,81,53),thic)
        #incident line
        len_incident_line=700  
        img =cv.line(img,(incident_point_x,incident_point_y),(round(incident_point_x-len_incident_line*sin(inc_agl)),round(incident_point_y-len_incident_line*cos(inc_agl))),(0,255,0),thic) 
        strt_pt=incident_point_x,incident_point_y
        dash_len=2000
        end_pt=round(strt_pt[0]+dash_len*sin(inc_agl)),round(strt_pt[1]+dash_len*cos(inc_agl))
        img=cv.line(img, strt_pt, end_pt, (0,255,0), thic//2) 
        #line inside slab    
        img = cv.line(img,(incident_point_x,incident_point_y),(incident_point_x+round(slab_ht*tan(refr_agl)),(win_ht+slab_ht)//2),(255,0,0),thic)   
        #normal to refracted
        img = cv.line(img,(incident_point_x+round(slab_ht*tan(refr_agl)),(win_ht+slab_ht)//2-50),(incident_point_x+round(slab_ht*tan(refr_agl)),(win_ht+slab_ht)//2+50),(0,0,255),thic)            
        #refracted line
        img =cv.line(img,(incident_point_x+round(slab_ht*tan(refr_agl)),(win_ht+slab_ht)//2),(incident_point_x+round(slab_ht*tan(refr_agl)+3*len_incident_line*sin(inc_agl)),((win_ht+slab_ht)//2+round(3*len_incident_line*cos(inc_agl)))),(0,255,0),thic) 
        #put text
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(img, "Refractive Index 1 : "+str(u_env), (win_wt-220,25), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)
        cv.putText(img, "Refractive Index 2 : "+str(u_slab), (win_wt-220,45), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)
        cv.putText(img, "Incident Angle : "+str(round((inc_agl*180)/(pi))), (win_wt-220,65), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)
        cv.putText(img, "Refraction Angle : "+str(round((refr_agl*180)/(pi))), (win_wt-220,85), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)
        cv.putText(img, "Lateral Shift : "+str(round(lateral_shift))+" pixels", (win_wt-220,105), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)        
        cv.putText(img, "Snell's Law", (225,25), font, 1, (255, 255, 255), 1, cv.LINE_AA)
        if flag:
            inc_agl+=0.002 
        else:
             inc_agl-=0.002
        refr_agl = asin((u_env/u_slab)*sin(inc_agl))
        if inc_agl>1.48353 or inc_agl<0:
            flag^=1          
        cv.imshow("Snell's Law", img)   
        if cv.waitKey(5) == ord(' '):
            if cv.waitKey(0) == ord(' '):
                continue
        if cv.waitKey(1) == 27:
            cv.destroyAllWindows()    
            break              
if __name__=="__main__":
    snell_anim()

