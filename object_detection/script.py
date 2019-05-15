import argparse
import os
import cv2

from multiprocessing import Queue, Pool
from threading import Thread
from queue import PriorityQueue
from utils.tf_worker import worker
from utils.streams import WebcamVideoStream

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # TF disable INFO, WARNING messages

DEVICE_ID = 0 # Device ID of the default camera (webcam)
FRAME_WIDTH = 1024 # Width of the frame
FRAME_HEIGHT = 768 # Height of the frame

def webcam(args):
	# Multiprocessing: input and output queue and pool of workers
	in_queue = Queue(maxsize=args["queue_size"])
	out_queue = Queue(maxsize=args["queue_size"])
	pool = Pool(args["num_workers"], worker, (in_queue, out_queue))
	# Create a threaded video stream
	camstream = WebcamVideoStream(
		src=DEVICE_ID,
		width=FRAME_WIDTH,
		height=FRAME_HEIGHT).start()
	while True:
		# Capture frame-by-frame
		ret, frame = camstream.read()
		if ret:
			in_queue.put(frame)
			output_rgb = cv2.cvtColor(out_queue.get(), cv2.COLOR_RGB2BGR)
			# Display the resulting frame
			cv2.imshow('frame', output_rgb)	 
		else:
			break
		# Exit by pressing 'e'
		if cv2.waitKey(1) & 0xFF == ord('e'):
			break
	pool.terminate()
	camstream.stop()
	cv2.destroyAllWindows()

def video(args):
	# Multiprocessing: input and output queue and pool of workers
	in_queue = Queue(maxsize=args["queue_size"])
	out_queue = Queue(maxsize=args["queue_size"])
	output_pq = PriorityQueue(maxsize=3*args["queue_size"])
	pool = Pool(args["num_workers"], worker, (in_queue,out_queue))
	# Create a threaded video stream
	videostream = cv2.VideoCapture("videos/{}".format(args["input_video"]))
	# Define the codec and create VideoWriter object
	if args["output"]:
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		out = cv2.VideoWriter(
			'videos/output.avi',
			fourcc, videostream.get(cv2.CAP_PROP_FPS),
			(int(videostream.get(cv2.CAP_PROP_FRAME_WIDTH)),
			int(videostream.get(cv2.CAP_PROP_FRAME_HEIGHT))))
	countWriteFrame = 1
	while True:
		# Check input queue is not full
		if not in_queue.full():
			# Read frame and store in input queue
			ret, frame = videostream.read()
			if ret:			
				in_queue.put((int(videostream.get(cv2.CAP_PROP_POS_FRAMES)),frame))
		# Check output queue is not empty
		if not out_queue.empty():
			# Recover treated frame in output queue and feed priority queue
			output_pq.put(out_queue.get())
		# Check output priority queue is not empty
		if not output_pq.empty():
			prior, output_frame = output_pq.get()
			if prior > countWriteFrame:
				output_pq.put((prior, output_frame))
			else:
				countWriteFrame = countWriteFrame + 1
				output_rgb = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)
				# Write the frame in file
				if args["output"]:
					out.write(output_rgb)
				cv2.imshow('frame', output_rgb)
		if cv2.waitKey(1) & 0xFF == ord('e'):
			break
		if ((not ret) & in_queue.empty() & out_queue.empty() & output_pq.empty()):
			break
	pool.terminate()
	videostream.release()
	if args["output"]:
		out.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	argParser = argparse.ArgumentParser()
	argParser.add_argument('-w', '--num-workers', dest='num_workers', type=int,
							default=2, help='Number of workers.')
	argParser.add_argument('-q-size', '--queue-size', dest='queue_size', type=int,
							default=5, help='Size of the queue.')
	argParser.add_argument("-o", "--output", type=int, default=0,
							help="Should the output be saved.")
	argParser.add_argument("-i", "--input-video", type=str, default="",
							help="Name of input video file.")
	args = vars(argParser.parse_args())

	if args["input_video"]:
		video(args)
	else:
		webcam(args)
