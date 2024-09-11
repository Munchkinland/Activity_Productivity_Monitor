import json
import matplotlib.pyplot as plt
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.reports = []

    def add_report(self, productive_time, non_productive_time, movement_detected):
        report = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "productive_time": productive_time,
            "non_productive_time": non_productive_time,
            "movement_detected": movement_detected
        }
        self.reports.append(report)

    def save_report(self, filename='report.json'):
        with open(filename, 'w') as f:
            json.dump(self.reports, f, indent=4)

    def generate_plot(self):
        dates = [r['date'] for r in self.reports]
        productive_time = [r['productive_time'] for r in self.reports]
        non_productive_time = [r['non_productive_time'] for r in self.reports]

        plt.plot(dates, productive_time, label="Productive Time")
        plt.plot(dates, non_productive_time, label="Non-Productive Time")
        plt.xlabel('Date')
        plt.ylabel('Time (seconds)')
        plt.title('Productivity Over Time')
        plt.legend()
        plt.show()
