from tensorflow import keras
saved_model = keras.models.load_model('saved_model/my_model') # Model directory goes here

import numpy as np
from keras.preprocessing import image
import os

# uploaded = files.upload()

# print(os.listdir('./content'))

test_files = os.listdir('./test_files') # Point to folder with the content were testing

print(test_files)

for fn in test_files:
 
  # predicting images
  path = './test_files/' + fn
  img = image.load_img(path, target_size=(200, 200))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])
  classes = saved_model.predict(images, batch_size=10) # Need savedmodel 
  print(classes[0])  
  if classes[0]<0.5:
    print(fn + " is a no-mask")
  else:
    print(fn + " is a mask")