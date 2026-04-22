# Parallel Web Server Load Simulation - Hedef Sunucu

Bu proje, **Grup-2** Paralel Programlama ödevi kapsamında Node.js kullanılarak geliştirilmiş bir test sunucusudur. Projenin temel amacı, senkron (blocking) ve asenkron (non-blocking) mimarilerin yoğun yük altındaki (load testing) davranışlarını ve performans farklarını simüle etmektir.

## 🚀 Teknolojiler
* **Node.js & Express.js:** Sunucu altyapısı ve API uç noktaları.
* **Docker:** Test ortamının izole edilmesi ve her cihazda aynı şartlarda çalışabilmesi için.

## 📡 API Uç Noktaları (Endpoints)

Sunucu **3000** portunda çalışmaktadır ve test ekibinin yük testi yapabilmesi için iki farklı uç nokta sunar:

### 1. Senkron / Blocking Mod
* **Adres:** `GET http://localhost:3000/blocking`
* **Davranış:** Bu uç nokta, Node.js'in tek iş parçacıklı (single-threaded) yapısını bilerek kilitlemek için ağır bir matematiksel döngü (5 milyar iterasyon) çalıştırır. İşlem bitene kadar Event Loop kilitlenir ve sunucu diğer hiçbir isteğe yanıt veremez.

### 2. Asenkron / Non-blocking Mod
* **Adres:** `GET http://localhost:3000/non-blocking`
* **Davranış:** Bu uç nokta, arka plandaki I/O bekleme süresini (2 saniye) simüle eder. Event Loop kilitlenmez ve sunucu bu bekleme süresi boyunca yüzlerce yeni isteği kabul edip eşzamanlı olarak işlemeye devam eder.

---

## 🛠️ Nasıl Çalıştırılır?

Projeyi takım arkadaşlarınızın bilgisayarında çalıştırmak için iki farklı yöntem kullanabilirsiniz:

### Yöntem 1: Doğrudan Node.js ile (Lokal Ortam)
Bilgisayarınızda Node.js yüklüyse şu komutları sırayla terminale yazın:
```bash
# Bağımlılıkları kurun
npm install

# Sunucuyu başlatın
node index.js
