import os
import shutil
import datetime
import subprocess

def create_backup():
    # Define source and backup directories
    source_dir = 'E:/Aurora'
    backup_dir = 'E:/AuroraBackup'

    # Create a timestamp for the backup folder
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_folder = os.path.join(backup_dir, f'backup_{timestamp}')

    # Copy the source directory to the backup directory
    shutil.copytree(source_dir, backup_folder)
    print(f"Backup created successfully at {backup_folder}")

def git_backup():
    try:
        # Change directory to the Git repository
        os.chdir('E:/Aurora')

        # Add all changes to the staging area
        subprocess.run(['git', 'add', '.'], check=True)

        # Check for changes
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout.strip():
            # Commit the changes
            subprocess.run(['git', 'commit', '-m', 'Automated backup'], check=True)

            # Push the changes to the remote repository
            subprocess.run(['git', 'push', '-u', 'origin', 'master'], check=True)
            print("Git backup completed successfully.")
        else:
            print("No changes to commit.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git backup: {e}")

if __name__ == "__main__":
    create_backup()
    git_backup()
