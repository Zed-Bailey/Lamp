import cv2
import mediapipe as mp
from threading import Thread, Event
import time
import queue

class WebCam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.thread: Thread
        self.last_time = 0
        self.isStopped = False



    def startCapture(self, event: Event, debug:bool=False):
        """
        event: when using this function in a multithreaded instance, trigger the veent to close the camera
        debug: as cv2 cant show images in a multithreaded process and requires lots of fiddling with queues.
        if not running this function in a thread set debug to True and webcam capture will be shown in a window

        """
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
    
        with mp_face_detection.FaceDetection(
            # min_detection_confidence = Minimum confidence value ([0.0, 1.0]) 
            # from the face detection model for the detection to be considered successful. 
            # Default to 0.5.
            model_selection=0, min_detection_confidence=0.6
        ) as face_detection:
            while self.cap.isOpened():
                
                if self.isStopped or event.is_set():
                    break

                success, image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_detection.process(image)

                
                
                if results.detections:
                    print(f"{len(results.detections)} faces detected")
                else:
                    print("no face \(•_•)/")

                # if debug:
                #     # Draw the face detection annotations on the image.
                #     image.flags.writeable = True
                #     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                #     if results.detections:
                #         for detection in results.detections:
                #             mp_drawing.draw_detection(image, detection)
                #     # Flip the image horizontally for a selfie-view display.
                #     cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
                #     if cv2.waitKey():
                #         break

        self.cap.release()
    
    def start(self, event: Event):
        self.thread = Thread(target=self.startCapture, args=(event,))
        self.thread.start()
    
    
    def join(self):
        self.thread.join()

    def stop(self):
        self.isStopped = True
        pass