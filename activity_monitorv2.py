import time
import json
import cv2
import os
import psutil
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class FocusModeAlert:
    def __init__(self, non_productive_apps):
        self.non_productive_apps = non_productive_apps
        self.alert_sent = False

    def check_non_productive_apps(self):
        for process in psutil.process_iter(['name']):
            if process.info['name'] in self.non_productive_apps:
                if not self.alert_sent:
                    print(f"Alerta: Estás utilizando una aplicación no productiva: {process.info['name']}")
                    self.alert_sent = True
                return True
        self.alert_sent = False
        return False

class InactivityAlert:
    def __init__(self, alert_time):
        self.alert_time = alert_time
        self.last_activity_time = time.time()

    def reset_timer(self):
        self.last_activity_time = time.time()

    def check_inactivity(self):
        if time.time() - self.last_activity_time > self.alert_time:
            print("Alerta: Inactividad prolongada detectada.")
            self.reset_timer()

class ActivityMonitorv2:
    def __init__(self, alert_time=3600, movement_threshold=5000):
        self.alert_time = alert_time
        self.last_movement_time = time.time()
        self.movement_detected_flag = False
        self.movement_threshold = movement_threshold

    def detect_movement(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return

        ret, frame1 = cap.read()
        ret, frame2 = cap.read()

        while True:
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) < self.movement_threshold:
                    continue
                self.last_movement_time = time.time()
                self.movement_detected_flag = True

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Activity Monitor", frame1)
            frame1 = frame2
            ret, frame2 = cap.read()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if time.time() - self.last_movement_time > self.alert_time:
                self.movement_detected_flag = False

        cap.release()
        cv2.destroyAllWindows()

class ReportGenerator:
    def __init__(self):
        self.reports = []
        self.last_report_time = time.time()

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

    def should_generate_report(self, interval=300):
        return time.time() - self.last_report_time > interval

### Main ###
def main():
    config = {
        "alert_time": 3600,
        "apps_to_track": ["code", "chrome", "word", "excel"],
        "non_productive_apps": ["netflix", "youtube", "steam"],
        "track_time": 7200,
        "report_frequency": 86400  # Se ajusta a 5 minutos (300s)
    }

    activity_monitor = ActivityMonitorv2(alert_time=config['alert_time'])
    report_generator = ReportGenerator()
    focus_mode_alert = FocusModeAlert(non_productive_apps=config['non_productive_apps'])
    inactivity_alert = InactivityAlert(alert_time=config['alert_time'])

    productive_time = 0
    non_productive_time = 0
    start_time = time.time()

    while True:
        current_time = time.time()

        # Verificar si se detecta movimiento
        activity_monitor.detect_movement()
        if activity_monitor.movement_detected_flag:
            inactivity_alert.reset_timer()

        # Verificar si hay aplicaciones no productivas
        if focus_mode_alert.check_non_productive_apps():
            non_productive_time += time.time() - current_time
        else:
            productive_time += time.time() - current_time

        # Verificar inactividad prolongada
        inactivity_alert.check_inactivity()

        # Generar reportes cada 5 minutos
        if report_generator.should_generate_report(interval=300):
            report_generator.add_report(productive_time, non_productive_time, activity_monitor.movement_detected_flag)
            report_generator.save_report()
            productive_time = 0
            non_productive_time = 0
            report_generator.last_report_time = time.time()

        # Salir al presionar 'q'
        if current_time - start_time > config["track_time"]:
            break

if __name__ == "__main__":
    main()
