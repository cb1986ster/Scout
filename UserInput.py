import threading

class UserInput(threading.Thread): # Interface for user
    def __init__(self,update_interval=0.05,callback=None,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.update_interval = update_interval
        self.__button_callback = callback

    def set_button_callback(self,callback):
        self.__button_callback = callback

    def running(self):return self.__running

    def run(self):
        self.__running = True
        while self.running:
            self.update()
            sleep(self.update_interval)

    def stop(self):
        self.__running = False
        self.join()

    def update(self,padNo=0):raise NotImplementedError
    @property
    def advance(self): raise NotImplementedError
    @property
    def sideway(self): raise NotImplementedError
    @property
    def turn(self): raise NotImplementedError
    @property
    def height(self): raise NotImplementedError
    @property
    def gx(self): raise NotImplementedError
    @property
    def gy(self): raise NotImplementedError

    @property
    def state(self):
        return self.advance, self.sideway, self.turn, self.height, self.gx, self.gy
