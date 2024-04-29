import json
import os
import logging

from classes.util.Score_Position_Encoder import Score_Position_Encoder


class File_util():
    default_score_file_path = "save_data/score.json"
    default_data = {
        "highscore_top_10": [],
        "score_last_100": [],
    }

    def __init__(self, file_path=default_score_file_path):

        self.file_path = file_path
        if self.file_path is None:
            self.file_path = File_util.default_score_file_path

        if not self.file_exists():
            self.create_file_with_content(File_util.default_data)

        self.data_raw = self.get_data_from_file()

    @staticmethod
    def _get_raw_data_from_file(file_path):
        """
        Load data from file, return None if file not found

        Args:
            file_path (str): Path to file

        Returns:
            json: raw data from file
        """

        if File_util._file_exists(file_path):
            try:
                with open(file_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logging.error("Error loading data from file: " + file_path)
                logging.error(str(e))

    @staticmethod
    def _file_exists(file_path):
        return os.path.exists(file_path)

    def get_data_from_file(self):
        logging.info("Getting data from file: " + self.file_path)
        if self.file_exists():
            return File_util._get_raw_data_from_file(self.file_path)
        else:
            logging.warning("Could not get data from file: " + self.file_path)
            return None

    def file_exists(self):
        if File_util._file_exists(self.file_path):
            return True
        else:
            logging.warning("File not found: " + self.file_path)
            return False

    def create_file_with_content(self, data):
        logging.info("Creating file: " + self.file_path)
        try:
            with open(self.file_path, "w") as f:
                json.dump(data, f, cls=Score_Position_Encoder, indent=4)
        except Exception as e:
            logging.error("Error creating file: " + self.file_path)
            logging.error(str(e))

    def clear_file(self):
        logging.info("Clearing file: " + self.file_path)
        try:
            with open(self.file_path, "w") as f:
                json.dump({}, f)
        except Exception as e:
            logging.error("Error clearing file: " + self.file_path)
            logging.error(str(e))
