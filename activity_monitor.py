import cv2
import time
import numpy as np

class ActivityMonitor:
    def __init__(self, alert_time=3600, movement_threshold=5000):
        """
        Inicializa el monitor de actividad.
        
        :param alert_time: Tiempo en segundos antes de enviar una alerta por inactividad
        :param movement_threshold: Umbral mínimo de área para considerar que hay movimiento
        """
        self.alert_time = alert_time
        self.last_movement_time = time.time()
        self.movement_detected_flag = False
        self.movement_threshold = movement_threshold
        self.cap = None

    def detect_movement(self):
        """
        Detecta movimiento comparando fotogramas consecutivos de la cámara.
        Muestra el video en tiempo real con un rectángulo alrededor del área con movimiento detectado.
        """
        print("Iniciando la cámara...")
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return

        print("Cámara abierta. Capturando primer fotograma...")
        ret, frame1 = self.cap.read()
        if not ret:
            print("Error: No se pudo capturar el primer fotograma.")
            self.cap.release()
            return

        print("Capturando segundo fotograma...")
        ret, frame2 = self.cap.read()
        if not ret:
            print("Error: No se pudo capturar el segundo fotograma.")
            self.cap.release()
            return

        while True:
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            movement_detected = False
            for contour in contours:
                if cv2.contourArea(contour) < self.movement_threshold:
                    continue
                movement_detected = True
                self.last_movement_time = time.time()
                self.movement_detected_flag = True

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Activity Monitor", frame1)

            frame1 = frame2
            ret, frame2 = self.cap.read()
            if not ret:
                print("Error: No se pudo capturar un fotograma durante la detección.")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Se presionó 'q'. Cerrando...")
                break

            if time.time() - self.last_movement_time > self.alert_time:
                print("No se ha detectado movimiento durante el tiempo de alerta. Reiniciando bandera de detección.")
                self.movement_detected_flag = False

        self.stop_camera()

    def movement_detected(self):
        """
        Retorna el estado de la bandera que indica si se ha detectado movimiento reciente.
        
        :return: True si se ha detectado movimiento recientemente, False en caso contrario.
        """
        return self.movement_detected_flag

    def stop_camera(self):
        """
        Libera la cámara y cierra las ventanas de OpenCV si fuera necesario.
        """
        if self.cap is not None:
            print("Liberando la cámara...")
            self.cap.release()
        cv2.destroyAllWindows()
        print("Todas las ventanas han sido cerradas.")
