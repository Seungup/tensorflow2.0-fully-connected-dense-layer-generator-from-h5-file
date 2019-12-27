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
    
    model = getModelConfig(file)
    model = model['layers']
    model_length = len(model)

    for i in range(model_length):
        model_name = model[i]['class_name']
        layer_name.append(model_name)

    return layer_name


def getModelLayersConfig(file):
    
    model_config_list = []
    

    model_config = getModelConfig(file)
    model_config = model_config['layers']
    model_config_length = len(model_config)

    for i in range(model_config_length):
        model_config_in_for = model_config[i]['config'].items()
        model_i = []

        for i in model_config_in_for:
            model_i.append(i)

        model_config_list.append(model_i)

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
    try:
        path = file
        f = h5py.File(path, 'r')
        f_keys = list(f.keys())
        f_keys_keys = list(f[f_keys[1]].keys())
        return f_keys_keys[0]
    except:
        return None

def printLayer(path):
    
    layers_name = getLayersName(path) 
    data = getModelLayersConfigNormalization(path)
    optimazier = getOptimazer(path)
    
    print(f"Optimazer : {optimazier}\n")
    for i in range(len(data)):

        init_new = 0

        print(f"Layer_{i} | Name : {layers_name[i]}")

        if (i == 0):
            init = 1
            batch_input_shape = data[i][2][1]

            for j in batch_input_shape:
                if (j == None):
                    j = 1
                init = init * j 

            print(f"Layer_{i} | input_shape : {batch_input_shape}")
            print(f"Layer_{i} | output_shape : {init}")
            print(f"Layer_{i} | Paragms : {init_new}\n")


        else:

            if(data[i][3][0] == "units"):

                nowlayer = i

                neruons = data[i][3][1]
                init_new = init * data[i][3][1] + data[i][3][1]
                init = data[i][3][1] # init update

                print(f"Layer_{i} | Neurons : {neruons}")
                print(f"Layer_{i} | Paragms : {init_new}\n")


            elif(data[i][3][0] == "rate"):

                rate = data[i][3][1] * 100

                print(f"Layer_{i} | Rate : {rate}%")
                print(f"Layer_{i} | Paragms : {init_new}\n")



            elif(data[i][3][0] == "activation"):

                funtion_name = data[i][3][1]

                print(f"Layer_{i} | Funtion : {funtion_name}")
                print(f"Layer_{i} | Paragms : {init_new}\n")


            else:
                print("XXXXXXXXXXXX")
                print(f"Layer_{i} | {data[i][3][0]} : {data[i][3][1]}")
                
                
def getLayersInfo(path):
    return_list = []
    try:
        layers_name = getLayersName(path) 
        data = getModelLayersConfigNormalization(path)
        optimazier = getOptimazer(path)

        return_list.append({"optimazier" : optimazier})

        for i in range(len(data)):

            init_new = 0

            if (i == 0):
                init = 1
                batch_input_shape = data[i][2][1]

                for j in batch_input_shape:
                    if (j == None):
                        j = 1
                    init = init * j 


                layer_data_dic = {
                    "layer" : layers_name[i],
                    "input_shape" : batch_input_shape,
                    "output_shape" : init,
                    "paragms" : init_new
                }

                return_list.append(layer_data_dic)


            else:

                if(data[i][3][0] == "units"):

                    nowlayer = i

                    neruons = data[i][3][1]
                    init_new = init * data[i][3][1] + data[i][3][1]
                    init = data[i][3][1] # init update

                    layer_data_dic = {
                        "layer" : layers_name[i],
                        "neruons" : neruons,
                        "paragms" : init_new
                    }

                    return_list.append(layer_data_dic)

                elif(data[i][3][0] == "rate"):

                    rate = data[i][3][1] * 100


                    layer_data_dic = {
                        "layer" : layers_name[i],
                        "rate" : rate,
                        "paragms" : init_new
                    }

                    return_list.append(layer_data_dic)

                elif(data[i][3][0] == "activation"):

                    funtion_name = data[i][3][1]

                    layer_data_dic = {
                        "layer" : layers_name[i],
                        "funtion" : funtion_name,
                        "paragms" : init_new
                    }

                    return_list.append(layer_data_dic)

                else:
                    print("XXXXXXXXXXXX")
                    return_list.append(None)
    finally:
        return return_list