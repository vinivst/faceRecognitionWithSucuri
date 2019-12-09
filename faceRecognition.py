import os
import sys
import time
import cv2

sys.path.append(os.environ['PYDFHOME'])
from pyDF import *

from PIL import Image

save_dir = 'recognizedFaces'

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
    print "Caminho da imagem = %s" %fname
    cascPath = "haarcascade_frontalface_default.xml"    

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(fname)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
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



if __name__ == '__main__':
    nprocs = int(sys.argv[1])
    imagePath = list_imgs(sys.argv[2])[:100]

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