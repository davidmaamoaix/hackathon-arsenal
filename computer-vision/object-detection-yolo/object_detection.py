# object detection

# dependencies
# pip install opencv-python numpy
import cv2 as cv
import numpy as np


# files
OBJECT_CLASSES_FILE = 'object_classes.txt'
YOLO_CONFIG_FILE = 'yolov3.cfg'
YOLO_WEIGHTS_FILE = 'yolov3.weights'

# network input size
# change this according to the network specs
image_size = 320

# confidence threshold
# predictions below this threshold will be discarded
confidence_threshold = 0.75

# read object classes from file
with open(OBJECT_CLASSES_FILE, 'r') as f:
	classes = [i.strip() for i in f.readlines()]

# random color per object
class_colors = [np.random.randint(255, size=(3,)).tolist() for _ in classes]

# set up the network
network = cv.dnn.readNetFromDarknet(YOLO_CONFIG_FILE, YOLO_WEIGHTS_FILE)

# YOLO's 3 output layers (refer to YOLO's paper/documentation)
output_layers = ['yolo_82', 'yolo_94', 'yolo_106']

# get the device's camera

# 0 is the index of the camera used, tweak this
# if your device has multiple cameras
camera = cv.VideoCapture(0)

# constant capturing & updating display
while True:
	successful, img = camera.read()

	blob = cv.dnn.blobFromImage(
		image=img,
		scalefactor=1 / 255, # convert image from int:[0, 255] to float:[0, 1]
		size=(image_size, image_size), # output size
		swapRB=True # swap R and B channels since OpenCV uses BGR
	)
	network.setInput(blob)

	# outputs is a list of 3 numpy arrays, corresponding
	# to the 3 output layers of YOLO
	outputs = network.forward(output_layers)

	# each prediction entry contains 85 elements
	# first 5 corresponds to (certer_x, center_y, width, height, confidence)
	# the rest is a one hot encoding of the predicted classes
	outputs = np.vstack(outputs)

	# outputs = outputs[outputs[:, 4] > confidence_threshold]
	predictions = np.argmax(outputs[:, 5:], axis=1)

	# get dimension of image
	img_height, img_width, _ = img.shape

	# change (certer_x, center_y, width, height) to (x, y, width, height)
	# each element is in percentage of the image shape, thus the
	# scaling by the image dimension
	object_boxes = np.zeros((predictions.shape[0], 4), dtype=np.int)
	# x
	object_boxes[:, 0] = (outputs[:, 0] - outputs[:, 2] / 2) * img_width
	# y
	object_boxes[:, 1] = (outputs[:, 1] - outputs[:, 3] / 2) * img_height
	# width
	object_boxes[:, 2] = outputs[:, 2] * img_width
	# height
	object_boxes[:, 3] = outputs[:, 3] * img_height

	# eliminate overlapping boxes on the same object via non max suppression
	# unfortunately NMSBoxes does not support numpy arrays as inputs
	filtered = cv.dnn.NMSBoxes(
		object_boxes.tolist(),
		outputs[:, 4].tolist(),
		confidence_threshold,
		0.2 # non max suppresion threshold
	)

	# draw boxes
	for i in filtered:

		# each element in filtered is a list of size 1, containing
		# the index of the passed in object_boxes whose corresponding
		# box survives the non max suppression
		index = i[0]
		box = object_boxes[index]
		x, y, w, h = box
		name = classes[predictions[index]]
		color = class_colors[predictions[index]]

		# draw the rectangle
		cv.rectangle(img, (x, y), (x + w, y + h), color, 3)
		cv.putText(img, f'{name}', (x, y - 15), 0, 1, color, 2)

	cv.imshow('capture', img)

	# stops the program if 'esc' is pressed
	if cv.waitKey(1) == 27:
		break