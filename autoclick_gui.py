import tkinter as tk
from tkinter import StringVar, messagebox
from autoclick import AutoClick
from pynput.keyboard import Listener, Key


"""
Python Auto Clicker GUI

NOTES:
        v1.4
        * Renamed modules and functions to be more "Pythonic"
        * Removed quit function redundancy
        * Minimize to tray when Start pressed
        * Changed versions to make more sense

        v1.3
        * Redesigned UI in OOP style
        * Change input values by pressing Start while clicking stopped
        * Escape key works in every fashion
        ---- time to close dependent on Click Interval, will try to fix
        * Window 'X' button works in every fashion
        * More exception handling
        * updated icon

        v1.2
        * Exception Handling
        * Implemented Quit via Escape key, kind of buggy (Fixed in v1.3)
        * Fixed performance issues

"""

vers = "v1.4"

keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
        "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


class AutoClickGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Auto Clicker")
        self.protocol("WM_DELETE_WINDOW", self.exit_program)

        width, height = 240, 220
        s_width, s_height = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (s_width/2) - (width/2)
        y = (s_height/2) - (height/2)

        self.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.resizable(0, 0)
        self.iconbitmap(r"icon2.ico")

        self.enable_key = StringVar()
        self.stop_key = StringVar()
        self.seconds = tk.DoubleVar()

        self.enable_key.set("z")
        self.stop_key.set("x")
        self.seconds.set(0.5)

        self.ac = AutoClick()
        self.ac.set_values(self.enable_key.get(),
                           self.stop_key.get(), self.seconds.get())

        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        self.set_widgets()
        self.mainloop()

    def on_press(self, key):
        if key == Key.esc:
            self.exit_program()

    def set_values(self):
        try:
            if self.seconds.get() > 0:
                self.ac.set_values(
                    self.enable_key.get(), self.stop_key.get(), self.seconds.get())
            else:
                messagebox.showwarning(
                    "An error occured", "Click Interval must be greater than zero!")

        except tk.TclError:
            messagebox.showwarning(
                "An error occured", "Make sure you enter a number for Click Interval!")

    def exit_program(self):
        self.ac.quit()
        self.destroy()

    def set_widgets(self):
        # LOGO:
        logo = tk.Label(
            self, text=f"Python Auto Clicker {vers}", font=("Arial, 12",))

        # Pack the logo at the top of the window
        logo.pack(pady=10, anchor="n")

        # use a Frame for grid objects (buttons, menus, etc.)
        frame = tk.Frame(self)
        frame.pack(expand=True)

        # OPTION MENU:  Set enable key
        enab_label = tk.Label(frame, text="Enable Key: ")
        enab_label.grid(column=0, row=1)
        enab_option = tk.OptionMenu(frame, self.enable_key, *keys)
        enab_option.grid(column=1, row=1)

        # OPTION MENU:  Set stop key
        stop_label = tk.Label(frame, text="Stop Key: ")
        stop_label.grid(column=0, row=2)
        stop_option = tk.OptionMenu(frame, self.stop_key, *keys)
        stop_option.grid(column=1, row=2)

        # TEXT ENTRY:  Set click interval
        interval_label = tk.Label(frame, text="Click Interval (sec): ")
        interval_label.grid(column=0, row=3, pady=10)
        interval_entry = tk.Entry(frame, width=8, textvariable=self.seconds)
        interval_entry.grid(column=1, row=3)

        # BUTTON:  Start the service
        enableButton = tk.Button(frame, text="Start",
                                 anchor='center', command=lambda: [self.wm_state("iconic"), self.ac.start_service(), self.set_values()])
        enableButton.grid(row=5, columnspan=3, pady=12, ipadx=20, ipady=5)


if __name__ == "__main__":
    AutoClickGUI()
