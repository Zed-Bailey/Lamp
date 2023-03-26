
from web_cam import WebCam
from microphone import Microphone
from hardware_control import HardwareController
import threading
from dotenv import load_dotenv
import os
import pvporcupine

import cv2

load_dotenv()

# https://stackoverflow.com/questions/14140495/how-to-capture-a-video-and-audio-in-python-from-a-camera-or-webcam

shutdown_event = threading.Event()

hardwareController = HardwareController()

accessKey = os.getenv("PICO_CONSOLE_KEY")
rhino = os.getenv("RHINO_CONTEXT_FILE")
# porcupine = os.getenv("PORCUPINE_KEYWORD_FILE")
porcupine = pvporcupine.KEYWORD_PATHS['blueberry']

print(porcupine)

mic_thread = Microphone(
    accessKey,
    porcupine,
    rhino,
    hardwareController,
    # may be required for raspberry pi
    # -1 uses default microphone
    # audio_device_index=1,
    # audio_device_index=-1
)
mic_thread.show_audio_devices()

# cam_thread = WebCam()
# cam_thread.start(shutdown_event)

mic_thread.start(shutdown_event)


# shutdown_event.wait()

input("press enter to shutdown threads\n")

shutdown_event.set()


# cam_thread.join()
mic_thread.join()

hardwareController.cleanup()

print("done")

