import psutil
import time

class ProductivityTracker:
    def __init__(self, apps_to_track=None, non_productive_apps=None):
        if apps_to_track is None:
            self.apps_to_track = ["code", "chrome", "word", "excel"]
        else:
            self.apps_to_track = apps_to_track

        if non_productive_apps is None:
            self.non_productive_apps = ["netflix", "youtube", "steam"]
        else:
            self.non_productive_apps = non_productive_apps

        self.usage_stats = {"productive": 0, "non_productive": 0}

    def track_usage(self, track_time=3600):
        start_time = time.time()

        while time.time() - start_time < track_time:
            active_apps = [p.info["name"].lower() for p in psutil.process_iter(['name'])]
            productive = False
            non_productive = False

            for app in self.apps_to_track:
                if app in active_apps:
                    productive = True

            for app in self.non_productive_apps:
                if app in active_apps:
                    non_productive = True

            if productive:
                self.usage_stats["productive"] += 1  # Sumar tiempo productivo
            elif non_productive:
                self.usage_stats["non_productive"] += 1  # Sumar tiempo no productivo

            time.sleep(1)

        return self.usage_stats
