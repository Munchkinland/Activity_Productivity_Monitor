#Camera
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
        self.alert_time = alert_time  # Tiempo antes de enviar una alerta
        self.last_movement_time = time.time()  # Última vez que se detectó movimiento
        self.movement_detected_flag = False  # Bandera para saber si hay movimiento reciente
        self.movement_threshold = movement_threshold  # Umbral para considerar que hay movimiento

    def detect_movement(self):
        """
        Detecta movimiento comparando fotogramas consecutivos de la cámara.
        Muestra el video en tiempo real con un rectángulo alrededor del área con movimiento detectado.
        """
        cap = cv2.VideoCapture(0)  # Iniciar la cámara

        # Verificar si la cámara se abrió correctamente
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return

        ret, frame1 = cap.read()  # Primer fotograma de referencia
        ret, frame2 = cap.read()  # Segundo fotograma para comparar

        while True:
            # Diferencia entre los dos fotogramas consecutivos
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
            blur = cv2.GaussianBlur(gray, (5, 5), 0)  # Aplicar desenfoque
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # Umbral para identificar áreas en movimiento
            dilated = cv2.dilate(thresh, None, iterations=3)  # Dilatación para cerrar huecos en los contornos
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            movement_detected = False

            # Recorrer todos los contornos detectados
            for contour in contours:
                if cv2.contourArea(contour) < self.movement_threshold:
                    continue  # Ignorar pequeños movimientos (ruido)
                movement_detected = True
                self.last_movement_time = time.time()  # Actualizar el tiempo de movimiento detectado
                self.movement_detected_flag = True  # Indicar que se detectó movimiento
                
                # Dibujar un rectángulo alrededor del área con movimiento
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Mostrar el video con el rectángulo alrededor del movimiento detectado
            cv2.imshow("Activity Monitor", frame1)

            # Actualizar los fotogramas para continuar con la comparación
            frame1 = frame2
            ret, frame2 = cap.read()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Si ha pasado demasiado tiempo sin detectar movimiento, reiniciar la bandera de detección
            if time.time() - self.last_movement_time > self.alert_time:
                self.movement_detected_flag = False  # Indicar que no hay movimiento reciente

        cap.release()  # Liberar la cámara al finalizar
        cv2.destroyAllWindows()  # Cerrar todas las ventanas abiertas por OpenCV

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
        self.cap.release()
        cv2.destroyAllWindows()
