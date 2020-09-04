from UserInput import UserInput

from inputs import get_gamepad

class JoystickInput(UserInput):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.__x = 127
        self.__y = 127
        self.__r = 127
        self.__z = 127
        self.__gx = 0.
        self.__gy = 0.
        self.button_down = set()

    def run(self):
        no_to_button = (
            'BTN_TRIGGER','BTN_THUMB','BTN_THUMB2','BTN_TOP','BTN_TOP2','BTN_PINKIE',
            'BTN_BASE','BTN_BASE2','BTN_BASE3','BTN_BASE4','BTN_BASE5','BTN_BASE6'
        )
        button_to_no = { btn:no for no,btn in enumerate(no_to_button) }
        while self.running:
            events = get_gamepad()
            for event in events:
                if event.code == "ABS_X": self.__x = event.state
                elif event.code == "ABS_Y": self.__y = event.state
                elif event.code == "ABS_Z": self.__z = event.state
                elif event.code == "ABS_RZ":  self.__r = event.state
                elif event.code == "ABS_HAT0X": self.__gx += event.state * 0.15
                elif event.code == "ABS_HAT0Y": self.__gy += event.state * 0.15
                elif event.code in no_to_button:
                    try:
                        if event.state == 1:
                            self.button_down.add(button_to_no[event.code])
                        else:
                            self.button_down.remove(button_to_no[event.code])
                    except Exception:pass
                # else: print(event.ev_type, event.code, event.state)

    @property
    def advance(self): return -(self.__y-127)/128

    @property
    def sideway(self): return (self.__x-127)/128

    @property
    def turn(self): return (self.__r-127)/128

    @property
    def height(self): return (self.__z-127)/128

    @property
    def gx(self): return self.__gx

    @property
    def gy(self): return self.__gy


if __name__ == '__main__':
    from time import sleep
    import sys
    joy = JoystickInput()
    joy.start()
    try:
        while 1:
            print("\r"," "*40,"\r",joy.advance, joy.sideway, joy.turn,end="")
            sys.stdout.flush()
            sleep(0.1)
    except KeyboardInterrupt:pass
    joy.stop()
