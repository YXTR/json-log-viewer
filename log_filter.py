from pandas import DataFrame


class LogFilter:
    @staticmethod
    def filter_logs(df: DataFrame, level: str = '', name: str = '') -> DataFrame:
        if level:
            df = df[df['levelname'].str.contains(level, case=False)]
        if name:
            df = df[df['name'].str.contains(name, case=False)]
        return df
