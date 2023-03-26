import threading
# import gpiozero

class HardwareController:

    def __init__(self) -> None:
        self.lock = threading.Lock()
        
        # true when light is open, false otherwise
        self.openState = False
        
        # true when light is on, false otherwise
        self.lightOnState = False
        
        # https://gpiozero.readthedocs.io/en/stable/api_output.html#gpiozero.RGBLED
        # self.led = gpiozero.RGBLED(23,24,25)

    """
    the webcam and voice control both have access to the same instance of the hardware control
    class. should i use a thread lock so that only 1 thread can control the gpio pins at one time
    
    the webcam control should only have access to 
        - closing and turning off the light
    
    the voice control should have access to
        - changing light colour
        - turn light off
        - close light
        - turn light on
        - open light

    
    should voice control only be able to open light after webcam has finished closing the light
        
    """

    def cleanup(self):
        # self.led.close()
        pass

    def toggleLightOpenClose(self):
        self.lock.acquire()
        try:
            self.openState = not self.openState
            # TODO: move servos based on new state
        finally:
            self.lock.release()

    def turnLightOnOff(self, on: bool = False, off=False):
        """
        on: set to True to turn light on, false to turn it off
        """
        print("awaiting lock")
        self.lock.acquire()
        try:
            print("acquired lock")
            # turns led on when it is off
            # if on and not self.led.is_lit:
            #     self.led.on()
            # # turn led off when it's on
            # elif off and self.led.is_lit:
            #     self.led.off()

            # self.lightOnState = self.led.is_lit

            print(f"light on = {self.lightOnState}")
            # TODO: toggle light on/off based on new state
        finally:
            print("lock released")
            self.lock.release()