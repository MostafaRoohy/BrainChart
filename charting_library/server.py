# server.py
from flask import Flask, jsonify
import csv

app = Flask(__name__)

class CSVLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        data = []
        with open(self.file_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    "time": int(row["time"]),        # time in milliseconds
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row["volume"])
                })
        return data

csv_loader = CSVLoader("salam.csv")

@app.route('/api/localdata', methods=['GET'])
def localdata():
    data = csv_loader.load_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000)
