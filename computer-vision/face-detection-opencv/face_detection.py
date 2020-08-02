# face detection

# dependencies
import cv2 as cv


# classifier
CLASSIFIER = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# 0 is the index of the camera used, tweak this
# if your device has multiple cameras
camera = cv.VideoCapture(0)

# constant capturing & updating display
while True:
	successful, img = camera.read()

	# harr cascade classifier for face is meant for grayscale image
	# covert the image to grayscale
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	# locate faces
	faces = CLASSIFIER.detectMultiScale(gray, 1.3, 5)

	# the position of box around object for each face,
	# do WHATEVER you want with it
	for x, y, w, h in faces:

		# draw rectangle
		cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)

	cv.imshow('capture', img)

	# stops the program if 'esc' is pressed
	if cv.waitKey(1) == 27:
		break