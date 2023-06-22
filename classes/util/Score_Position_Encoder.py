"""
Module: Score_Position_Encoder
Custom JSON encoder for ScorePosition objects.
"""

import json
from classes.Score_Position import ScorePosition


class Score_Position_Encoder(json.JSONEncoder):
    """
    Custom JSON encoder for ScorePosition objects.
    """

    def default(self, obj):
        """
        Convert ScorePosition object to a dictionary for JSON serialization.

        Args:
            obj (ScorePosition): The ScorePosition object to encode.

        Returns:
            dict: The dictionary representation of the ScorePosition object.
        """
        if isinstance(obj, ScorePosition):
            return {
                "name": obj.name,
                "score": obj.score,
                "date_time": obj.date_time.strftime(ScorePosition.formatted_datetime)
            }
        return super().default(obj)
