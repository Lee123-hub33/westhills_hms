import os
import datetime

def run_backup():
    # Set the name of the backup file with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.sql"
    
    # The command to run (using pg_dump)
    # We use 'set PGPASSWORD' so it doesn't stop to ask for it
    os.environ['PGPASSWORD'] = 'Lee@2026'
    
    command = f"pg_dump -U postgres -h localhost westhills_hms > {backup_file}"
    
    print(f"Starting backup for westhills_hms...")
    os.system(command)
    print(f"Backup complete! Saved as: {backup_file}")

if __name__ == "__main__":
    run_backup()