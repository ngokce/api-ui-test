#!/usr/bin/env python3
"""
Basit Test Çalıştırıcı
Software Quality Assurance Dönem Projesi
"""

import subprocess
import sys
import os

def run_api_tests():
    """API testlerini çalıştır"""
    print("🔗 API Testleri Çalıştırılıyor...")
    
    # Python API testleri
    result1 = subprocess.run(['pytest', 'tests/api/', '-v'], capture_output=False)
    
    # Postman testleri
    if os.path.exists('JSONPlaceholder_API_Tests.postman_collection.json'):
        print("\n📊 Postman Testleri Çalıştırılıyor...")
        result2 = subprocess.run(['python3', 'run_postman_tests.py'], capture_output=False)
        return result1.returncode == 0 and result2.returncode == 0
    
    return result1.returncode == 0

def run_ui_tests():
    """UI testlerini çalıştır"""
    print("🖥️ UI Testleri Çalıştırılıyor...")
    result = subprocess.run(['pytest', 'tests/test_fullstack_ui.py', '-v'], capture_output=False)
    return result.returncode == 0

def run_all_tests():
    """Tüm testleri çalıştır"""
    print("🧪 Tüm Testler Çalıştırılıyor...")
    result = subprocess.run(['pytest', 'tests/', '-v'], capture_output=False)
    return result.returncode == 0

def generate_report():
    """HTML raporu oluştur"""
    print("📄 HTML Raporu Oluşturuluyor...")
    result = subprocess.run([
        'pytest', 'tests/', 
        '--html=test_report.html', 
        '--self-contained-html', 
        '-v'
    ], capture_output=False)
    
    if result.returncode == 0:
        print("✅ Rapor oluşturuldu: test_report.html")
    return result.returncode == 0

def main():
    """Ana menü"""
    print("=" * 50)
    print("🧪 Software Quality Assurance Test Runner")
    print("=" * 50)
    
    while True:
        print("\nSeçenekler:")
        print("1. API Testleri")
        print("2. UI Testleri") 
        print("3. Tüm Testler")
        print("4. HTML Raporu Oluştur")
        print("5. Çıkış")
        
        choice = input("\nSeçiminiz (1-5): ").strip()
        
        if choice == '1':
            run_api_tests()
        elif choice == '2':
            run_ui_tests()
        elif choice == '3':
            run_all_tests()
        elif choice == '4':
            generate_report()
        elif choice == '5':
            print("👋 Çıkılıyor...")
            break
        else:
            print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    main() 