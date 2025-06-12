#!/usr/bin/env python3
"""
Postman API Testlerini Çalıştırma Script'i
Newman kullanarak Postman koleksiyonunu çalıştırır
"""

import subprocess
import sys
import os
import json
from datetime import datetime


def check_newman_installed():
    """Newman'ın yüklü olup olmadığını kontrol et"""
    try:
        result = subprocess.run(['newman', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Newman kurulu: {result.stdout.strip()}")
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def install_newman():
    """Newman'ı yükle"""
    print("📦 Newman yükleniyor...")
    try:
        # npm ile newman yükle
        result = subprocess.run(['npm', 'install', '-g', 'newman'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Newman başarıyla yüklendi!")
            return True
        else:
            print(f"❌ Newman yüklenemedi: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ npm bulunamadı. Node.js yüklü olduğundan emin olun.")
        return False


def run_postman_collection():
    """Postman koleksiyonunu çalıştır"""
    collection_file = "JSONPlaceholder_API_Tests.postman_collection.json"
    
    if not os.path.exists(collection_file):
        print(f"❌ Koleksiyon dosyası bulunamadı: {collection_file}")
        return False
    
    print(f"🚀 Postman testleri çalıştırılıyor: {collection_file}")
    
    # Rapor dosyaları için timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = f"postman_report_{timestamp}.html"
    json_report = f"postman_report_{timestamp}.json"
    
    # Newman komutunu çalıştır
    newman_cmd = [
        'newman', 'run', collection_file,
        '--reporters', 'html,json,cli',
        '--reporter-html-export', html_report,
        '--reporter-json-export', json_report,
        '--timeout', '10000',  # 10 saniye timeout
        '--delay-request', '100'  # İstekler arası 100ms bekleme
    ]
    
    try:
        print("⏳ Testler çalışıyor...")
        result = subprocess.run(newman_cmd, capture_output=True, text=True)
        
        print("\n" + "="*60)
        print("📋 POSTMAN TEST SONUÇLARI")
        print("="*60)
        print(result.stdout)
        
        if result.stderr:
            print("\n⚠️  Uyarılar/Hatalar:")
            print(result.stderr)
        
        # Sonuç dosyalarının varlığını kontrol et
        if os.path.exists(html_report):
            print(f"📄 HTML Rapor: {html_report}")
        if os.path.exists(json_report):
            print(f"📊 JSON Rapor: {json_report}")
            analyze_json_report(json_report)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test çalıştırma hatası: {e}")
        return False


def analyze_json_report(json_file):
    """JSON raporunu analiz et ve özet bilgi ver"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Test istatistikleri
        run_stats = data.get('run', {}).get('stats', {})
        tests = run_stats.get('tests', {})
        assertions = run_stats.get('assertions', {})
        requests = run_stats.get('requests', {})
        
        print("\n📊 TEST İSTATİSTİKLERİ:")
        print(f"   Toplam İstek: {requests.get('total', 0)}")
        print(f"   Başarılı İstek: {requests.get('total', 0) - requests.get('failed', 0)}")
        print(f"   Başarısız İstek: {requests.get('failed', 0)}")
        print(f"   Toplam Test: {tests.get('total', 0)}")
        print(f"   Başarılı Test: {tests.get('total', 0) - tests.get('failed', 0)}")
        print(f"   Başarısız Test: {tests.get('failed', 0)}")
        print(f"   Toplam Assertion: {assertions.get('total', 0)}")
        print(f"   Başarılı Assertion: {assertions.get('total', 0) - assertions.get('failed', 0)}")
        print(f"   Başarısız Assertion: {assertions.get('failed', 0)}")
        
        # Başarısız testleri listele
        if tests.get('failed', 0) > 0:
            print("\n❌ BAŞARISIZ TESTLER:")
            executions = data.get('run', {}).get('executions', [])
            for execution in executions:
                if 'assertions' in execution:
                    for assertion in execution['assertions']:
                        if assertion.get('error'):
                            test_name = assertion.get('assertion', 'Bilinmeyen Test')
                            error_msg = assertion.get('error', {}).get('message', 'Bilinmeyen Hata')
                            print(f"   • {test_name}: {error_msg}")
        
        # Performans bilgileri
        timings = data.get('run', {}).get('timings', {})
        if timings:
            print(f"\n⏱️  PERFORMANS:")
            print(f"   Toplam Süre: {timings.get('completed', 0)}ms")
            print(f"   Ortalama Yanıt Süresi: {timings.get('responseAverage', 0)}ms")
            
    except Exception as e:
        print(f"⚠️  JSON rapor analizi hatası: {e}")


def main():
    """Ana fonksiyon"""
    print("🧪 JSONPlaceholder API Test Çalıştırıcısı")
    print("="*50)
    
    # Newman kontrolü
    if not check_newman_installed():
        print("❌ Newman yüklü değil.")
        choice = input("Newman'ı yüklemek ister misiniz? (y/N): ").lower()
        
        if choice in ['y', 'yes', 'evet']:
            if not install_newman():
                print("❌ Newman yüklenemedi. Manuel olarak yüklemeyi deneyin:")
                print("   npm install -g newman")
                sys.exit(1)
        else:
            print("❌ Newman gerekli. Çıkılıyor...")
            sys.exit(1)
    
    # Testleri çalıştır
    success = run_postman_collection()
    
    if success:
        print("\n✅ Tüm testler tamamlandı!")
        print("\n💡 Postman GUI'de daha detaylı testler için:")
        print("   1. Postman'ı açın")
        print("   2. Import butonuna tıklayın")
        print("   3. JSONPlaceholder_API_Tests.postman_collection.json dosyasını seçin")
        print("   4. Collection'ı çalıştırın")
    else:
        print("\n❌ Testlerde hatalar var. Raporları kontrol edin.")
        sys.exit(1)


if __name__ == "__main__":
    main() 