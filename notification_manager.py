from plyer import notification

class NotificationManager:
    def __init__(self, title="Recordatorio", message="Es hora de moverte"):
        self.title = title
        self.message = message

    def send_notification(self):
        notification.notify(
            title=self.title,
            message=self.message,
            timeout=5  # La notificación dura 5 segundos
        )
