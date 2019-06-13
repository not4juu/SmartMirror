import cv2
import os
import sys
import pickle
import face_recognition
import threading
import smartmirror.Logger as Logger

PATH = os.path.dirname(os.path.realpath(__file__))
if sys.platform != 'linux':
    PATH = PATH.replace("\\", '/')

"""
    Authorization Class

    - authorization is based on face recognition method
    - two options available :
        1. opencv face lib
        2. face_recognition (dlib)
    - name_id is collected by a folder name where person images are located
"""


class Authorization:
    def __init__(self, camera, callback):
        self.camera = camera
        self.callback = callback
        self.thread_running = False
        self.authorization_running = False

        self.debug = False
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.detected = {}
        self.samples_confidence = 20

        self.min_width = 0.1 * self.camera.get(3)
        self.min_height = 0.1 * self.camera.get(4)

        try:
            self.face_cascade = cv2.CascadeClassifier(PATH + '/../cascades/haarcascade_frontal_face_default.xml')
        except Exception as exception:
            print("Face Cascade Classifier reading file problem: {0}".format(exception))
            return

    def run_opencv_face_recognition(self):

        folders_name = [f for f in os.listdir(PATH + '/../dataset')]
        tmp = 0
        faces_dic = {}

        for name_id in folders_name:
            if name_id not in faces_dic.values():
                faces_dic[tmp] = name_id
                tmp += 1

        recognizer = cv2.face.LBPHFaceRecognizer_create()  # https://docs.opencv.org/3.4/d4/d48/namespacecv_1_1face.html
        recognizer.read(PATH + '/../trained_data/trainer.yml')

        while self.thread_running and self.authorization_running:
            response, image = self.camera.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            detected_face_square = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5,
                                                                      minSize=(int(self.min_width), int(self.min_height)))
            for (x, y, width, height) in detected_face_square:

                cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

                name_id, confidence = recognizer.predict(gray[y:y + height, x:x + width])
                recognition_name = "unknown"

                if(confidence < 100):
                    recognition_name = faces_dic[name_id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    self.add_detected_face(str(recognition_name))
                else:
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(image, str(recognition_name), (x + 5, y - 5), self.font, 1, (255, 255, 255), 1)
                cv2.putText(image, str(confidence), (x + 5, y + height - 5), self.font, 1, (255, 255, 255), 1)

            if self.debug:
                cv2.imshow('Authorization detected', image)
                cv2.waitKey(10)

    def run_dlib_face_recognition(self):
        data = pickle.loads(open(PATH + "/../trained_data/encodings.pickle", "rb").read())

        while self.thread_running and self.authorization_running:

            response, image = self.camera.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            detected_face_square = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                                                      minSize=(int(self.min_width), int(self.min_height)))

            boxes = [(y, x + width, y + height, x) for (x, y, width, height) in detected_face_square]

            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []
            recognition_name = "Unknown"

            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"], encoding)

                if True in matches:
                    matched_index = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    for i in matched_index:
                        recognition_name = data["names"][i]
                        counts[recognition_name] = counts.get(recognition_name, 0) + 1

                    recognition_name = max(counts, key=counts.get)
                names.append(recognition_name)

            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(image, name, (left, y), self.font, 1, (255, 255, 255), 1)

            if recognition_name != "Unknown":
                self.add_detected_face(recognition_name)

            if self.debug:
                cv2.imshow('Authorization detected', image)
                cv2.waitKey(10)

    def add_detected_face(self, name):
        Logger.logging.debug("Detected {0}".format(name))
        if name in self.detected:
            self.detected[name] += 1
        else:
            self.detected[name] = 1
        self.recognition_confidence()

    def recognition_confidence(self):
        Logger.logging.debug("Authorization confidence {0}".format(self.detected))
        if self.samples_confidence in self.detected.values():
            Logger.logging.debug("Authorization confidence {0}".format(self.samples_confidence))
            self.authorization_running = False
            for name, confidence in self.detected.items():
                if self.samples_confidence == confidence:
                    self.callback(name)

    def run(self, method='opencv_face_recognition', debug=False):
        Logger.logging.debug("Start authorization thread: {0}".format(method))
        self.thread_running = True
        self.authorization_running = True
        self.debug = debug
        if method is 'opencv_face_recognition':
            target = self.run_opencv_face_recognition
        if method is 'dlib_face_recognition':
            target = self.run_dlib_face_recognition

        listener_thread = threading.Thread(target=target)
        listener_thread.daemon = True
        listener_thread.start()

    def stop(self):
        Logger.logging.debug("Stop authorization thread")
        self.thread_running = False


if __name__ == "__main__":
    pass
