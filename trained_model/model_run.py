from tensorflow import keras
from socket import socket, AF_INET, SOCK_STREAM

saved_model = keras.models.load_model('saved_model/my_model') # Model directory goes here

import numpy as np
from keras.preprocessing import image
import os

server = socket(AF_INET, SOCK_STREAM)
server.bind(("127.0.0.1", 12000))
server.listen()
print()
print("Server listening")
# uploaded = files.upload()

# print(os.listdir('./content'))

while True:
  conn, addr = server.accept()

#test_files = os.listdir('./testfiles/') # Point to folder with the content were testing

# print(test_files)
  
  print("connected")
# for fn in test_files:
  # predicting images
  # path = './testfiles/' + fn

  isMask = False
  data = conn.recv(1024)
  if not data:
    continue
  fn = data.decode("UTF-8")
  path = './Dashboard/dashboard/static/images/' + fn
  img = image.load_img(path, target_size=(200, 200))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])
  classes = saved_model.predict(images, batch_size=10) # Need savedmodel 
  print(classes[0])  
  if classes[0]<0.5:
    print(fn + " is a no-mask")
    isMask = False
  else:
    print(fn + " is a mask")
    isMask =  True

  conn.send(str(isMask).encode("UTF-8"))
  conn.close()