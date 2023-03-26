from threading import Thread, Event
from picovoice import *
from pvrecorder import PvRecorder
import sys
import wave
import struct
import pvrhino
from hardware_control import HardwareController

class Microphone:
    def __init__(self, 
            accessKey,
            porcupineKeywordPath,
            rhinoContextPath,
            hardwareController: HardwareController,
            audio_device_index = 0,
            porcupine_sensitivity=0.5,
            rhino_sensitivity=0.5,
            endpoint_duration_sec=1.,
            require_endpoint=True
        ):
        self.thread:Thread
        
        self.hardwareController = hardwareController

        self.audio_device_index = audio_device_index
        self.shutdown_event: Event
        self._picovoice = Picovoice(
                access_key=accessKey,
                keyword_path=porcupineKeywordPath,
                wake_word_callback=self._wake_word_callback,
                context_path=rhinoContextPath,
                inference_callback=self._inference_callback,
                porcupine_sensitivity=porcupine_sensitivity,
                rhino_sensitivity=rhino_sensitivity,
                endpoint_duration_sec=endpoint_duration_sec,
                require_endpoint=require_endpoint
        )



    def capture(self, event: Event):
        """
        """
        # listen for shutdown command, toggle event
        recorder = None
        
        try:
            # frame_length=self._picovoice.frame_length
            recorder = PvRecorder(device_index=self.audio_device_index, frame_length=512)
            recorder.start()

            print("Using device: %s" % recorder.selected_device)
            print('[Listening ...]')

            while True:
                pcm = recorder.read()

                self._picovoice.process(pcm)

                if event.is_set():
                    break

        except KeyboardInterrupt:
            sys.stdout.write('\b' * 2)
            print('Stopping ...')
        finally:
            print('Cleaning up ...')
            if recorder is not None:
                recorder.delete()

            self._picovoice.delete()


    @classmethod
    def show_audio_devices(cls):
        devices = PvRecorder.get_audio_devices()

        for i in range(len(devices)):
            print('index: %d, device name: %s' % (i, devices[i]))

    # @staticmethod
    def _wake_word_callback(self):
        print('[wake word]\n')
        # toggle light to show wake word detected?

    # @staticmethod
    def _inference_callback(self, inference: pvrhino.Rhino.Inference):
        
        if inference.is_understood:
            print('{')
            print("  intent : '%s'" % inference.intent)
            print('  slots : {')
            for slot, value in inference.slots.items():
                print("    %s : '%s'" % (slot, value))
            print('  }')
            print('}\n')

            if inference.intent == 'changeLightState':
                if inference.slots['state'] == 'off':
                    print("turning light off")
                    self.hardwareController.turnLightOnOff(off=True)
                if inference.slots['state'] == 'on':
                    print("turning light on")
                    self.hardwareController.turnLightOnOff(on=True)
                    
        else:
            print("Didn't understand the command.\n")


    def start(self, event:Event):
        self.shutdown_event = event
        self.thread = Thread(target=self.capture, args=(event,))
        self.thread.start()
        

    def join(self):
        self.thread.join()
    
    def stop(self):
        pass