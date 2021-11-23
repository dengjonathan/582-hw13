import random
import requests
import json
import datetime

import pygit2
import shutil
from pathlib import Path
import sys

# Get the students' github username and name of repository
with open("/home/codio/workspace/student_credentials", "r") as f:
    github_username, DIR = f.readlines()
    github_username, DIR = github_username.strip(), DIR.strip()

# Clear any existing directory (clone_repository will fail otherwise)
dir_path = Path(f'/home/codio/workspace/.guides/{DIR}')
try:
    if dir_path.exists():
        shutil.rmtree(dir_path)
except OSError as e:
    print("Error when removing directory: %s : %s" % (dir_path, e.strerror))
    
try:
    # import student code using pygit2
    keypair = pygit2.Keypair("git", "/home/codio/workspace/ssh_keys/id_rsa.pub", "/home/codio/workspace/ssh_keys/id_rsa", "")
    callbacks = pygit2.RemoteCallbacks(credentials=keypair)
    print(f'Cloning from: git@github.com:{github_username}/{DIR}.git')
    pygit2.clone_repository(f"git@github.com:{github_username}/{DIR}.git", f"/home/codio/workspace/.guides/{DIR}",
                            callbacks=callbacks)
except:
    print("Failed to clone the repository.")
    exit()

sys.path.append(f'/home/codio/workspace/.guides/{DIR}')
    
try:
    from validate import validate
except ImportError:
    raise ImportError('Unable to import validation script')

score = validate(f'/home/codio/workspace/.guides/{DIR}')