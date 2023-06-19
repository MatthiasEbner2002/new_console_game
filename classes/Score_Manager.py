import logging, json, atexit
from classes.util.File_util import File_util
from classes.Score_Position import Score_Position

class Score_Manager:
    
    def __init__(self, score_path=None) -> None:
        self.file_util: File_util = None
        self.file_util: File_util = File_util(score_path)

        self.live_score = 0

        self.highscore_top_10 = []
        self.score_last_100 = []
        
        self.get_score_last_100_from_raw_data()
        self.get_highscore_top_10_from_raw_data()   
        atexit.register(self.write_into_file)   # register exit handler   
        
    def get_highscore_top_10_from_raw_data(self):
        """
        Get highscore top 10, from File_util.raw_data
        """
        
        logging.info("Getting highscore top 10")      
        raw_data = self.file_util.data_raw
        raw_highscore_top_10 = raw_data['highscore_top_10']
        for raw_score_position in raw_highscore_top_10:
            self.highscore_top_10.append(Score_Position(raw_score_position['name'], raw_score_position['score'], raw_score_position['date_time']))

    def get_score_last_100_from_raw_data(self):
        """
        Get score last 100, from File_util.raw_data
        """
        
        logging.info("Getting score last 100")      
        raw_data = self.file_util.data_raw
        raw_score_last_100 = raw_data['score_last_100']
        for raw_score_position in raw_score_last_100:
            self.score_last_100.append(Score_Position(raw_score_position['name'], raw_score_position['score'], raw_score_position['date_time']))
            
    def write_into_file(self):
        """
        Write data into file
        """ 
        logging.info("Writing data into file: Saving highscore top 10 and score last 100")
        json_data = {
            "highscore_top_10": self.highscore_top_10,
            "score_last_100": self.score_last_100
        }
        self.file_util.create_file_with_content(json_data)

    def add_score(self, score: Score_Position):
        logging.info("Adding score: " + str(score.score))
        self.add_score_to_top_10(score)
        self.add_score_to_last_100(score)
        

    def add_score_to_last_100(self, score: Score_Position):
        self.score_last_100.insert(0, score)
        if len(self.score_last_100) > 100:
            self.score_last_100 = self.score_last_100[:100]
            
    def add_score_to_top_10(self, score: Score_Position):
        if len(self.highscore_top_10) == 0:
            self.highscore_top_10.append(score)
            return
        
        if self.highscore_top_10[len(self.highscore_top_10) - 1].score >= score.score:
            self.highscore_top_10.append(score)
        else:  
            for i in range(len(self.highscore_top_10)):
                if score.score > self.highscore_top_10[i].score:
                    self.highscore_top_10.insert(i, score)
                    break
                

        if len(self.highscore_top_10) > 10:
            self.highscore_top_10 = self.highscore_top_10[:10]