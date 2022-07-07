from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key
import time
import threading


class AutoClick(threading.Thread):

    mouse = Controller()

    def __init__(self):
        super().__init__()
        self.start()  # Start a thread for the Class instance

        self.program_running = False
        self.clicking = False

        self.e = threading.Event()
        self.e.clear()

        # Start a Thread for mouse clicking, control via Thread Event
        self.t1 = threading.Thread(target=self.start_loop, args=())

        # Initialize a Keyboard Listener
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        print('\n\n[Python AutoClickApp Initialized.]')

    # Quit function to wrap up Threads and exit
    def quit(self):
        print("\nEscape key pressed.\n[Exiting Program]\n")
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

    # Called from GUI to set input values
    def set_values(self, enable_key, stop_key, seconds):
        if not self.clicking:
            self.enable_key = KeyCode(char=enable_key)
            self.stop_key = KeyCode(char=stop_key)
            self.seconds = seconds

            if self.program_running == True:
                print(
                    f'\n[VALUES SET]\nENABLE_KEY: {self.enable_key}\nSTOP_KEY: {self.stop_key}\nINTERVAL: {self.seconds}')

    # Called when Start button clicked
    def start_service(self):
        if not self.t1.is_alive():
            self.program_running = True
            self.t1.start()

    # Keyboard Listener controls
    def on_press(self, key):
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

    # Start Click Loop, control with thread event trigger
    def start_loop(self):
        print("\n[Auto Clicker Running]\nPress Escape to quit program.\n")

        self.e.wait()

        while self.program_running:
            while self.clicking:
                AutoClick.mouse.click(Button.left)
                time.sleep(self.seconds)
            time.sleep(0.1)
