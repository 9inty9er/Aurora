import subprocess
import time

def start_backup_process():
    try:
        subprocess.Popen(["python", "E:/Aurora/capabilities/aurora_backup.py"])
        print("Backup process started successfully.")
    except Exception as e:
        print(f"Error starting backup process: {e}")

def schedule_periodic_backup():
    while True:
        time.sleep(300)  # Wait for 5 minutes
        start_backup_process()
