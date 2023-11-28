import datetime


class ScorePosition:
    """
    Represents a score position with a name, score, and date/time.
    """

    formatted_datetime = "%Y-%m-%d %H:%M:%S"

    def __init__(self, name: str, score: int, date_time: str = None) -> None:
        """
        Initializes a ScorePosition instance.

        Args:
            name (str): The name associated with the score.
            score (int): The score value.
            date_time (str, optional): The date/time string in the format "%Y-%m-%d %H:%M:%S".
                Defaults to current date/time.
        """
        if date_time is None:
            self.date_time = datetime.datetime.now()
        else:
            self.date_time = datetime.datetime.strptime(
                date_time, ScorePosition.formatted_datetime)

        self.name = name
        self.score = score

    def to_json(self):
        """
        Converts the ScorePosition instance to a JSON object.

        Returns:
            dict: The JSON representation of the ScorePosition instance.
        """
        return {
            "name": self.name,
            "score": self.score,
            "date_time": self.date_time.strftime(ScorePosition.formatted_datetime)
        }
