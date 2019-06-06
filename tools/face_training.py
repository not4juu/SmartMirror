from imutils import paths
import cv2
import face_recognition
import os
import sys
import pickle


PATH = os.path.dirname(os.path.realpath(__file__))
DATASET_PATH = PATH + '/../dataset'
if sys.platform != 'linux':
    PATH = PATH.replace("\\", '/')

running_console_bar = ['.', '..', '...', '....', '.....']


def face_recognition_training():
    known_encodings = []
    known_names = []

    image_paths = list(paths.list_images(DATASET_PATH))
    items = 0
    model = 'hog'  # available also 'cnn' https://face-recognition.readthedocs.io/en/latest/face_recognition.html
    print("Starts face recognition training with model: {0}".format(model))
    for (i, image_path) in enumerate(image_paths):
        name = image_path.split(os.path.sep)[-2]
        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=model)
        encodings_data = face_recognition.face_encodings(rgb, boxes)

        for encoding_sample in encodings_data:
            known_encodings.append(encoding_sample)
            known_names.append(name)

        print('\r {0}'.format(running_console_bar[items % len(running_console_bar)]), end="")
        items += 1

    print("Faces encoding data ends, items: {0}".format(items))
    data = {"encodings": known_encodings, "names": known_names}
    file = open(PATH + "/../encodings.pickle", "wb")
    file.write(pickle.dumps(data))
    file.close()
    print("Face recognition training ends successfully")


if __name__ == "__main__":
    face_recognition_training()
