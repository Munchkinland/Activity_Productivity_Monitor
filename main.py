from activity_monitor import ActivityMonitor
from productivity_tracker import ProductivityTracker
from notification_manager import NotificationManager
from reports import ReportGenerator
from utils import load_config, format_time, timer
import time

def main():
    # Cargar configuración desde config.json
    config = load_config('config.json')

    # Inicializar los módulos
    activity_monitor = ActivityMonitor(alert_time=config["alert_time"])
    productivity_tracker = ProductivityTracker(
        apps_to_track=config["apps_to_track"],
        non_productive_apps=config["non_productive_apps"]
    )
    notification_manager = NotificationManager( #modificar según SO
        title="¡Es hora de moverte!", 
        message="No se ha detectado movimiento en una hora. ¡Toma un descanso!"
    )
    report_generator = ReportGenerator()

    # Ciclo de monitoreo y generación de reportes
    try:
        start_time = time.time()
        report_time = time.time()  # Tiempo para el próximo reporte
        track_time = config["track_time"]  # Tiempo de monitoreo de productividad (e.g. 2 horas)

        while True:
            # Monitoreo de actividad física (detectar movimiento)
            activity_monitor.detect_movement()

            # Verificar si ha pasado mucho tiempo sin movimiento
            if not activity_monitor.movement_detected():
                notification_manager.send_notification()

            # Monitorear productividad por un período definido
            usage_stats = productivity_tracker.track_usage(track_time)
            print(f"Tiempo productivo: {format_time(usage_stats['productive'])}")
            print(f"Tiempo no productivo: {format_time(usage_stats['non_productive'])}")

            # Añadir los datos al informe
            report_generator.add_report(
                productive_time=usage_stats['productive'],
                non_productive_time=usage_stats['non_productive'],
                movement_detected=activity_monitor.movement_detected()
            )

            # Guardar el reporte a un archivo cada cierto tiempo (configurado en segundos)
            if time.time() - report_time > config["report_frequency"]:
                report_generator.save_report('daily_report.json')
                report_generator.generate_plot()
                report_time = time.time()

            # Pausar hasta la próxima iteración
            timer(10)  # Descanso de 10 segundos entre ciclos

    except KeyboardInterrupt:
        print("Aplicación terminada. Guardando reportes.")
        report_generator.save_report('final_report.json')

if __name__ == "__main__":
    main()
