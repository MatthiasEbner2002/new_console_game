import json
from classes.Score_Position import Score_Position


class Score_PositionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Score_Position):
            # Convert Score_Position object to a dictionary
            return {
                "name": obj.name,
                "score": obj.score,
                "date_time": obj.date_time.strftime(Score_Position.formatted_datetime)
            }
        return super().default(obj)