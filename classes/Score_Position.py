import datetime



class Score_Position:
    formatted_datetime = "%Y-%m-%d %H:%M:%S"
        
    def __init__(self, name: str, score: int, date_time:str=None) -> None:
        if date_time is None:
            self.date_time = datetime.datetime.now()
        else:
            self.date_time = datetime.datetime.strptime(date_time, Score_Position.formatted_datetime)
        
        self.name = name
        self.score = score
        
    def to_json(self):
        return {
            "name": self.name,
            "score": self.score,
            "date_time": self.date_time.strftime(Score_Position.formatted_datetime)
        }