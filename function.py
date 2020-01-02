import tensorflow as tf
import h5py
import cv2
import numpy as np
from tqdm import tqdm

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
    
    
def getBlankImage(height, width, dimension=3):
    return np.zeros((height, width, dimension), np.uint8)

def showImage(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def getArrowStartPoint(circle_center, radius):
    x, y = circle_center
    return (x+radius, y)

def getArrowEndPoint(circle_center, radius):
    x, y = circle_center
    return (x-radius, y)

def getSectionWight(section_num, section, wight):
    
    if (wight % section_num == 0):
        new_w = (wight / section_num)
    else:
        new_w = int(wight / section_num)
    
    if (new_w % 2 == 0):
        move_w = (new_w * (section-1)) + (new_w / 2)
    else:
        move_w = (new_w * (section-1)) + int(new_w / 2)
        
    return move_w

def getSectionHeigh(h, num):
    
    if (h % num == 0):  
        distance = h / num
    else:
        if (num >= int(h / num)):
            distance = int(h / num)
        else:
            distance = int(h / num) - 1
            
    blank_piexl = (h - (distance * num))

    sub_h = h - blank_piexl    
    add_h = 0
    return_h_list = []
    
    while(True):
        if(add_h == sub_h):
            break
        else:
            return_h_list.append(add_h + (blank_piexl / 2))
            add_h = add_h + distance
    
    return return_h_list

def drawingNerons(img, data, radius=1, color=(255, 255, 255)):
    for i in data:
        img = cv2.circle(img=img,
                         center=i,
                         radius=radius,
                         color=color,
                         thickness=-1)
    return img



def getNeuronPostion(img_w, img_h, number_of_section, section, number_of_neuron):

    x = getSectionWight(wight=img_w, section_num=number_of_section, section=section)


    y = getSectionHeigh(h=img_h, num=number_of_neuron)
    
    circe_center = []
    for i in y:
        data = (int(x), int(i + ((img_h - y[len(y) - 1]) / 2)))
        circe_center.append(data)
    return circe_center

def drawingLines(img, data, radius=1):
    
    values = []
    for now_data in range(len(data)):
        values.append(data[now_data])
    

    for a in range(len(values)):
        if (len(values)-1 >= (a+1)):
                
                for i in values[a]:                    
                        for j in values[a+1]:

                                if(a == 0):
                                    img = cv2.line(img=img,
                                                   pt1=getArrowStartPoint(i, radius),
                                                   pt2=getArrowEndPoint(j, radius),
                                                   color=(255, 255, 0))

                                else:
                                    img = cv2.line(img=img,
                                                   pt1=getArrowStartPoint(i, radius),
                                                   pt2=getArrowEndPoint(j, radius),
                                                   color=(255, 255, 0))
        else:
            pass

    return img

# Data Sequence n_neuron, n_sction_number
def getAllNeurons(img, img_w, img_h, number_of_sction, data):
    tmp_list = []
    
    for i in range(len(data)):
        tmp_list.append(data[i])
    
    return_list = []
    for i in range(len(tmp_list)):
        data = getNeuronPostion(img_w=img_w,
                                         img_h=img_h,
                                         number_of_neuron=tmp_list[i][0],
                                         number_of_section=number_of_sction,
                                         section=tmp_list[i][1])
        return_list.append(data)
    
    
    return return_list

def getLayerList(path):
    model_data = getLayersInfo(path)
    dense_list = []
    for i in range(len(model_data)):
        if i == 0:
            pass
        else:
            data = model_data[i]['layer']
            if data == "Flatten":
                num = model_data[i]['output_shape']
                getData = (num, i, "Flatten")
                dense_list.append(getData)
                
            if data == "Dropout":
                num = model_data[i-1]['neruons']
                getData = (num, i, "Dropout")
                dense_list.append(getData)
                
            if data == "Dense":
                num = model_data[i]['neruons']
                getData = (num, i, "Dense")
                dense_list.append(getData)
    return dense_list

def save(img, number):
    cv2.imwrite(f"saved_{number}.png", img)


def model_neurons_position(data, max_num=130, max2min=30):

    return_list = []
    for i in range(len(data)):
        if(data[i][0] > max_num):
            num, sec, _ = data[i]
            num = max2min
            return_list.append([num, sec])
        else:
            return_list.append(list(data[i]))
    return return_list

def getModelWeights(path):
    model_data = tf.keras.models.load_model(path)
    data = model_data.get_weights()
    
    return data

def findDropoutPart(dense_list):
    a = []
    for i in range(len(dense_list)):
        if (dense_list[i][2] == "Dropout"):
            a.append(i)

    return_list = []
    for i in range(len(dense_list)):
        for now_a in range(len(a)):
            if (i+1 == a[now_a]):
                return_data = (i, a[now_a])
                return_list.append(return_data)

    return return_list

def drawDropoutLine(img, neuron_postion, radius, dense_list):
    
    location_of_dropout = findDropoutPart(dense_list)
    
    for i in tqdm(range(len(location_of_dropout)), "Dropout to Dense"):
        new_postion = (neuron_postion[location_of_dropout[i][0]], 
                       neuron_postion[location_of_dropout[i][1]])
        
        for j in range(len(new_postion[0])):
            img = cv2.line(img=img,
                           pt1= getArrowStartPoint(new_postion[0][j], radius),
                           pt2= getArrowEndPoint(new_postion[1][j], radius),
                           color=(255, 0, 255))
    return img

def findDensePart(dense_List):

    test_list = list(range(len(dense_List)))
    test_ = []
    for i in range(len(test_list)):
        test_.append((i, i+1))
    

    test_1 = []
    num = findDropoutPart(dense_List)
    
    for i in test_[:-1]:
        if(i in num):
            pass
        else:
            test_1.append(i)
            
    return test_1


def drawDenseLine(img, neuron_postion, radius, dense_list):
    
    location_of_dense = findDensePart(dense_list)
    
    for i in tqdm(range(len(location_of_dense)), "Dense to Dense"):
        first = location_of_dense[i][0]
        second = location_of_dense[i][1]
        
        new_postion = neuron_postion[first], neuron_postion[second]
        
        for j in range(len(new_postion[0])):
            img = drawingLines(img=img, 
                                data=new_postion,
                                radius=radius)
    return img
