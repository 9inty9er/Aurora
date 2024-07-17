import subprocess
import time
import threading

def start_backup_process():
    try:
        subprocess.Popen(["python", "E:/Aurora/capabilities/aurora_backup.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Backup process started successfully.")
    except Exception as e:
        print(f"Error starting backup process: {e}")

def schedule_periodic_backup():
    while True:
        time.sleep(300)  # Wait for 5 minutes
        start_backup_process()

def start_periodic_backup_thread():
    backup_thread = threading.Thread(target=schedule_periodic_backup)
    backup_thread.daemon = True
    backup_thread.start()
