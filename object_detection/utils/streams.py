import cv2
from threading import Thread

class WebcamVideoStream:
	def __init__(self, src=0, width=640, height=480):
		# Initialize the stream
		self.stream = cv2.VideoCapture(src)
		# Set window width and height
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
		# Read the first frame
		(self.grabbed, self.frame) = self.stream.read()
		# Indicate if the thread should be stopped
		self.stopped = False

	def start(self):
		# Start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		# Keep looping infinitely until the thread is stopped
		while True:
			# If the thread indicator variable is set, stop the thread
			if self.stopped:
				return
			# Otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
 
	def read(self):
		# Return the frame most recently read
		return self.grabbed, self.frame
 
	def stop(self):
		# Indicate that the thread should be stopped
		self.stopped = True
