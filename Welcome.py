import streamlit as st

st.title(" Welcome to Drowsiness Detection App! 🚗💤")

st.markdown("""
Selamat datang di **Aplikasi Deteksi Mengantuk**! 👋  
Aplikasi ini dirancang untuk mendeteksi tanda-tanda mengantuk pada pengemudi secara **real-time** menggunakan **YOLOv8**, model deteksi objek berbasis AI yang canggih. 🧠🤖  

---

### 🌟 Apa yang bisa aplikasi ini lakukan?  
- 🔍 **Deteksi Tanda Mengantuk:** Mendeteksi tanda-tanda mengantuk seperti mata tertutup atau menguap.  
- 🚨 **Peringatan Real-Time:** Memberikan peringatan jika mengantuk terdeteksi untuk meningkatkan keselamatan berkendara.  
- 🎯 **Akurasi Tinggi:** Menggunakan teknologi AI terbaru untuk hasil yang cepat dan akurat.

---

### 📋 Cara Menggunakan Aplikasi:
1. 🖱️ Gunakan **sidebar** dan pilih menu **Detect** untuk memulai deteksi mengantuk.  
2. 📷 **Aktifkan kamera** dengan menekan tombol **"Aktifkan"** agar aplikasi dapat mendeteksi secara real-time.  
3. 👀 Pantau deteksi secara langsung di layar aplikasi dengan informasi FPS dan 3 label: **Normal**, **Menguap**, dan **Microsleep**.  
4. 🔊 Saat aplikasi mendeteksi **Microsleep**, akan ada **suara peringatan** untuk pengendara.  

---

💡 **Catatan:** Pastikan perangkat Anda memiliki akses ke kamera untuk hasil terbaik! 📸✅  

---

### 🤖 Tentang YOLOv8  
YOLOv8 adalah model deteksi objek mutakhir dengan kemampuan mendeteksi sekaligus melakukan klasifikasi secara **real-time** dengan cepat dan akurat. Dengan teknologi ini, aplikasi dapat mengenali pola mengantuk berdasarkan wajah dan perilaku pengguna. ✨🧠  
""")

# Subheader tambahan
st.subheader("🚀 Keunggulan Utama Aplikasi")
st.markdown("""
- 😴 **Mendeteksi Microsleep dan Menguap:** Aplikasi dapat mengenali pola frekuensi kedipan mata dan menguap.  
- ⚡ **Performa Cepat:** Memanfaatkan kecepatan YOLOv8 untuk deteksi **real-time**.  
- 💻 **User-Friendly Interface:** Mudah digunakan oleh siapa saja tanpa memerlukan pengetahuan teknis.  
""")

st.caption("🛡️ Selalu utamakan keselamatan dalam berkendara. Jangan ragu untuk menggunakan aplikasi ini sebagai asisten Anda!")
