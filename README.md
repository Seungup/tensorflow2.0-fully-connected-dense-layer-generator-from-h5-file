Tensorflow Model Picture Generator
=============

Advance preparation
-------------
> 1. tensorflow 2.0 ver
> 2. opencv
> 3. tqdm
> 4. h5py
> 5. matplotlib

how to use
-------------
#### just lunch the .ipny file and click it that's it
* * *
When you want to modify code
-------------
#### If you want to more big size of result or neurons radius, you can modified to this section

##### File PATH = function_test.ipynb

```python
img_w =  layers_number * 400
img_h = img_w
radius = 8
```
* * *

#### If you want to change the nurens color, you can change here.

##### File PATH = function.py
##### LINE NUMBER = 288
```python
def drawingNerons(img, data, radius=1, color=(255, 255, 255)): # here
    for i in data:
        img = cv2.circle(img=img,
                         center=i,
                         radius=radius,
                         color=color,
                         thickness=-1)
    return img
```
* * *
#### If you want to change the Dense to Dense line color, you can change here.

##### File PATH = function.py
##### LINE NUMBER = 312
```python
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
                                                   color=(255, 255, 0)) # here

                                else:
                                    img = cv2.line(img=img,
                                                   pt1=getArrowStartPoint(i, radius),
                                                   pt2=getArrowEndPoint(j, radius),
                                                   color=(255, 255, 0)) # here
        else:
            pass

    return img
```
* * *
#### When the number of neurons rises above a certain level, the computer's performance slows down the results. 
#### Thus, by default, if more than 130 nodes exist inside a single layer, they are forced to switch to 30.
#### If you want to chage that value, you can chage here

##### File PATH = function.py
##### LINE NUMBER = 387
```python
def model_neurons_position(data, max_num=130, max2min=30): #here
    return_list = []
    for i in range(len(data)):
        if(data[i][0] > max_num):
            num, sec, _ = data[i]
            num = max2min
            return_list.append([num, sec])
        else:
            return_list.append(list(data[i]))
    return return_list
```
* * *
#### If you want to chage Dropout to Dense line color you can chage here

##### File PATH = function.py
##### LINE NUMBER = 472
```python
def drawDropoutLine(img, neuron_postion, radius, dense_list):
    
    location_of_dropout = findDropoutPart(dense_list)
    
    for i in tqdm(range(len(location_of_dropout)), "Dropout to Dense"):
        new_postion = (neuron_postion[location_of_dropout[i][0]], 
                       neuron_postion[location_of_dropout[i][1]])
        
        for j in range(len(new_postion[0])):
            img = cv2.line(img=img,
                           pt1= getArrowStartPoint(new_postion[0][j], radius),
                           pt2= getArrowEndPoint(new_postion[1][j], radius),
                           color=(255, 0, 255)) # here
    return img
```
