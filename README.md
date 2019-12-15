# faceRecognitionWithSucuri

# How to Install

1) Run pip install opencv-python or change directory to C:\Python27\Scripts\ and run pip.exe install opencv-python
2) Download lfw from http://vis-www.cs.umass.edu/lfw/lfw.tgz (or any set of images you want to use)
3) Create "recognizedFaces" folder inside the folder you unziped this git
4) Run python server.py to start the server
5) Run python client.py 8 "path/to/the/image_set" to start the transfer of images from client to server
6) Wait till the transfer is done and the face recognition will automatically start
7) Wait till the processing is done and the recognized faces images will appear inside recognizedFaces folder

Obs:
The second parameter in step 5 is the number of processors you want to use, in my case was 8.
