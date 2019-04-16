import os

import numpy as np
import tensorflow as tf

# models/research/object_detection dizinindeki modül yüklemeleri
from utils import label_map_util
from utils import visualization_utils as vis_util

# Sadece harici modül olarak kullanılabilir
if __name__ == '__main__':
    print("Yardımcı modüldür, doğrudan çalıştırılmaz")
    exit()

# Eğitilmiş modellerimizi barındıran dizinin adı (.pb olmadan)
MODEL_DIR = 'model'

# Çalışma ortamımızın bulunduğu dizinin yolu
CWD_PATH = os.getcwd()

# Obje algılama için kullanılacak modelin dondurulmuş çıkarım grafiğinin
# (frozen_inference_graph.py) yolu
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_DIR, 'ali_model.pb')

# Etiket haritasının yolu (.pbtxt uzantılı dosya)
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_DIR, 'labelmap.pbtxt')

# Obje algılayan modeldeki etiket çeşidi sayısı
NUM_CLASSES = 14

# Alt algılama sınırı (olasılık %)
MIN_SCORE_THRESH = 0.85,

# Model Değişkenleri
model_prepared = False
detection_graph = None
sess = None

# Etiket ve kategori değişkenleri
label_map = None
categories = None
category_index = None


def prepare_tf_model():
    """Tensorflow modelini hazırlama
    Dondurulmuş Tensorflow modelini, etiket haritasını ve kategorileri hafızaya yükleme
    """

    # Dondurulmuş tensorflow modelini hafizaya yükleme
    global detection_graph, sess
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    # Etiket haritasını ve kategorileri yükleme
    global label_map, categories, category_index
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Modelin hazır olduğunu kaydetme
    global model_prepared
    model_prepared = True


def is_model_prepared():
    return model_prepared


def detect_from_image(image: np.ndarray, visualize=True) -> list:
    """Resimden algılanan obje bilgilerini alma

    Arguments:
        image {numpy.ndarray} -- Numpy array formatında resim objesi
    """

    # Model hazır değilse hazırlama
    prepare_tf_model() if not is_model_prepared() else None

    # Resmin uzunluklarını saklama
    height, width = image.shape[0:2]

    # Expand dimensions since the model expects images to have shape: [1,
    # None, None, 3]
    image_expanded = np.expand_dims(image, axis=0)
    # Input tensor is the image_np
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image_np where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image_np, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    # Extract detection classes
    detection_classes = detection_graph.get_tensor_by_name(
        'detection_classes:0')
    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Perform the actual detection by running the model with the image_np as input
    (boxes, scores, classes, _) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    # Bulunan obje bilgilerini kaydetme
    detect_infos = []
    for score, box, label in zip(scores[0], boxes[0], classes[0]):
        if score > MIN_SCORE_THRESH:
            detect_infos.append((
                label,
                # Koordinat verileri (y0, x0, y1, x1) şeklindedir (x0, y0, x1, y1 yapıyoruz)
                (box[1] * width, box[0] * height,
                 box[3] * width, box[2] * height)
            ))

    if visualize:
        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=4,
            min_score_thresh=MIN_SCORE_THRESH)

    # Resim, (etiket, koordinat)
    return detect_infos
