import logging

from pynput import keyboard
from pynput.keyboard import Key
from classes.Score_Manager import Score_Manager
from classes.Score_Position import Score_Position

class Input:
    def __init__(self, level, max_power: int=25):
        self.disable_input: bool = False    # disable input or not
        self.level = level
        self.score_manager: Score_Manager = Score_Manager()
        self.score: int = 0                 # Score, the Points
        
        self.cheats: bool        = False    # cheats enabled or not
        self.show_info: bool     = False    # show info or not
        self.max_line_count: int = 0        # max lines that can be shown
        self.line_position: int  = 0        # actual position in the lines
        self.lines_count: int    = 0        # how many lines exist
        self.get_name: bool      = False    # get name for highscore 
        
        self.angle: int = 0
        self.power: int = 0
        
        self.max_power:int  = max_power
        
        
        # listener is a thread, so it will run in the background
        listener = keyboard.Listener(on_press=self.keyDown, on_release=self.keyUp)
        listener.start()
        
    
    def keyDown(self, key):
        """
        This function is used to handle key presses.

        Args:
            key : The key that was pressed.
        """
        
        if self.disable_input:
            return
        
        match key:
            case Key.up:
                if self.show_info:
                    if self.line_position > 0:
                        self.line_position -= 1
                else:
                    self.up = 1
                    self.angle += 5
                    
            case Key.down:
                if self.show_info:
                    if self.line_position < self.lines_count - self.max_line_count:
                        self.line_position += 1
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
            
            case Key.space:
                self.level.next_step_for_game()
                
            case keyboard.KeyCode(char='i'):
                self.show_info = not self.show_info
            
            case keyboard.KeyCode(char='q'):
                self.q = 1
                self.show_info = False
                self.level.stop_game_and_exit()
            
            case keyboard.KeyCode(char='c'):
                self.cheats = not self.cheats
        
            case keyboard.KeyCode(char='s'):
                # self.score_manager.add_score(Score_Position("Test", self.score))
                self.get_name = True
        self.angle %= 360
        
                

    def keyUp(self, key):
        """
        This function is used to handle key releases.

        Args:
            key: The key that was released.
        """
        if self.disable_input:
            return
        
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
            #case default:
            #    logging.info(f"Key not recognized: {key}")
    
    
    def update_info_input(self, max_line_count: int, lines: int):
        self.max_line_count = max_line_count
        self.lines_count = lines
        
        if self.line_position + max_line_count > self.lines_count:
            self.line_position = max(0, self.lines_count - self.max_line_count)
            
            
    def add_score(self, score_position: Score_Position):
        self.score_manager.add_score(score_position)