import json
import os
import hashlib
from datetime import datetime

class AdvancedConfig:
    def __init__(self):
        self.config = self._load_or_create()
        self.encryption_key = self._generate_key()
        
    def _generate_key(self):
        """إنشاء مفتاح تشفير فريد"""
        system_id = os.urandom(16).hex()
        timestamp = str(datetime.now().timestamp())
        return hashlib.sha256((system_id + timestamp).encode()).hexdigest()[:32]
    
    def _load_or_create(self):
        """تحميل أو إنشاء إعدادات متقدمة"""
        config_file = "data/advanced_config.json"
        default_config = {
            "system": {
                "name": "SPECTER_VANGUARD_PRO",
                "version": "3.0.1",
                "mode": "AGGRESSIVE",
                "max_threads": 100,
                "request_timeout": 5
            },
            "targets": {
                "platforms": ["facebook", "instagram", "twitter"],
                "auto_expand": True,
                "deep_scan": True
            },
            "attack": {
                "vectors": ["phishing", "reporting", "automation"],
                "concurrent_attacks": 10,
                "delay_between": 0.5,
                "retry_failed": 3
            },
            "stealth": {
                "user_agents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                ],
                "proxy_rotation": True,
                "ip_spoofing": True,
                "cookie_randomization": True
            },
            "performance": {
                "max_memory_mb": 512,
                "cpu_usage_limit": 80,
                "log_level": "DEBUG",
                "auto_cleanup": True
            }
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    
    def get(self, section, key=None):
        """الحصول على قيمة من الإعدادات"""
        if key:
            return self.config.get(section, {}).get(key)
        return self.config.get(section)
    
    def update(self, section, key, value):
        """تحديث الإعدادات ديناميكيًا"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self._save()
    
    def _save(self):
        """حفظ الإعدادات"""
        with open("data/advanced_config.json", 'w') as f:
            json.dump(self.config, f, indent=4)
