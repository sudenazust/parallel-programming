const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

// GÖREV 1: Senkron/Blocking Mod
// Senin görevin: "İşlemleri sırayla yapan (ağır bir döngü içeren) uç nokta."
app.get('/blocking', (req, res) => {
    const start = Date.now();
    console.log('Senkron istek geldi. Node.js Event Loop şu an KİLİTLENDİ...');

    // Bu döngü bitene kadar sunucu başka hiçbir isteğe cevap veremez!
    let counter = 0;
    for (let i = 0; i < 5_000_000_000; i++) {
        counter++;
    }

    const end = Date.now();
    res.status(200).json({
        mod: "Senkron (Blocking)",
        mesaj: `Ağır işlem bitti. Sayaç: ${counter}`,
        gecenSureMs: end - start
    });
});

// GÖREV 2: Asenkron/Non-blocking Mod
// Senin görevin: "Node.js'in doğal yapısını kullanarak istekleri bloklamadan karşılayan yapı."
app.get('/non-blocking', async (req, res) => {
    const start = Date.now();
    console.log('Asenkron istek geldi. Node.js arka planda beklerken diğer isteklere açık...');

    // 2 saniyelik bir veritabanı veya ağ isteğini simüle eder. Event Loop KİLİTLENMEZ!
    await new Promise(resolve => setTimeout(resolve, 2000));

    const end = Date.now();
    res.status(200).json({
        mod: "Asenkron (Non-Blocking)",
        mesaj: "2 saniyelik bekleme bitti, sunucu bu sürede hiç kilitlenmedi.",
        gecenSureMs: end - start
    });
});

// Sunucuyu Başlat
app.listen(PORT, () => {
    console.log(`Hedef sunucu çalışıyor!`);
    console.log(`Blocking Test: http://localhost:${PORT}/blocking`);
    console.log(`Non-blocking Test: http://localhost:${PORT}/non-blocking`);
});