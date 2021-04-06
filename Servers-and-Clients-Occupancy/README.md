First create an environment:

python -m venv flaskenv (or pick your own name)

Then install the dependencies:

pip3 install -r requirements.txt

In the Front-End folder, run the flask server:

flask run --host=0.0.0.0 (opens at localhost:5000)

In the Occupancy folderm simply run the file:

python3 occupancyClient.py

To check out the dummy mask client, go in the mask dummy folder and run:

python3 maskClient.py

For the occupancy tracker: change captureVideo = cv2.VideoCapture("example_02.mp4") to captureVideo = cv2.VideoCapture(0) (or another number if multiple web cams) to get a webcam input. This line is in the setUpVideo function.

Also note that due to the example video being a generic video, people moving out of frame upwards were considered entering the room, and people moving downwards out of framw were considered exiting the room. This can be fixed by changing the occupancyCount update lines in the code (i.e. change occupancyCount += 1 to occupancyCount -= 1 and occupancyCount -= 1 to occupancyCount += 1, the change is needed in multiple locations.)
