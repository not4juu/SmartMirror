import cv2
import os


class FaceSampleCollector:
    def __init__(self):

        self.frame = None
        self.gray = None
        self.samples_number = 10
        self.cascades_number = 3
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise NameError
        except cv2.error as exception:
            print("OpenCV camera hardware problem: {0}".format(exception))
            exit(1)
        except Exception as exception:
            print("Camera hardware is not connected: {0}".format(exception))
            exit(1)

        try:
            self.face_cascade = cv2.CascadeClassifier('../cascades/haarcascade_frontal_face_default.xml')
            self.eye_cascade = cv2.CascadeClassifier('../cascades/haarcascade_eye.xml')
            self.smile_cascade = cv2.CascadeClassifier('../cascades/haarcascade_smile.xml')
        except Exception as exception:
            print("Camera hardware is not connected: {0}".format(exception))
            return None

    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def run_sample_collector(self):
        self.face_id = input('\n Enter user id end press <enter> ==>  ')
        faced_detected = 0
        directory = 'dataset/' + str(self.face_id)
        if not os.path.exists(directory):
            os.makedirs(directory)

        while faced_detected < self.samples_number * self.cascades_number:

            response, self.frame = self.camera.read()
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            detection_square = self.detection_option(faced_detected)

            for (x, y, width, height) in detection_square:
                cv2.rectangle(self.frame, (x, y), (x + width, y + height), (255, 0, 0), 2)

            if len(detection_square) != 0:
                detection_square_1 = self.face_cascade.detectMultiScale(
                    self.gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))

                for (x, y, width, height) in detection_square_1:
                    cv2.rectangle(self.frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                    cv2.imwrite(str(directory) + '/' + str(faced_detected) + ".jpg",
                                self.gray[y:y + height, x:x + width])

                faced_detected += 1

            cv2.putText(self.frame,
                        'Detected: ' + str(faced_detected) + "/" + str(self.samples_number * self.cascades_number),
                        (10, int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT) - 30)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('image', self.frame)

            cv2.waitKey(500)

    def detection_option(self, number):
        detection = None
        if number in range(0, self.samples_number):
            detection = self.face_cascade.detectMultiScale(self.gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
            self.display_method_text('Please look at camera')
            print("get face_detection sample {0}".format(number))
        if number in range(self.samples_number, self.samples_number * 2):
            detection = self.eye_cascade.detectMultiScale(self.gray, scaleFactor=1.5, minNeighbors=10, minSize=(5, 5))
            self.display_method_text('Please look at camera')
            print("get eye_detection sample {0}".format(number))
        if number in range(self.samples_number * 2, self.samples_number * self.cascades_number):
            detection = self.smile_cascade.detectMultiScale(self.gray, scaleFactor=1.5, minNeighbors=15, minSize=(25, 25))
            self.display_method_text('Please smile :)')
            print("get smile_detection sample {0}".format(number))

        return detection

    def display_method_text(self, text):
        cv2.putText(self.frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)


if __name__ == "__main__":
    collector = FaceSampleCollector()
    collector.run_sample_collector()





