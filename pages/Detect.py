import streamlit as st
from ultralytics import YOLO
import cv2
import time
import pygame  # Import pygame untuk kontrol suara

# Inisialisasi pygame mixer untuk audio
pygame.mixer.init()

# Fungsi untuk mendeteksi dan mengklasifikasikan objek
def detect_and_classify(frame, yolo_model):
    global alert_playing

    yolo_results = yolo_model(frame)

    # Status deteksi MicroSleep
    micro_sleep_detected = False

    for r in yolo_results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Koordinat bounding box
            conf = box.conf[0]  # Confidence score
            class_id = int(box.cls[0])  # ID kelas

            class_name = yolo_model.names[class_id]

            if class_name == "Alert":
                class_name = "Normal"
                color = (0, 255, 0)  # Hijau untuk Normal
            elif class_name == "Yawn":
                class_name = "Mengantuk"
                color = (255, 0, 0)  # Biru untuk Menguap
            elif class_name == "MicroSleep":
                color = (0, 0, 255)  # Merah untuk MicroSleep
                micro_sleep_detected = True
                if not alert_playing:
                    # Jika MicroSleep terdeteksi dan suara belum dimainkan, putar suara
                    pygame.mixer.music.load('alert_sound.mp3')  # Pastikan file audio benar
                    pygame.mixer.music.play(-1)  # Memutar suara secara loop
                    alert_playing = True
            else:
                color = (255, 255, 255)  # Putih untuk kelas lain

            if conf > 0.5:
                # Gambarkan bounding box dan nama kelas
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Jika MicroSleep tidak terdeteksi lagi, berhenti memainkan suara
    if not micro_sleep_detected and alert_playing:
        pygame.mixer.music.stop()  # Berhenti memainkan suara
        alert_playing = False

    return frame

st.title("Ayo Mulai Deteksi 🚀")
st.markdown("""Untuk memulai deteksi, tekan tombol **"Aktifkan Kamera"** di bawah! 📸""")

# Fungsi untuk load model
@st.cache_resource
def load_model():
    model = YOLO('model/best.pt')
    return model

# Load model agar tidak berat
yolo_model = load_model()

# Inisialisasi status suara
alert_playing = False

# Session state untuk mengatur kamera
if "cap" not in st.session_state:
    st.session_state.cap = None
    st.session_state.running = False  # Status kamera

# Fungsi untuk menangani tombol
def toggle_camera():
    if st.session_state.running:
        # Stop kamera
        st.session_state.running = False
        if st.session_state.cap is not None:
            st.session_state.cap.release()
            st.session_state.cap = None
        st.rerun()
    else:
        # Aktifkan kamera
        st.session_state.cap = cv2.VideoCapture(0)
        st.session_state.running = True
        st.rerun()

# Tombol toggle kamera
button_label = "Stop Kamera" if st.session_state.running else "Aktifkan Kamera"
if st.button(button_label):
    toggle_camera()

# Menghitung FPS
frame_count = 0
fps = 0
start_time = time.time()

# Kamera aktif
if st.session_state.running and st.session_state.cap is not None:
    st_frame = st.empty()

    while st.session_state.running:
        ret, frame = st.session_state.cap.read()
        if not ret:
            st.error("Tidak dapat membaca data dari kamera.")
            break

        # Deteksi Yolo
        frame = detect_and_classify(frame, yolo_model)

        # Hitung FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 1:
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = time.time()

        # Tampilkan FPS di frame
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st_frame.image(frame, channels="RGB")
