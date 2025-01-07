import streamlit as st
from ultralytics import YOLO
import cv2
import time

def detect_and_classify(frame, yolo_model):
    yolo_results = yolo_model(frame)

    for r in yolo_results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Koordinat bounding box
            conf = box.conf[0]  # Confidence score
            class_id = int(box.cls[0])  # ID kelas

            class_name = yolo_model.names[class_id]

            if class_name == "Alert":
                color = (0, 255, 0)  # Hijau untuk Normal
            elif class_name == "Yawn":
                color = (255, 0, 0)  # Biru untuk Menguap
            elif class_name == "MicroSleep":
                color = (0, 0, 255)  # Merah untuk MicroSleep
            else:
                color = (255, 255, 255)  # Putih untuk kelas lain

            if conf > 0.5:
                # Gambarkan bounding box dan nama kelas
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame

st.title("Deteksi Mengantuk menggunakan YOLO")
st.text("Aktifkan kamera untuk mendeteksi")

# Fungsi untuk load model
@st.cache_resource
def load_model():
    model = YOLO('model/best.pt')
    return model

#load model agar tidak berat
yolo_model = load_model()

col1, col2 = st.columns(2)

with col1:
    run_camera = st.button("Aktifkan Kamera")

with col2:
    stop_camera = st.button("Stop Kamera")

if "cap" not in st.session_state:
    st.session_state.cap = None

if run_camera and st.session_state.cap is None:
    st.session_state.cap = cv2.VideoCapture(0)
    st.session_state.running = True

# Menghitung FPS
frame_count = 0
fps = 0 
start_time = time.time()

if st.session_state.cap is not None and st.session_state.running:
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
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st_frame.image(frame, channels="RGB")

        if stop_camera:
            st.session_state.running = False
            st.session_state.cap.release()
            st.session_state.cap = None
            st.success("Kamera telah dihentikan.")
