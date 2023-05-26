from pynput import keyboard
from pynput.keyboard import Key
import logging

class Input:
    def __init__(self, render_what):
        self.render_what = render_what
        self.a = 0
        self.d = 0
        self.w = 0
        self.s = 0
        self.space = 0
        listener = keyboard.Listener(on_press=self.keyDown, on_release=self.keyUp)
        listener.start()
        
    
    def keyDown(self, key):
        match key:
            case keyboard.KeyCode(char='a'):
                self.a = 1 
            case keyboard.KeyCode(char='d'):
                self.d = 1
            case keyboard.KeyCode(char='w'):
                self.w = 1
            case keyboard.KeyCode(char='s'):
                self.s = 1
            case Key.space:
                self.space += 1

    def keyUp(self, key):
        match key:
            case keyboard.KeyCode(char='a'):
                self.a = 0 
            case keyboard.KeyCode(char='d'):
                self.d = 0
            case keyboard.KeyCode(char='w'):
                self.w = 0
            case keyboard.KeyCode(char='s'):
                self.s = 0
            case default:
                logging.info(f"Input.py | keyUp(): Key not recognized: {key}")
        