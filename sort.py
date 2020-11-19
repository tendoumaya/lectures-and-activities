import keras
from keras.models import Sequential as seq
from keras.layers import Dense as dens
from keras.layers import Dropout as drop
from keras.layers import Flatten as flat
from keras.layers import Conv2D, MaxPooling2D
import matplotlib.image as mimage

batch_size=int(input('Number of initial sample:'))
classes=4
epochs=12
imgR,imgC=25,25

(x_train,y_train),(x_test,y_test)=mimage.read('''data''') #input the training images and test image
x_train=x_train.reshape(60000,25,25,1)
x_test=x_test.reshape(10000,25,25,1)
y_train=keras.utils.to_categorical(y_train,classes)
y_test=keras.utils.to_categorical(y_test,classes)

model=seq()
model.add(Conv2D(32,kernel_size=(3,3),
                 activation='relu',
                 input_shape=(28,28,1)))
model.add(Conv2D(64,kernel_size=(3,3),
                 activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(drop(0.25))
model.add(flat())
model.add(dens(128,activation='relu'))
model.add(drop(0.25))
model.add(dens(classes,activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
model.fit(x_train,y_train,
          batch_size=batch_size,
          epochs=epochs,verbose=1,
          validation_data=(x_test,y_test))
score=(model.evaluate(x_test,y_test,verbose=0))
print('Test loss: %s; Test accuracy: %s'%(score[0],score[1]))
