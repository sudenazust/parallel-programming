# Sunucumuzun çalışacağı temel işletim sistemi ve Node.js sürümü
FROM node:18-alpine

# Konteyner içindeki çalışma klasörümüz
WORKDIR /app

# Sadece bağımlılık listesini kopyala ve kütüphaneleri (Express) kur
COPY package*.json ./
RUN npm install

# Yazdığımız index.js dahil tüm kodları konteynere kopyala
COPY . .

# Sunucumuzun dış dünyaya açılacağı port
EXPOSE 3000

# Konteyner ayağa kalktığında çalıştırılacak komut
CMD ["node", "index.js"]