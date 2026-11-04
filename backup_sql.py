# import os
# import datetime
# import subprocess

# # ✅ Step 1: Database Settings
# db_name = "school_imentor"
# db_user = "root"
# db_password = ""  # 👉 Add your DB password if any
# db_host = "localhost"

# # ✅ Step 2: Create backup folder and file name
# today = datetime.datetime.now().strftime("%Y-%m-%d")
# backup_dir = os.path.join(os.getcwd(), "backup")
# os.makedirs(backup_dir, exist_ok=True)

# backup_file = os.path.join(backup_dir, f"db_backup_{today}.sql")

# # ✅ Step 3: mysqldump command
# if db_password:
#     command = f'mysqldump -h {db_host} -u {db_user} -p{db_password} {db_name} > "{backup_file}"'
# else:
#     command = f'mysqldump -h {db_host} -u {db_user} {db_name} > "{backup_file}"'

# # ✅ Step 4: Run command
# try:
#     subprocess.run(command, shell=True, check=True)
#     print(f"[OK] Backup created: {backup_file}")
# except subprocess.CalledProcessError as e:
#     print(f"[ERROR] Backup failed: {e}")


import subprocess
import datetime
import os

# Backup folder
backup_dir = r"C:\iMentor_Github\imentor\backup"
os.makedirs(backup_dir, exist_ok=True)

# Date format
today = datetime.datetime.now().strftime('%Y-%m-%d')
backup_file = os.path.join(backup_dir, f"db_backup_{today}.sql")

# MySQL config
mysqldump_path = r"C:\xampp\mysql\bin\mysqldump.exe"
mysql_user = "root"
mysql_password = ""
mysql_db = "school_imentor"

# Construct command
command = [
    mysqldump_path,
    "-u", mysql_user,
    "-h", "localhost",
    mysql_db
]

if mysql_password:
    command.insert(3, f"-p{mysql_password}")

try:
    with open(backup_file, 'w', encoding='utf-8') as f:
        subprocess.run(command, stdout=f, stderr=subprocess.PIPE, shell=False, check=True)
    print(f"[✅] Backup Success: {backup_file}")
except subprocess.CalledProcessError as e:
    print("[❌] Backup failed")
    print(e.stderr.decode())