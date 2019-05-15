import numpy as np
import tensorflow as tf
import cv2

from utils.network import ardConnect
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

NUM_CLASSES = 90 # Max number of classes
PATH_TO_CKPT = 'model/frozen_inference_graph.pb' # Path to frozen detection graph (model)
PATH_TO_LABELS = 'model/mscoco_label_map.pbtxt' # Object labels for detection

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
	label_map,
	max_num_classes=NUM_CLASSES,
	use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def detect_objects(image_np, sess, detection_graph):
	# Expand dimensions since the model expects images to have shape
	image_np_expanded = np.expand_dims(image_np, axis=0)
	image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
	# Each box represents a part of the image where a particular object was detected.
	boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
	# Each score represent how level of confidence for each of the objects.
	# Score is shown on the result image, together with the class label.
	scores = detection_graph.get_tensor_by_name('detection_scores:0')
	classes = detection_graph.get_tensor_by_name('detection_classes:0')
	num_detections = detection_graph.get_tensor_by_name('num_detections:0')
	# Actual detection.
	(boxes, scores, classes, num_detections) = sess.run(
		[boxes, scores, classes, num_detections],
		feed_dict={image_tensor: image_np_expanded})

	for i in range(len(classes[0])):
		if classes[0][i] == 18: # dog is labelled 18
			ardConnect.call()
			break

	# Visualization of the results of a detection.
	vis_util.visualize_boxes_and_labels_on_image_array(
		image_np,
		np.squeeze(boxes),
		np.squeeze(classes).astype(np.int32),
		np.squeeze(scores),
		category_index,
		use_normalized_coordinates=True,
		line_thickness=8)
	return image_np

def worker(in_queue, out_queue):
	# Load a frozen Tensorflow model into memory.
	detection_graph = tf.Graph()
	with detection_graph.as_default():
		od_graph_def = tf.GraphDef()
		with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
			serialized_graph = fid.read()
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')
		sess = tf.Session(graph=detection_graph)
	# Send queued frames for object detection
	while True:
		frame = in_queue.get()
		if len(frame) == 2:
			frame_rgb = cv2.cvtColor(frame[1], cv2.COLOR_BGR2RGB)
			out_queue.put((frame[0], detect_objects(frame_rgb, sess, detection_graph)))
		else:
			frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			out_queue.put(detect_objects(frame_rgb, sess, detection_graph))
	sess.close()
