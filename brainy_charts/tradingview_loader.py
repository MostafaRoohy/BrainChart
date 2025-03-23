import pandas as pd

class TradingViewLoader:
    def __init__(self, filepath):
        """
        Initialize the TradingViewLoader with the path to the CSV file.
        """
        self.filepath = filepath

    def load_data(self):
        """
        Load the TradingView chart data from the CSV file into a Pandas DataFrame.
        """
        try:
            data = pd.read_csv(self.filepath)
            data['time'] = pd.to_datetime(data['time'], unit='ms')  # Convert timestamp to datetime
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
