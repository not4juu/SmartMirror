from argparse import ArgumentParser
from imutils import paths
from PIL import Image
import pickle
import numpy as np
import cv2
import face_recognition
import os
import sys

PATH = os.path.dirname(os.path.realpath(__file__))
if sys.platform != 'linux':
    PATH = PATH.replace("\\", '/')

IMAGES_PATHS = list(paths.list_images(PATH + '/../dataset'))

running_console_bar = ['.', '..', '...', '....', '.....']


def face_recognition_training():
    known_encodings = []
    known_names = []

    items = 0
    model = 'hog'  # available also 'cnn' https://face-recognition.readthedocs.io/en/latest/face_recognition.html
    print("Starts face recognition training with model: {0}".format(model))

    for (i, image_path) in enumerate(IMAGES_PATHS):
        sample_name = image_path.split(os.path.sep)[-2]
        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=model)
        encodings_data = face_recognition.face_encodings(rgb, boxes)

        for encoding_sample in encodings_data:
            known_encodings.append(encoding_sample)
            known_names.append(sample_name)

        print('\r {0}'.format(running_console_bar[items % len(running_console_bar)]), end="")
        items += 1

    print("Faces encoding data ends, items: {0}".format(len(known_names)))
    data = {"encodings": known_encodings, "names": known_names}
    file = open(PATH + "/../trained_data/encodings.pickle", "wb")
    file.write(pickle.dumps(data))
    file.close()
    print("Face recognition training ends successfully")


def face_opencv_training():
    known_encodings = []
    known_names = []

    faces_detected = {}
    ids_number = 0

    recognizer = cv2.face.LBPHFaceRecognizer_create()  # https://docs.opencv.org/3.4/d4/d48/namespacecv_1_1face.html
    detector = cv2.CascadeClassifier(PATH + '/../cascades/haarcascade_frontal_face_default.xml')
    print("Starts face opencv training")

    for image_path in IMAGES_PATHS:
        sample_name = image_path.split(os.path.sep)[-2]

        if sample_name not in faces_detected.keys():
            faces_detected[sample_name] = ids_number
            ids_number += 1

        pil_image = Image.open(image_path).convert('L')  # convert it to grayscale
        numpy_image = np.array(pil_image, 'uint8')

        faces = detector.detectMultiScale(numpy_image)

        for (x, y, width, height) in faces:
            known_encodings.append(numpy_image[y: y + height, x: x + width])
            known_names.append(faces_detected[sample_name])

    print("Faces encoding data ends, items: {0}".format(len(known_names)))
    print("\n Training  ... {0}".format(faces_detected))
    recognizer.train(known_encodings, np.array(known_names))
    recognizer.write(PATH + '/../trained_data/trainer.yml')
    print("Face opencv training ends successfully")


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="smartmirror face_training",
        description="Smart Mirror tools to train collected image samples",
        epilog="more detailed information in README.md file https://github.com/not4juu/SmartMirror"
    )
    parser.add_argument("-t", "--training_method", type=str, default="face_recognition",
                        help="training method to use: face_recognition or face_opencv")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    args = parser.parse_args()

    if not os.path.exists(PATH + '/../trained_data/'):
        os.makedirs(PATH + '/../trained_data/')

    if args.training_method == "face_recognition":
        face_recognition_training()
    elif args.training_method == "face_opencv":
        face_opencv_training()
