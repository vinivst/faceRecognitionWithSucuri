import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import logging
import os
import sys
import time
import cv2

sys.path.append(os.environ['PYDFHOME'])
from pyDF import *

from PIL import Image

save_dir = 'recognizedFaces'

# Set up logging
logging.basicConfig(level=logging.INFO)

server = SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests=True,
    allow_none=True
)

dataReceivedFolder = "C:/Users/vinic/Documents/UERJ/Sistemas Distribuidos/Sucuri-master/examples/FaceRecognition/dataReceived"

# Expose a function
def server_receive_file(self,directory):
        with open("dataReceived/"+directory, "wb") as handle:
            handle.write(self.data)
            return True


server.register_function(server_receive_file)

def list_imgs(rootdir):
    fnames = []

    for current, directories, files in os.walk(rootdir):
        for f in files:
        	fnames.append(current + '/' + f)
 
    fnames.sort()
    return fnames

def faceRecognition(args):
    fname = args[0]
    recognizedFace = fname.split('/')[-1]
    cascPath = "haarcascade_frontalface_default.xml"    

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(fname)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    recognizedFace = save_dir + '/' +  recognizedFace.split('.')[0]  + '.png'

    cv2.imwrite( recognizedFace, image );

    return faces


def print_name(args):
    faces = args[0]

    print("Found {0} faces!".format(len(faces)))

def sucuri(nprocs):
    nprocs = nprocs
    imagePath = list_imgs(dataReceivedFolder)

    graph = DFGraph()
    sched = Scheduler(graph, nprocs, mpi_enabled = False)



    feed_files = Source(imagePath)

    convert_file = FilterTagged(faceRecognition, 1)  

    pname = Serializer(print_name, 1)


    graph.add(feed_files)
    graph.add(convert_file)
    graph.add(pname)


    feed_files.add_edge(convert_file, 0)
    convert_file.add_edge(pname, 0)

    t0 = time.time()
    sched.start()
    t1 = time.time()
    print "Execution time %.3f" %(t1-t0)

server.register_function(sucuri)

if __name__ == '__main__':
	# Start the server
	try:
	    print('Use Control-C to exit')
	    server.serve_forever()
	except KeyboardInterrupt:
	    print('Exiting')