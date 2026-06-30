import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import time

# 1. Konfigurasi Halaman & Inisialisasi State di Awal
st.set_page_config(page_title="Kalkulator BMI", page_icon="⚖️")

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

def hitung_bmi(berat, tinggi):
    return berat / (tinggi ** 2)

def kategori_bmi(bmi):
    if bmi < 18.5:
        return "Kekurangan berat badan", "#3498db"  # Biru
    elif 18.5 <= bmi < 25.0:  # Diubah dari 24.9 agar presisi
        return "Berat badan normal", "#2ecc71"      # Hijau
    elif 25.0 <= bmi < 30.0:  # Diubah dari 29.9
        return "Kelebihan berat badan", "#f39c12"  # Oranye
    else:
        return "Obesitas", "#e74c3c"                # Merah

st.title("⚖️ Kalkulator BMI Sederhana")
st.write("Yuk cek kondisi berat badanmu dan pantau riwayatnya dalam grafik!")

# Input pengguna dengan nilai default rasional agar tidak kosong
col1, col2 = st.columns(2)
with col1:
    berat = st.number_input("Berat badan (kg):", min_value=1.0, value=60.0, step=0.1)
with col2:
    tinggi_cm = st.number_input("Tinggi badan (cm):", min_value=50.0, value=165.0, step=1.0)

if st.button("🔍 Hitung BMI", use_container_width=True):
    if tinggi_cm > 0:
        # Animasi loading sebelum hasil muncul
        with st.spinner("Menghitung BMI kamu..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.003)
                progress_bar.progress(i + 1)
            progress_bar.empty()

        tinggi_m = tinggi_cm / 100
        bmi = hitung_bmi(berat, tinggi_m)
        kategori, warna = kategori_bmi(bmi)
        waktu_cek = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Tampilkan hasil dengan balon dan kartu berwarna HTML yang dinamis
        st.balloons()
        st.markdown(
            f"""
            <div style="background-color:{warna}; padding:20px; border-radius:10px; text-align:center; color:white; margin-bottom:20px;">
                <h2 style="margin:0; color:white;">BMI Anda: {bmi:.2f}</h2>
                <h3 style="margin:5px 0; color:white; font-weight:bold;">{kategori}</h3>
                <p style="margin:0; font-size:14px; opacity:0.9;">📅 {waktu_cek}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Simpan ke dalam riwayat session state
        st.session_state.riwayat.append({
            "waktu": waktu_cek,
            "berat": berat,
            "tinggi_cm": tinggi_cm,
            "bmi": round(bmi, 2),
            "kategori": kategori
        })
    else:
        st.error("Tinggi badan harus lebih dari 0!")

# Grafik riwayat BMI (Hanya muncul jika riwayat sudah terisi data)
if st.session_state.riwayat:
    st.write("---")
    st.subheader("📈 Grafik Riwayat BMI")

    df = pd.DataFrame(st.session_state.riwayat)
    df["urutan"] = range(1, len(df) + 1)

    fig = go.Figure()

    # Garis tren BMI
    fig.add_trace(go.Scatter(
        x=df["urutan"],
        y=df["bmi"],
        mode="lines+markers+text",
        text=df["bmi"],
        textposition="top center",
        line=dict(color="#6c5ce7", width=3, shape="spline"),
        marker=dict(size=12, color="#6c5ce7", line=dict(width=2, color="white")),
        name="BMI"
    ))

    # Garis batas kategori (referensi visual)
    fig.add_hline(y=18.5, line_dash="dot", line_color="#3498db", annotation_text="Batas Kurus")
    fig.add_hline(y=25.0, line_dash="dot", line_color="#2ecc71", annotation_text="Batas Normal")
    fig.add_hline(y=30.0, line_dash="dot", line_color="#e74c3c", annotation_text="Batas Obesitas")

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=1, dtick=1),
        xaxis_title="Pengecekan ke-",
        yaxis_title="Nilai BMI",
        template="plotly_white",
        transition_duration=500,
        height=420,
        margin=dict(l=20, r=20, t=30, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Tombol reset riwayat dengan fungsi penataan ulang halaman
    if st.button("🗑️ Hapus Riwayat", use_container_width=True):
        st.session_state.riwayat = []
        st.rerun()
