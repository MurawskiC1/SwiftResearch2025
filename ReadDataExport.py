#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:52:54 2023

@author: catermurawski
"""

import pandas as pd
import BurstChaser as bc

#Find The GRBS Name withing the Subject Data 
def findName(n):
    try:
        n = n.split("batgrbcat//")
        n = n[1].split("/web/GRB")
        return n[0]
    except:
        return "No Name Found"
    


beta = pd.read_csv("burst-chaser-classifications.csv")


repeatS=0
repeatP=0
#dictionairy {id: PusleShapeClass}
shapes_practice = {}
pulse_shapes = {}
pulse_noise = {}
pulse_locations = {}
cont = {}
#sort through all indexes
for i in range(11101,beta.shape[0]):
    workflow = beta.workflow_name.iloc[i]
    wid = beta.workflow_id.iloc[i]
    id_number = beta.subject_ids.iloc[i]
    results = beta.annotations.iloc[i]
    user = beta.user_name.iloc[i]
    burst_name = findName(beta.subject_data.iloc[i])

    if user not in cont and "not-logged" not in user:
        cont[user] = 1
    elif "not-logged" not in user:
        cont[user] += 1
    
    #Workflow Pulse Shape Practice
    if workflow == "(Optional) Practice: Pulse Shapes":
        if  id_number not in shapes_practice:
            #create a pulse shape class
            shapes_practice[id_number] = bc.PulseShape(burst_name, id_number, wid)
        if user not in shapes_practice[id_number].contributers:
            shapes_practice[id_number].contributersAdd(user)
            shapes_practice[id_number].ShapeCount(results)
            shapes_practice[id_number].FollowCount(results)
           
    #Workflow Pulse Shape 
    if workflow == "Pulse shapes":
        if  id_number not in pulse_shapes:
            #create a pulse shape class
            pulse_shapes[id_number] = bc.PulseShape(burst_name, id_number, wid)
        if user not in pulse_shapes[id_number].contributers:
            pulse_shapes[id_number].contributersAdd(user)
            pulse_shapes[id_number].ShapeCount(results)
            pulse_shapes[id_number].FollowCount(results)
        
    
    #Worflow Pulse or Noise Practice
    if workflow == "(Optional) Practice: Pulse or noise?":
        if id_number not in pulse_noise:
            pulse_noise[id_number] = bc.PulseNoise(burst_name,id_number, wid)
        if user not in pulse_noise[id_number].contributers:  
            pulse_noise[id_number].contributersAdd(user)
            pulse_noise[id_number].classCount(results)
        else:
            repeatP +=1
    
    #Workflow Where are the Pulses
    if workflow =="Where are pulses?":
        if id_number not in pulse_locations:
            pulse_locations[id_number] = bc.PulseLocation(burst_name, id_number, wid)
        if user not in pulse_locations[id_number].contributers:
            pulse_locations[id_number].contributersAdd(user)
            pulse_locations[id_number].read(results)
        
            
            
            
        



###UPDATE THE CSV FILES

bc.PulseShape.export("Pulse_Shapes", [pulse_shapes[i] for i in pulse_shapes])
bc.PulseShape.export("Pulse_Shapes_Practice", [shapes_practice[i] for i in shapes_practice])
bc.PulseNoise.export("Pulse_Noise_Practice", [pulse_noise[i] for i in pulse_noise])
bc.PulseLocation.export("Pulse_Location", [pulse_locations[i] for i in pulse_locations])




print(bc.count)
