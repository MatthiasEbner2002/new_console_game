from pynput import keyboard
from pynput.keyboard import Key
import logging

class Input:
    def __init__(self, level):
        self.a = 0
        self.d = 0
        self.w = 0
        self.s = 0
        self.q = 0
        self.space = 0
        self.level = level
        
        # listener is a thread, so it will run in the background
        listener = keyboard.Listener(on_press=self.keyDown, on_release=self.keyUp)
        listener.start()
        
    
    def keyDown(self, key):
        """
        This function is used to handle key presses.

        Args:
            key : The key that was pressed.
        """
        
        match key:
            case keyboard.KeyCode(char='a'):
                self.a = 1 
            case keyboard.KeyCode(char='d'):
                self.d = 1
            case keyboard.KeyCode(char='w'):
                self.w = 1
            case keyboard.KeyCode(char='s'):
                self.s = 1
            case keyboard.KeyCode(char='q'):
                self.q = 1
                self.level.stop_game_and_exit()
            case Key.space:
                self.level.next_step_for_game()
                

    def keyUp(self, key):
        """
        This function is used to handle key releases.

        Args:
            key: The key that was released.
        """
        
        match key:
            case keyboard.KeyCode(char='a'):
                self.a = 0 
            case keyboard.KeyCode(char='d'):
                self.d = 0
            case keyboard.KeyCode(char='w'):
                self.w = 0
            case keyboard.KeyCode(char='s'):
                self.s = 0
            case Key.space:
                pass
            case default:
                logging.info(f"Key not recognized: {key}")
        