# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 20:22:35 2018

@author: Josh
"""
import math
from copy import deepcopy

def getEntropy(attrs, data_frame, target_att):
    valFreq = {}
    data_entropy = 0.0

    """
    Find target_att
    """
    i = 0
    for entry in attrs:
        if(target_att == entry):
            break
        else:
            i += 1
    """
    Find frequencies
    """
    for entry in data_frame:
        if(entry[i] in valFreq):
            valFreq[entry[i]] += 1.0
        else:
            valFreq[entry[i]] = 1.0
    """
    Get entropy
    """
    for freq in valFreq.values():
        data_entropy += (-freq/len(data_frame))*math.log(freq/len(data_frame), 2)
        
    return(data_entropy)

def get_gain(attrs, data_frame, target_att, attr):
    valFreq = {}
    subset_entropy = 0.0
    
    i = attrs.index(attr)
    
    for entry in data_frame:
        if(entry[i] in valFreq):
            valFreq[entry[i]] += 1.0
        else:
            valFreq[entry[i]] = 1.0
    
    for val in valFreq.keys():
        val_prob = valFreq[val]/sum(valFreq.values())
        data_subset = [entry for entry in data_frame if entry[i] == val]
        subset_entropy += val_prob * getEntropy(attrs, data_subset, target_att)
    return(getEntropy(attrs, data_frame, target_att) - subset_entropy)
    
def get_best_gain(attrs, data_frame, target_att):
    max_gain = 0
    best = ""
    for attrib in attrs:
        if(attrib != target_att):
            set_entropy = getEntropy(attrs, data_frame, attrib)
            if(set_entropy != 0.0):
                new_gain = get_gain(attrs, data_frame, target_att, attrib)/getEntropy(attrs, data_frame, attrib)
                if (max_gain < new_gain):
                    max_gain = new_gain
                    best = attrib
    #print(best)
    #print(max_gain,"\n")
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
    
    default = majority(attrs, data_frame, target_att)
    
    if(len(data_frame) == 0 or (len(attrs)-1) <= 0):
        return default
    elif(vals.count(vals[0]) == len(vals)):
        return vals[0]
    else:
        best = get_best_gain(attrs, data_frame, target_att)
        if(best == ""):
            return default
        else:
            tree = {best:{}}
        
            for val in get_values(data_frame, attrs, best):
                new_attr = attrs[:]
                new_attr.remove(best)
                i=attrs.index(best)
                examples = deepcopy([entry for entry in data_frame if entry[i] == val])
                for line in examples:
                    line.pop(i)
                subtree = make_tree(examples, new_attr, target_att, recursion)
                tree[best][val] = subtree
            return tree
    
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

data_frame_game_full = [
        ["Is Home/Away?", "Is Opponent in AP Top 25 at Preseason?", "Media", "Win/Lose"],
        ["Home","Out","1-NBC", "Win"],
        ["Away","Out","4-ABC", "Win"],
        ["Home","In","1-NBC", "Win"],
        ["Home","Out","1-NBC", "Win"],
        ["Away","In","4-ABC", "Lose"],
        ["Home","Out","1-NBC", "Win"],
        ["Home","In","1-NBC", "Win"],
        ["Away","Out","4-ABC", "Win"],
        ["Away","Out","4-ABC", "Win"],
        ["Home","Out","1-NBC", "Win"],
        ["Away","Out","1-NBC", "Win"],
        ["Away","In","3-FOX", "Lose"],
        ["Away","Out","4-ABC", "Lose"],
        ["Home","Out","1-NBC", "Win"],
        ["Home","Out","1-NBC", "Lose"],
        ["Home","Out","1-NBC", "Lose"],
        ["Home","Out","2-ESPN", "Win"],
        ["Away","Out","4-ABC", "Lose"],
        ["Home","In","1-NBC", "Lose"],
        ["Home","Out","1-NBC", "Win"],
        ["Home","Out","5-CBS", "Lose"],
        ["Home","Out","1-NBC", "Win"],
        ["Home","In","1-NBC", "Lose"],
        ["Away","In","4-ABC", "Lose"],
        ]

print("Win/Lost Data Frame:\n")
attrs = data_frame_game[0]
data_frame_game.remove(attrs)

print(make_tree(data_frame_game,attrs,"Win/Lose",0), "\n")

print("Play or Not Data Frame:\n")
attrs = data_frame_play[0]
data_frame_play.remove(attrs)

print(make_tree(data_frame_play,attrs,"Play?",0), "\n")

print("Win/Lost Full Data Frame:\n")
attrs = data_frame_game_full[0]
data_frame_game_full.remove(attrs)

print(make_tree(data_frame_game_full,attrs,"Win/Lose",0), "\n")


