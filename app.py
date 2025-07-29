import streamlit as st 
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# File CSV untuk penyimpanan permanen
CSV_FILE = "riwayat.csv"

# --------------------
# Fungsi bantu
# --------------------
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, parse_dates=["Tanggal"])
    else:
        return pd.DataFrame(columns=["Tanggal", "Tinggi (cm)", "Jenis Kelamin", "Berat Aktual", "Berat Ideal (kg)", "Status Gizi"])

def save_data(new_row):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return df

# --------------------
# Setup halaman
# --------------------
st.set_page_config(page_title="Kalkulator Berat Ideal", page_icon="🧮", layout="centered")

# Inisialisasi state history dari file CSV
if "history" not in st.session_state:
    st.session_state.history = load_data()

# --------------------
# Judul
# --------------------
st.markdown("""
<h1 style='text-align: center; color: #3882F6;'>💪 Kalkulator Berat Badan Ideal</h1>
<p style='text-align: center;'>Menggunakan Rumus Broca berdasarkan jenis kelamin</p>
<hr style='border: 1px solid #ccc;'>
""", unsafe_allow_html=True)

# --------------------
# Input
# --------------------
st.subheader("📝 Masukkan Data Anda")
col1, col2 = st.columns(2)
with col1:
    tinggi = st.number_input("📏 Tinggi Badan (cm)", min_value=100, max_value=250, step=1)
    berat = st.number_input("⚖️ Berat Badan Saat Ini (kg)", min_value=30.0, max_value=200.0, step=0.1)
with col2:
    jenis_kelamin = st.radio("👨 Jenis Kelamin", ["Pria", "Wanita"], horizontal=True)
    tanggal = st.date_input("📅 Tanggal Pengukuran", value=datetime.now().date())

# --------------------
# Hitung dan Simpan
# --------------------
if st.button("🔍 Hitung dan Simpan"):
    if tinggi > 0:
        dasar = tinggi - 100
        berat_ideal = dasar - (dasar * 0.10) if jenis_kelamin == "Pria" else dasar - (dasar * 0.15)

        # Klasifikasi status gizi
        if berat < berat_ideal * 0.9:
            status = "Kurus"
        elif berat > berat_ideal * 1.1:
            status = "Gemuk"
        else:
            status = "Ideal"

        # Simpan ke file CSV dan session state
        new_row = {
            "Tanggal": pd.to_datetime(tanggal),
            "Tinggi (cm)": tinggi,
            "Jenis Kelamin": jenis_kelamin,
            "Berat Aktual": berat,
            "Berat Ideal (kg)": round(berat_ideal, 1),
            "Status Gizi": status
        }
        df_updated = save_data(new_row)
        st.session_state.history = df_updated

        # Tampilkan hasil
        st.success("✅ Hasil Perhitungan")
        st.markdown(f"""
        <div style='text-align: center; font-size: 20px; background-color: #F3F4F6; border-radius: 10px'>
            <h2 style='color: #10B981;'>Berat Badan Ideal Anda: {berat_ideal:.1f} kg</h2>
            <h3 style='color: #F59E0B;'>Status Gizi: <span style='color: #EF4444'>{status}</span></h3>
            <p>Untuk {jenis_kelamin.lower()} dengan tinggi <b>{tinggi} cm</b> dan berat aktual <b>{berat} kg</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Silakan masukkan tinggi badan yang valid.")

# --------------------
# Tampilkan Riwayat
# --------------------
st.subheader("📚 Riwayat Perhitungan")
df = st.session_state.history
if not df.empty:
    st.dataframe(df.sort_values(by="Tanggal", ascending=False), use_container_width=True)
else:
    st.info("📖 Belum ada riwayat perhitungan yang disimpan.")

# --------------------
# Grafik
# --------------------
st.subheader("📈 Grafik Perkembangan Berat Badan")
if not df.empty:
    fig = px.line(
        df.sort_values(by="Tanggal"),
        x="Tanggal",
        y="Berat Aktual",
        title="Perkembangan Berat Badan",
        markers=True
    )
    fig.update_layout(
        xaxis_title="Tanggal",
        yaxis_title="Berat Badan (kg)"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📊 Tidak ada data untuk ditampilkan dalam grafik.")

# --------------------
# Footer
# --------------------
st.markdown("""
<hr>
<div style='text-align: center; font-size: 14px; color: gray;'>
    Dibuat dengan ❤️ menggunakan Streamlit & Plotly | Rumus Broca Method
</div>
""", unsafe_allow_html=True)
