import pandas as pd
from pandas import DataFrame


class LogReader:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def read_logs(self) -> DataFrame:
        return pd.read_json(self.filepath, lines=True)
