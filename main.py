
from web_cam import WebCam
from microphone import Microphone
import threading
from dotenv import load_dotenv
import os
import pvporcupine

import cv2

load_dotenv()

# https://stackoverflow.com/questions/14140495/how-to-capture-a-video-and-audio-in-python-from-a-camera-or-webcam

shutdown_event = threading.Event()

accessKey = os.getenv("PICO_CONSOLE_KEY")
rhino = os.getenv("RHINO_CONTEXT_FILE")
porcupine = pvporcupine.KEYWORD_PATHS['blueberry']
debug = True

print(porcupine)

mic_thread = Microphone(
    accessKey,
    porcupine,
    rhino,
)

mic_thread.show_audio_devices()

# cam_thread = WebCam()
# cam_thread.start(shutdown_event)

mic_thread.start(shutdown_event)


# shutdown_event.wait()

input("press enter to shutdown threads")

shutdown_event.set()


# cam_thread.join()
mic_thread.join()

print("done")

