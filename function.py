#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tensorflow as tf
import h5py

# In[8]:


def getModelConfig(file):
    return tf.keras.models.load_model(file).get_config()


def getLayersName(file):
    
    layer_name = []
    
    try:
        model = getModelConfig(file)
        model = model['layers']
        model_length = len(model)

        for i in range(model_length):
            model_name = model[i]['class_name']
            layer_name.append(model_name)
    
    except:
        print("Unknown Error")
    
    finally:
        return layer_name


def getModelLayersConfig(file):
    
    model_config_list = []
    
    try:
        model_config = getModelConfig(file)
        model_config = model_config['layers']
        model_config_length = len(model_config)

        for i in range(model_config_length):
            model_config_in_for = model_config[i]['config'].items()
            model_i = []

            for i in model_config_in_for:
                model_i.append(i)

            model_config_list.append(model_i)
    except:
        print("Unkown Error")
    
    finally:
        return model_config_list
    
    
def showModelSummary(file):
    tf.keras.models.load_model(file).summary()
    
    
def getModelLayersConfigNormalization(file):
    model_layer_config = getModelLayersConfig(file)
    
    # <-- Nomarlization -->
    all_model_legnth = len(model_layer_config)
    NoneType_index = []
    
    for i in range(all_model_legnth):
        model_lenght = len(model_layer_config[i])
        
        for j in range(model_lenght):
            value = model_layer_config[i][j][1]
            if(value == None):
                NoneType_index.append([i, 
                                       j, 
                                       model_layer_config[i][j]
                                      ])

    for data in NoneType_index:
        i, j, removeData = data
        model_layer_config[i].remove(removeData)
    # <-- FINISH -->    
    
    return model_layer_config

def getOptimazer(file):
    path = file
    f = h5py.File(path, 'r')
    f_keys = list(f.keys())
    f_keys_keys = list(f[f_keys[1]].keys())
    return f_keys_keys[0]