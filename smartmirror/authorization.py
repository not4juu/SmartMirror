import cv2
import os
import sys
import pickle
import face_recognition
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
"""


class Authorization:
    def __init__(self, camera, callback):
        self.camera = camera
        self.callback = callback
        self.detected = {}
        try:
            self.face_cascade = cv2.CascadeClassifier(PATH + '/../cascades/haarcascade_frontal_face_default.xml')
        except Exception as exception:
            print("Face Cascade Classifier reading file problem: {0}".format(exception))
            return

    def run_opencv_face_recognition(self):

        imagePaths = [f for f in os.listdir(PATH + '/../dataset')]
        tmp = 0
        faces_dic = {}

        for imagePath in imagePaths:
            if imagePath not in faces_dic.values():
                faces_dic[tmp] = imagePath
                tmp += 1

        minW = 0.1 * self.camera.get(3)
        minH = 0.1 * self.camera.get(4)

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(PATH + '/../trainer.yml')
        font = cv2.FONT_HERSHEY_SIMPLEX

        while True:
            ret, img = self.camera.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Check if confidence is less them 100 ==> "0" is perfect match
                if (confidence < 100):
                    id = faces_dic[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    self.add_detected_face(str(id))
                    self.callback(str(id))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cv2.imshow('camera', img)

            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break

    def run_dlib_face_recognition(self):
        data = pickle.loads(open(PATH + "/../encodings.pickle", "rb").read())
        while True:
            # grab the frame from the threaded video stream and resize it
            # to 500px (to speedup processing)
            ret, img = self.camera.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # convert the input frame from (1) BGR to grayscale (for face
            # detection) and (2) from BGR to RGB (for face recognition)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # detect faces in the grayscale frame
            rects = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(30, 30))

            # OpenCV returns bounding box coordinates in (x, y, w, h) order
            # but we need them in (top, right, bottom, left) order, so we
            # need to do a bit of reordering
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding)
                name = "Unknown"

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                # update the list of names
                names.append(name)

            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image
                cv2.rectangle(img, (left, top), (right, bottom),
                              (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                self.callback(name)
                cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 255, 0), 2)
            if name != "Unknown":
                self.add_detected_face(name)
            # display the image to our screen
            cv2.imshow("Frame", img)
            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
        pass

    def add_detected_face(self, name):
        if name in self.detected:
            self.detected[name] += 1
            print("jest {0}".format(self.detected[name]))
        else:
            print("nie ma")
            self.detected[name] = 1
        self.recognition_confidence()

    def recognition_confidence(self):
        if 10 in self.detected.values():
            print("confidence")


def fun_callback(name):
    print("detected {0}".format(name))


if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)  # set video widht
    camera.set(4, 480)  # set video height
    test = Authorization(camera, fun_callback)
    test.run_opencv_face_recognition()
    #test.run_dlib_face_recognition()
    camera.release()
    cv2.destroyAllWindows()
    pass
