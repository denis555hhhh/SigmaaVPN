#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import os

# Change to the project directory
os.chdir(r'c:\Users\Gnida222\Desktop\Сайт впн')

# Run the init_db.py script
result = subprocess.run([sys.executable, 'init_db.py'], capture_output=True, text=True)

# Print output
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# Check if database was created
if os.path.exists('sigmavpn.db'):
    print("\n✅ Database file created successfully!")
    print(f"Database size: {os.path.getsize('sigmavpn.db')} bytes")
else:
    print("\n❌ Database file was not created")

sys.exit(result.returncode)
