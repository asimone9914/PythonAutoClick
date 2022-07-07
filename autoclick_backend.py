from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key
import time
import threading

"""
Python Auto Clicker Backend

"""

mouse = Controller()


class AutoClickApp(threading.Thread):
    def __init__(self):
        super().__init__()
        self.start()  # Start a thread for the Class instance

        self.program_running = False
        self.clicking = False

        self.e = threading.Event()
        self.e.clear()

        # Start a Thread for mouse clicking, control via Thread Event
        self.t1 = threading.Thread(target=self.start_clicking, args=())

        # Initialize a Keyboard Listener
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        print('\n\n[Python AutoClickApp Initialized.]')

    # Quit function to wrap up Threads and exit backend
    def quit(self):
        try:
            self.clicking = False
            self.program_running = False
            self.e.set()
            self.t1.join()
            self.join()
        except:
            self.clicking = False
            self.program_running = False
            self.join()

    # the enable function is called from the GUI
    def setValues(self, enable_key, stop_key, seconds):
        if not self.clicking:
            self.enable_key = KeyCode(char=enable_key)
            self.stop_key = KeyCode(char=stop_key)
            self.seconds = seconds
            print(
                f'\n[VALUES SET]\nENABLE_KEY: {self.enable_key}\nSTOP_KEY: {self.stop_key}\nINTERVAL: {self.seconds}')

    def startService(self):
        if not self.t1.is_alive():
            self.program_running = True
            self.clicking = True
            self.t1.start()

    # Keyboard Listener controls
    def on_press(self, key):
        if key == Key.esc:
            self.quit()

        if self.program_running:
            if key == self.enable_key:
                if not self.e.is_set():

                    print(
                        f'\n[Clicking Enabled]\nPress {self.stop_key} to stop.')

                    self.e.set()
                    self.clicking = True

            elif key == self.stop_key:
                if self.e.isSet() and self.t1.is_alive():

                    print(
                        f'\n[Clicking Stopped]\nPress {self.enable_key} to resume.')

                    self.e.clear()
                    self.clicking = False

    # Start Mouse Clicking
    def start_clicking(self):
        print("\n[Auto Clicker Running]\nPress Escape to quit program.")

        self.e.wait()

        while self.program_running:
            while self.clicking:
                mouse.click(Button.left)
                time.sleep(self.seconds)
            time.sleep(0.1)
