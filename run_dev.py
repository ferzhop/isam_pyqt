import subprocess
import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_DIR = os.path.join(os.path.dirname(__file__), 'src')
MAIN_PATH = os.path.join(os.path.dirname(__file__), 'src', 'main.py')

class RestartHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        super().__init__()
        self.restart_callback = restart_callback

    def on_any_event(self, event):
        if event.is_directory:
            return
        # Ignorar archivos temporales y pyc
        if event.src_path.endswith(('.py', '.json')) and not event.src_path.endswith('.pyc'):
            print(f"Archivo cambiado: {event.src_path}. Reiniciando app...")
            self.restart_callback()

def run_app():
    try:
        return subprocess.Popen([sys.executable, MAIN_PATH])
    except Exception as e:
        print(f"Error al iniciar la app: {e}")
        return None

def main():
    process = run_app()
    def restart():
        nonlocal process
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
        time.sleep(0.5)
        process = run_app()

    event_handler = RestartHandler(restart)
    observer = Observer()
    observer.schedule(event_handler, WATCHED_DIR, recursive=True)
    observer.start()
    print("Modo desarrollo: la app se reiniciará al guardar cambios en src/ ...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if process and process.poll() is None:
            process.terminate()
    observer.join()

if __name__ == "__main__":
    main()
