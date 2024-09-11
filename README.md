# Activity_Productivity_Monitor

Flujo de trabajo del proyecto:

    main.py:
        El archivo principal ejecuta las clases de monitoreo y productividad, además de generar notificaciones y generar informes usando el módulo reports.py.

    activity_monitor.py:
        Maneja la detección de movimiento usando la cámara y establece alertas si no se detecta movimiento en un período de tiempo.

    productivity_tracker.py:
        Rastrea las aplicaciones productivas y no productivas utilizadas por el usuario, basado en la lista en config.json.

    notification_manager.py:
        Envío de notificaciones al sistema, indicando cuándo debe moverse o cuándo ha pasado demasiado tiempo en aplicaciones no productivas.

    reports.py:
        Genera informes diarios del tiempo productivo, no productivo, y la actividad física detectada, además de generar gráficos con matplotlib.

    utils.py:
        Contiene funciones para cargar configuraciones, manejar temporizadores y dar formato al tiempo, simplificando el código en otros archivos.

Descripción del código:

    Carga de configuración (config.json):
        La configuración (como el tiempo de alerta y la lista de aplicaciones productivas/no productivas) se carga al inicio usando load_config() desde utils.py.

    Inicialización de módulos:
        ActivityMonitor: Monitorea la actividad física del usuario usando la cámara.
        ProductivityTracker: Rastrea el uso de aplicaciones productivas y no productivas durante el tiempo configurado (track_time).
        NotificationManager: Envía notificaciones si el usuario no ha estado activo físicamente.
        ReportGenerator: Genera y guarda informes periódicos del uso del tiempo, además de generar gráficos con matplotlib.

    Monitoreo del movimiento y productividad:
        Se monitorea el movimiento del usuario y el uso de aplicaciones productivas en paralelo. Si no se detecta movimiento por un tiempo (alert_time), se envía una notificación.
        El tiempo productivo y no productivo se registra y se muestra en consola.

    Generación de informes y gráficos:
        Cada cierto tiempo (definido en config.json con report_frequency), el sistema guarda un reporte en un archivo JSON y genera un gráfico con la evolución del tiempo productivo vs no productivo.
        Los informes también se pueden guardar cuando se interrumpe la ejecución del programa con Ctrl + C.

    Función timer():
        Usa un temporizador entre ciclos para pausar el monitoreo por un intervalo de tiempo (10 segundos en este caso).

    ## activity_monitor.py 

    Paso a producción 

    ara producción (sin mostrar ventanas):

Si deseas eliminar la visualización en producción, simplemente comenta o elimina las siguientes líneas relacionadas con la visualización en la función detect_movement():

python

# Mostrar el video con el rectángulo alrededor del movimiento detectado
cv2.imshow("Activity Monitor", frame1)

# Presionar 'q' para cerrar la ventana
if cv2.waitKey(1) & 0xFF == ord('q'):
    break

Con esto, el código seguirá ejecutándose en segundo plano y detectando movimiento, pero sin mostrar la ventana de video.

{
    "alert_time": 300,  # Tiempo en segundos antes de enviar una alerta por inactividad (5 minutos)
    "apps_to_track": ["code", "chrome", "word", "excel"],
    "non_productive_apps": ["netflix", "youtube", "steam"],
    "track_time": 7200,  # Tiempo durante el cual se realiza el seguimiento de la actividad
    "report_frequency": 300  # Intervalo para generar un reporte (5 minutos)
}
