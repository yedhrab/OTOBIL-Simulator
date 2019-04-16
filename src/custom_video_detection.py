######## Video Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 1/16/18
# Description:
# This program uses a TensorFlow-trained classifier to perform object detection.
# It loads the classifier uses it to perform object detection on a video.
# It draws boxes and scores around the objects of interest in each frame
# of the video.

# Some of the code is copied from Google's example at
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

# and some is copied from Dat Tran's exampsle at
# https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

# but I changed it to make it more understandable to me.

# Import packages
from image_processing_utils import find_turn_angle
from utils import visualization_utils as vis_util
from utils import label_map_util
import os
import cv2
import numpy as np
import tensorflow as tf
import sys


# Modeli devreye sokma
MODEL_ACTIVE = True
# KEEP = True
SHOW = True
SHOW_ORIGINAL = True

# Name of the directory containing the object detection module we're using
MODEL_DIR = 'model'
VIDEO_PATH = r'test/test.mp4'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_DIR, 'ali_model.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_DIR, 'labelmap.pbtxt')

# Path to video
PATH_TO_VIDEO = os.path.join(CWD_PATH, VIDEO_PATH)

# Number of classes the object detector can identify
NUM_CLASSES = 14

# Alt algılama sınırı (olasılık %)
MIN_SCORE_THRESH = 0.60

# OUT = cv2.VideoWriter(
#     'OUTput.avi',
#    cv2.VideoWriter_fourcc(*'XVID'),
#    5.0,
#    (640, 400)
# ) if KEEP else None


if MODEL_ACTIVE:
    # Load the label map.
    # Label maps map indices to category names, so that when our convolution
    # network predicts `5`, we know that this corresponds to `king`.
    # Here we use internal utility functions, but anything that returns a
    # dictionary mapping integers to appropriate string labels would be fine
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    # Define input and output tensors (i.e. data) for the object detection classifier

    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name(
        'detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')


# Open video file
video = cv2.VideoCapture(PATH_TO_VIDEO)

while(video.isOpened()):
    # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
    ret, frame = video.read()

    # Frame varsa kontrol yapma
    if frame is not None:
        # İlk videoyu ekrana basma
        cv2.imshow('Orjinal Video', frame) if SHOW_ORIGINAL else None

        if MODEL_ACTIVE:
            frame_expanded = np.expand_dims(frame, axis=0)

            # Perform the actual detection by running the model with the image as input
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores,
                    detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})

            # Draw the results of the detection (aka 'visulaize the results')
            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8,
                min_score_thresh=MIN_SCORE_THRESH)
        try:
            data = find_turn_angle(frame)
            if data is not None:
                frame, data = data
                print("Dönüş değerleri:",
                      "Sol" if data[0] < 0 else "Sağ", "Pixel uzunluğu:", data[1])
        except:
            print("Görüntü işlemede sorun meydana geldi")

        # Sonucu ekrana basma
        cv2.imshow('Islenmis Video', frame) if SHOW else None

        # Sonucu videoya kayıt etme
        # OUT.write(frame) if KEEP else None
    else:
        print("Frame değeri None olarak geldi, video kapatıldı.")
        break

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break


# Clean up
video.release()
cv2.destroyAllWindows()
# OUT.release() if KEEP else None
