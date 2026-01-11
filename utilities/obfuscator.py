import base64
import zlib
import random
import string
from cryptography.fernet import Fernet

class AdvancedObfuscator:
    def __init__(self, encryption_key=None):
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
    
    def obfuscate_payload(self, payload, method='advanced'):
        """تشويش الحمولة بعدة طرق"""
        if method == 'simple':
            return self._simple_obfuscation(payload)
        elif method == 'advanced':
            return self._advanced_obfuscation(payload)
        elif method == 'military':
            return self._military_grade_obfuscation(payload)
        else:
            return payload
    
    def _simple_obfuscation(self, payload):
        """تشويش بسيط"""
        # Base64 encoding
        encoded = base64.b64encode(payload.encode()).decode()
        
        # Reverse string
        reversed_str = encoded[::-1]
        
        # Add random padding
        padding = ''.join(random.choices(string.ascii_letters, k=10))
        return f"{padding}{reversed_str}{padding}"
    
    def _advanced_obfuscation(self, payload):
        """تشويش متقدم"""
        # Compression
        compressed = zlib.compress(payload.encode())
        
        # Base85 encoding
        encoded = base64.b85encode(compressed).decode()
        
        # Split and rearrange
        parts = [encoded[i:i+10] for i in range(0, len(encoded), 10)]
        random.shuffle(parts)
        
        # Join with separators
        separator = random.choice(['|', ':', ';', '#'])
        return separator.join(parts)
    
    def _military_grade_obfuscation(self, payload):
        """تشويش عسكري المستوى"""
        # AES Encryption
        encrypted = self.cipher.encrypt(payload.encode())
        
        # Multiple encoding layers
        layers = [
            lambda x: base64.b64encode(x).decode(),
            lambda x: base64.b32encode(x.encode()).decode(),
            lambda x: base64.b16encode(x.encode()).decode(),
        ]
        
        result = encrypted
        for layer in layers:
            try:
                result = layer(result)
            except:
                result = result
        
        # Add fake headers
        headers = [
            "HTTP/1.1 200 OK",
            "Content-Type: text/html",
            "Cache-Control: no-cache",
            f"X-Encoded: {random.randint(1000, 9999)}"
        ]
        
        return '\n'.join(headers) + '\n\n' + result
    
    def deobfuscate(self, obfuscated_payload, method='advanced'):
        """فك التشويش"""
        if method == 'simple':
            # Remove padding
            cleaned = obfuscated_payload[10:-10]
            reversed_back = cleaned[::-1]
            return base64.b64decode(reversed_back).decode()
        
        elif method == 'advanced':
            # Reassemble and decode
            separator = obfuscated_payload[0] if obfuscated_payload[0] in '|:;#' else '|'
            parts = obfuscated_payload.split(separator)
            
            # Reorder (need to know original order, in real implementation would need mapping)
            # For simplicity, assuming order is preserved
            encoded = ''.join(parts)
            compressed = base64.b85decode(encoded)
            return zlib.decompress(compressed).decode()
        
        elif method == 'military':
            # Remove headers
            lines = obfuscated_payload.split('\n')
            payload = '\n'.join(lines[5:])  # Skip headers
            
            # Reverse the encoding layers (simplified)
            try:
                decoded = base64.b16decode(payload)
                decoded = base64.b32decode(decoded)
                decoded = base64.b64decode(decoded)
                return self.cipher.decrypt(decoded).decode()
            except:
                return "Decryption failed"
        
        return obfuscated_payload
