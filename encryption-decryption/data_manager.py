import json
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import hashlib

class DataManager:
    def __init__(self):
        self.data_file = "encrypted_data.json"
        self.users_file = "users.json"
        self.lockout_file = "lockout_data.json"
        self.load_data()
        self.load_users()
        self.load_lockout_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.stored_data = json.load(f)
        else:
            self.stored_data = {}

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def load_lockout_data(self):
        if os.path.exists(self.lockout_file):
            with open(self.lockout_file, 'r') as f:
                self.lockout_data = json.load(f)
        else:
            self.lockout_data = {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.stored_data, f, indent=4)

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def save_lockout_data(self):
        with open(self.lockout_file, 'w') as f:
            json.dump(self.lockout_data, f, indent=4)

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = os.urandom(16)
        else:
            salt = base64.b64decode(salt)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.b64encode(kdf.derive(password.encode()))
        return key, base64.b64encode(salt).decode()

    def verify_password(self, password, stored_hash, salt):
        key, _ = self.hash_password(password, salt)
        return key.decode() == stored_hash

    def is_locked_out(self, username):
        if username in self.lockout_data:
            lockout_time = datetime.fromisoformat(self.lockout_data[username]['time'])
            if datetime.now() - lockout_time < timedelta(minutes=15):
                return True
            else:
                del self.lockout_data[username]
                self.save_lockout_data()
        return False

    def record_failed_attempt(self, username):
        if username not in self.lockout_data:
            self.lockout_data[username] = {'attempts': 0, 'time': datetime.now().isoformat()}
        
        self.lockout_data[username]['attempts'] += 1
        
        if self.lockout_data[username]['attempts'] >= 3:
            self.lockout_data[username]['time'] = datetime.now().isoformat()
        
        self.save_lockout_data()

    def reset_failed_attempts(self, username):
        if username in self.lockout_data:
            del self.lockout_data[username]
            self.save_lockout_data()

    def register_user(self, username, password):
        if username in self.users:
            return False
        
        key, salt = self.hash_password(password)
        self.users[username] = {
            'password_hash': key.decode(),
            'salt': salt
        }
        self.save_users()
        return True

    def authenticate_user(self, username, password):
        if username not in self.users:
            return False
        
        user_data = self.users[username]
        return self.verify_password(password, user_data['password_hash'], user_data['salt']) 