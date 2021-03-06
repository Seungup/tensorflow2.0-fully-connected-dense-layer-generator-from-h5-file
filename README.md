fully connected dense layer generator from h5 file
=============
### this is an useful program when you want to visualize the h5 model file. 
### this program will be generate fully connected dense layer.
### Currently, only Flatten, Dense, and Dropout are available.

* * *

Advance preparation
-------------
> 1. tensorflow 2.0
> 2. opencv-python
> 3. numpy
> 4. h5py
* * *

RESULT
-------------
## Fashion MNIST fully connected dense layer
![sample](https://github.com/Seungup/tensorflow-model-picture-generator/blob/master/saved_fashion_mnist_model.png)

* * *


* * *
## MNIST fully connected dense layer
![sample](https://github.com/Seungup/tensorflow-model-picture-generator/blob/master/samples/80458048_3043523079205350_242428497014816768_o.jpg)
![sample](https://github.com/Seungup/tensorflow-model-picture-generator/blob/master/samples/80622785_3043523679205290_7629639145098313728_o.jpg)

* * *


* * *

When you want to modify code
-------------
#### If you want to more big size of result or neurons radius, you can chage here

##### File PATH = function_test.ipynb

```python
img_w =  layers_number * 400 #here
img_h = img_w
radius = 8
```
* * *

#### If you want to change the nurens color, you can change here.

##### File PATH = function.py
```python
def drawingNerons(img, data, radius=1, color=(255, 255, 255)): #here
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
```python
def drawingLines(img, data, radius=1):
    values = []
    for now_data in range(len(data)):
        values.append(data[now_data])
    for a in range(len(values)):
        if (len(values)-1 >= (a+1)):
                for i in values[a]:                    
                        for j in values[a+1]:
                            img = cv2.line(img=img,
                                           pt1=getArrowStartPoint(i, radius),
                                           pt2=getArrowEndPoint(j, radius),
                                           color=(255, 255, 0)) #here
        else:
            pass
    return img
```
* * *
#### When the number of neurons rises above a certain level, the computer's performance slows down the results. 
#### Thus, by default, if more than 100 nodes exist inside a single layer, they are forced to switch to 30.

##### File PATH = function.py
```python
def model_neurons_position(data, max_num=100, max2min=30): #here
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
                           color=(255, 0, 255)) #here
    return img
```
