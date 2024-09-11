import unittest
import cv2
from activity_monitor import ActivityMonitor

class TestActivityMonitor(unittest.TestCase):

    def test_camera_open(self):
        """
        Verifica que la cámara se pueda abrir y capture al menos un fotograma.
        """
        camera = cv2.VideoCapture(0)  # Intenta abrir la cámara predeterminada
        self.assertTrue(camera.isOpened(), "La cámara no pudo ser abierta.")
        ret, frame = camera.read()  # Captura un fotograma
        self.assertTrue(ret, "No se pudo capturar ningún fotograma.")
        self.assertIsNotNone(frame, "El fotograma capturado está vacío o es None.")
        camera.release()

    def test_activity_monitor_movement_detection(self):
        """
        Verifica que el método detect_movement de ActivityMonitor funcione sin errores.
        """
        activity_monitor = ActivityMonitor(alert_time=3600)
        try:
            activity_monitor.detect_movement()  # Debe ejecutarse sin lanzar excepciones
            self.assertTrue(True)  # Si no falla, el test pasa
        except Exception as e:
            self.fail(f"detect_movement lanzó una excepción: {e}")

if __name__ == "__main__":
    unittest.main()
