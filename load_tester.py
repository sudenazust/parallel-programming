import asyncio
import aiohttp
import time
import pandas as pd
import os

# Sunucuya tek bir asenkron HTTP isteği gönderen fonksiyon
async def fetch_response(session, url, results):
    request_start = time.perf_counter()
    try:
        async with session.get(url) as response:
            await response.text() 
            request_end = time.perf_counter()
            
            results.append({
                'latency': request_end - request_start,
                'status_code': response.status,
                'is_success': response.status == 200
            })
    except Exception as e:
        results.append({'latency': 0, 'status_code': 500, 'is_success': False})

# Belirlenen sanal kullanıcı sayısı kadar eşzamanlı yük oluşturan ana simülasyon
async def run_load_simulation(target_url, concurrent_users):
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_response(session, target_url, results) for _ in range(concurrent_users)]
        test_start_time = time.perf_counter()
        await asyncio.gather(*tasks)
        total_duration = time.perf_counter() - test_start_time
        
    return results, total_duration

# Sonuçları analiz eden ve CSV dosyasına kaydeden fonksiyon
def analyze_and_save(results, duration, user_count, url):
    df = pd.DataFrame(results)
    success_rate = (df['is_success'].sum() / len(df)) * 100
    average_latency = df['latency'].mean()
    throughput = len(df) / duration 
    
    # Test tipini URL'den belirliyoruz (Raporlama kolaylığı için)
    test_type = "Blocking" if "non-blocking" not in url else "Non-Blocking"

    # Terminal çıktısı
    print(f"--- {test_type} Test Sonuçları ({user_count} Kullanıcı) ---")
    print(f"Toplam Test Süresi: {duration:.2f} saniye")
    print(f"Verimlilik (Throughput): {throughput:.2f} req/sec")
    print(f"Ortalama Yanıt Süresi: {average_latency:.4f} saniye")
    print(f"Başarı Oranı: %{success_rate:.2f}")
    print("-" * 55)

    # Verileri dosyaya kaydetme hazırlığı
    report_data = {
        'Model': [test_type],
        'User_Count': [user_count],
        'Throughput_Req_Sec': [round(throughput, 2)],
        'Avg_Latency_Sec': [round(average_latency, 4)],
        'Total_Duration_Sec': [round(duration, 2)],
        'Success_Rate': [f"%{success_rate}"]
    }
    
    report_df = pd.DataFrame(report_data)
    file_name = "test_results.csv"

    # Eğer dosya yoksa başlıklarla oluştur, varsa altına ekle (append)
    if not os.path.isfile(file_name):
        report_df.to_csv(file_name, index=False)
    else:
        report_df.to_csv(file_name, mode='a', header=False, index=False)

if __name__ == "__main__":
    # Test edilecek rotayı buradan seçiyoruz
    # BASE_URL = "http://localhost:3000/non-blocking" 
    BASE_URL = "http://localhost:3000/blocking" 
    
    LOAD_LEVELS = [10, 100, 500]

    for level in LOAD_LEVELS:
        print(f"\nSenaryo: {level} sanal kullanıcı sisteme yükleniyor...")
        test_data, duration = asyncio.run(run_load_simulation(BASE_URL, level))
        # Hem analiz yapıyoruz hem de CSV'ye kaydediyoruz
        analyze_and_save(test_data, duration, level, BASE_URL)