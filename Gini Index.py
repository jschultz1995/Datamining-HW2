# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 20:22:35 2018

@author: Josh
"""
import math

def get_gini(attrs, data_frame, target_att, attr):
    valFreq_att = {}
    valFreq_target = {}
    count = 0
    index_one = attrs.index(attr)
    index_two = attrs.index(target_att)
    gini = 0.0
    tot_gini = 0.0
    
    i = attrs.index(attr)
    
    for entry in data_frame:
        if(entry[i] in valFreq_att):
            valFreq_att[entry[i]] += 1.0
        else:
            valFreq_att[entry[i]] = 1.0
    
    i =attrs.index(target_att)
    
    for entry in data_frame:
        if(entry[i] in valFreq_target):
            valFreq_target[entry[i]] += 1.0
        else:
            valFreq_target[entry[i]] = 1.0
            
    for val in valFreq_att.keys():
        for label in valFreq_target.keys():
            for entry in data_frame:
                if(entry[index_one] == val and entry[index_two] == label):
                    count += 1
            gini += (math.pow(count/valFreq_att[val],2))
            count = 0
        tot_gini += ((1 - gini)*(valFreq_att[val]/len(data_frame)))
        gini = 0
    #print("Gini to Return: ", tot_gini)
    return tot_gini
  
def get_low_gini(attrs, data_frame, target_att):
    low_gini = 1
    #best = ""
    for attrib in attrs:
        if(attrib != target_att):
            new_gini = (get_gini(attrs, data_frame, target_att, attrib))
            if (low_gini > new_gini):
                low_gini = new_gini
                best = attrib
    return best

def majority(attrs, data_frame, target_att):
    valFreq = {}
    index = attrs.index(target_att)
    
    for entry in data_frame:
        if (entry[index] in valFreq):
            valFreq[entry[index]] += 1.0
        else:
            valFreq[entry[index]] = 1.0
    
    max = 0
    major = ""
    
    for key in valFreq.keys():
        if (valFreq[key] > max):
            max = valFreq[key]
            major = key
    
    return major

def get_values(data_frame, attrs, attr):
    index = attrs.index(attr)
    values = []
    for entry in data_frame:
        if(entry[index] not in values):
            values.append(entry[index])
    return values


def make_tree(data_frame, attrs, target_att, recursion):
    recursion += 1
    data_frame = data_frame[:]
    vals = [record[attrs.index(target_att)] for record in data_frame]
    #print(data_frame)
    #print(attrs.index(target_att))
    #print("Vals: ",vals)
    
    default = majority(attrs, data_frame, target_att)
    
    if(len(data_frame) == 0 or (len(attrs)-1) <= 0):
        return default
    elif(vals.count(vals[0]) == len(vals)):
        #print(vals[0])
        return vals[0]
    else:
        best = get_low_gini(attrs, data_frame, target_att)
        #if(best != ""):
        tree = {best:{}}
        
        for val in get_values(data_frame, attrs, best):
            new_attr = attrs[:]
            new_attr.remove(best)
            i=attrs.index(best)
            #print("index to delete: ",i)
            examples = [entry for entry in data_frame if entry[i] == val]
            #print("Before deletion:\n", examples)
            #examples = py.delete(examples, 0, i)
            for list in examples:
                list.pop(i)
            #print("After deletion:\n",examples)
            subtree = make_tree(examples, new_attr, target_att, recursion)
            tree[best][val] = subtree
    return tree
        #else:
            #return
    
data_frame_game = [
        ["Is Home/Away?", "Is Opponent in AP Top 25 at Preseason?", "Media", "Win/Lose"],
        ["Home","Out","1-NBC", "Win"],
        ["Home", "In", "1-NBC", "Lose"],
        ["Away","Out","2-ESPN", "Win"],
        ["Away","Out","3-FOX", "Win"],
        ["Home","Out","1-NBC", "Win"],
        ["Away","Out","4-ABC", "Win"],
        ]

data_frame_play = [
        ["Outlook","Temperature","Humidity","Windy","Play?"],
        ["Sunny","Hot","High","False","No"],
        ["Sunny","Hot","High","True","No"],
        ["Overcast","Hot","High","False","Yes"],
        ["Rainy","Mild","High","False","Yes"],
        ["Rainy","Cool","Normal","False","Yes"],
        ["Rainy","Cool","Normal","True","No"],
        ["Overcast","Cool","Normal","True","Yes"],
        ["Sunny","Mild","High","False","No"],
        ["Sunny","Cool","Normal","False","Yes"],
        ["Rainy","Mild","Normal","False","Yes"],
        ["Sunny","Mild","Normal","True","Yes"],
        ["Overcast","Mild","High","True","Yes"],
        ["Overcast","Hot","Normal","False","Yes"],
        ["Rainy","Mild","High","True","No"],
        ]

print("Win/Lost Data Frame:\n")
attrs = data_frame_game[0]
data_frame_game.remove(attrs)

print(make_tree(data_frame_game,attrs,"Win/Lose",0))

print("Play or Not Data Frame:\n")
attrs = data_frame_play[0]
data_frame_play.remove(attrs)

print(make_tree(data_frame_play,attrs,"Play?",0))

