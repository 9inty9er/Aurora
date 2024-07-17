import subprocess
import time
import threading
import sys

LOG_FILE = 'E:/AuroraBackup/backup_log.txt'

def start_backup_process():
    def loading_indicator():
        chars = "/—\\|"
        for char in chars:
            sys.stdout.write(f'\rBackup in progress... {char}')
            time.sleep(0.1)
            sys.stdout.flush()

    loading_thread = threading.Thread(target=loading_indicator)
    loading_thread.start()

    try:
        process = subprocess.Popen(
            ["python", "E:/Aurora/capabilities/aurora_backup.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        with open(LOG_FILE, 'r') as log_file:
            backup_status = log_file.readlines()[-1].strip()

        print(f"\rBackup process status: {backup_status}")
    except Exception as e:
        print(f"Error starting backup process: {e}")
    finally:
        loading_thread.join()

def schedule_periodic_backup():
    while True:
        time.sleep(300)  # Wait for 5 minutes
        start_backup_process()

def start_periodic_backup_thread():
    backup_thread = threading.Thread(target=schedule_periodic_backup)
    backup_thread.daemon = True
    backup_thread.start()
