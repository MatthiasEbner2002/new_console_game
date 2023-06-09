from pynput import keyboard
from pynput.keyboard import Key
import logging

class Input:
    def __init__(self, level, max_power=25):
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
        self.space = 0
        self.q = 0
        self.w = 0
        self.level = level
        
        self.show_info: bool = False
        self.max_line_count = 0 # max lines that can be shown
        self.line_position = 0 # actual position in the lines
        self.lines_count = 0 # how many lines exist
        
        self.angle = 0
        self.power = 0
        self.max_power = max_power
        
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
            case keyboard.KeyCode(char='i'):
                logging.debug("i was pressed ")
                self.show_info = not self.show_info
            
            case Key.up:
                if self.show_info:
                    if self.line_position < self.lines_count - self.max_line_count:
                        self.line_position += 1
                else:
                    self.up = 1
                    self.angle += 5
                    
                    
            case Key.down:
                if self.show_info:
                    if self.line_position > 0:
                        self.line_position -= 1
                else:
                    self.down = 1
                    self.angle -= 5
                
            case Key.left:
                if self.power > 0:
                    self.power -= 1
            case Key.right:
                self.right = 1
                if self.power < self.max_power:
                    self.power += 1
            case keyboard.KeyCode(char='q'):
                self.q = 1
                self.level.stop_game_and_exit()
            case Key.space:
                self.level.next_step_for_game()
        
        self.angle %= 360
        
                

    def keyUp(self, key):
        """
        This function is used to handle key releases.

        Args:
            key: The key that was released.
        """
        
        match key:
            case Key.up:
                self.up = 0
            case Key.down:
                self.down = 0
            case Key.left:
                self.left = 0
            case Key.right:
                self.right = 0
            case Key.space:
                pass
            case default:
                logging.info(f"Key not recognized: {key}")
    
    
    def update_info_input(self, max_line_count: int, lines: int):
        self.max_line_count = max_line_count
        self.lines_count = lines
        
        if self.line_position + max_line_count > self.lines_count:
            self.line_position = self.lines_count - self.max_line_count