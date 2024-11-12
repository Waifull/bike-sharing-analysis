import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

data = pd.read_csv(r'C:\Users\Wafiul Achdi\Documents\data science\submission\dashboard\main_data.csv')

st.title("Dashboard Analisis Data Penyewaan Sepeda")



st.subheader("Distribusi Total Penyewaan, Suhu, Kelembapan, dan Kecepatan Angin")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
sns.histplot(data['total_sewa'], kde=True, ax=axes[0, 0]).set_title("Distribusi Total Penyewaan")
sns.histplot(data['suhu'], kde=True, ax=axes[0, 1]).set_title("Distribusi Suhu")
sns.histplot(data['kelembapan'], kde=True, ax=axes[1, 0]).set_title("Distribusi Kelembapan")
sns.histplot(data['kecepatan_angin'], kde=True, ax=axes[1, 1]).set_title("Distribusi Kecepatan Angin")
plt.tight_layout()
st.pyplot(fig)

with st.expander("Insight untuk distribusi"):
    st.write(
    """
    Insight dari setiap distribusi pada grafik di atas:

1. **Distribusi Total Penyewaan**: Grafik distribusi total penyewaan menunjukkan penyewaan cenderung berpusat di sekitar 4000–6000 kali per hari, dengan sedikit penurunan di atas 6000. Hal ini menandakan bahwa jumlah penyewaan terbanyak berada di sekitar nilai tengah, sementara permintaan ekstrem (baik sangat tinggi atau sangat rendah) jarang terjadi. **Insight**: Pengelola bisa fokus pada penambahan sepeda di area yang sering mencapai sekitar 4000–6000 penyewaan harian untuk efisiensi.

2. **Distribusi Suhu**: Distribusi suhu menunjukkan sebagian besar hari berada pada rentang suhu sedang, sekitar 0.2–0.6 (dalam skala normalisasi). **Insight**: Mayoritas penyewaan terjadi saat suhu sedang, menunjukkan bahwa pengguna cenderung bersepeda dalam kondisi yang nyaman.

3. **Distribusi Kelembapan**: Grafik kelembapan menunjukkan distribusi yang cenderung normal dengan puncak di sekitar 0.5–0.6. **Insight**: Kelembapan dalam rentang tersebut tampaknya paling umum terjadi, yang bisa berhubungan dengan kenyamanan pengguna saat bersepeda.

4. **Distribusi Kecepatan Angin**: Grafik menunjukkan bahwa kecepatan angin lebih sering rendah hingga sedang (sekitar 0.1–0.2), dengan jarang terjadi angin yang kencang. **Insight**: Kecepatan angin yang rendah ini mendukung kenyamanan bersepeda dan mungkin menjadi faktor yang mendorong penggunaan sepeda.

**Kesimpulan Umum**: Berdasarkan keempat distribusi, dapat disimpulkan bahwa kondisi yang nyaman (suhu sedang, kelembapan moderat, dan kecepatan angin rendah) mendukung aktivitas penyewaan sepeda. Pengelola bisa mempertimbangkan kondisi-kondisi ini untuk mengoptimalkan layanan sepeda di waktu-waktu tertentu.
    """
    )


st.subheader("Pengaruh Cuaca Terhadap Penyewaan Sepeda")
plt.figure(figsize=(10, 6))
sns.boxplot(x='cuaca', y='total_sewa', data=data, order=[1, 2, 3])
plt.title("Pengaruh Cuaca Terhadap Penyewaan Sepeda")
plt.xlabel("Situasi Cuaca")
plt.ylabel("Total Penyewaan")
plt.xticks(ticks=[0, 1, 2], labels=['Cerah', 'Mendung', 'Hujan'])
st.pyplot(plt)

with st.expander("Insight pengaruh cuaca"):
    st.write(
    """
    Insight dari pengaruh cuaca grafik di atas:

Penyewaan tertinggi terjadi saat cuaca cerah, dan menurun saat mendung atau hujan. Ini menunjukkan cuaca cerah lebih mendukung minat bersepeda.
    """
    )

st.subheader("Total Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
plt.figure(figsize=(10, 6))
sns.barplot(x='weekday', y='total_sewa', data=data, estimator=sum)
plt.title("Total Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
plt.xlabel("Hari dalam Seminggu")
plt.ylabel("Total Penyewaan")
plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
st.pyplot(plt)

with st.expander("Insight berdasarkan hari"):
    st.write(
    """
    Insight dari grafik di atas:

Penyewaan sepeda menunjukkan bahwa tingkat penyewaan cenderung lebih tinggi pada hari kerja dibandingkan dengan akhir pekan..
    """
    )

st.subheader("Tren Penyewaan Sepeda Seiring Waktu")
plt.figure(figsize=(14, 6))
sns.barplot(data=data, x='bulan', y='total_sewa')
plt.title("Tren Penyewaan Sepeda Seiring Waktu")
plt.xlabel("Bulan")
plt.ylabel("Total Penyewaan")
plt.xticks(rotation=45)
st.pyplot(plt)

with st.expander("Insight tren penyewaan"):
    st.write(
    """
    Insight dari grafik di atas:

Tren penyewaan menunjukkan pola musiman, dengan peningkatan selama musim panas dan gugur, saat cuaca lebih hangat. Pada musim dingin atau hujan, penyewaan turun signifikan. Insight ini dapat dimanfaatkan untuk strategi penempatan sepeda dan promosi di bulan-bulan sepi guna menjaga stabilitas pengguna sepanjang tahun.
    """
    )


data['tanggal'] = pd.to_datetime(data['tanggal'])


data['Recency'] = (data['tanggal'].max() - data['tanggal']).dt.days


data['Frequency'] = data['casual'] + data['registered']
data['Monetary'] = data['total_sewa']


rfm_data = data[['Recency', 'Frequency', 'Monetary']]


scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_data)


def assign_group(row):
    if row['Recency'] < 30 and row['Frequency'] > 5 and row['Monetary'] > 1000:
        return 'High Value'
    elif row['Recency'] < 60 and row['Frequency'] > 3:
        return 'Medium Value'
    else:
        return 'Low Value'

data['Cluster'] = data.apply(assign_group, axis=1)




st.subheader("Manual Grouping Based on Recency and Monetary")
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Recency', y='Monetary', hue='Cluster', data=data, palette='viridis')
plt.title("Manual Grouping Berdasarkan Recency dan Monetary")
plt.xlabel("Recency (days)")
plt.ylabel("Monetary (Total Rental)")
plt.legend()
st.pyplot(plt)

with st.expander("Insight RFM Analysis & Manual Grouping"):
    st.write(
    """
    Insight dari grafik di atas:

Setelah melakukan clustering pada data RFM, mendapatkan beberapa segmen pengguna berdasarkan perilaku mereka:
- **Low Value**: Mereka yang jarang menyewa sepeda dan menghabiskan sedikit uang. Kita perlu mencari cara untuk menarik perhatian mereka agar mau menyewa lebih sering.
- **Medium Value**: Mereka yang kadang-kadang menyewa sepeda dan menghabiskan jumlah uang yang sedang. Mereka memiliki potensi untuk menjadi pelanggan yang lebih baik jika kita memberikan perhatian lebih.
- **High Value**: Mereka yang sering menyewa sepeda dan menghabiskan banyak uang. Ini adalah pelanggan yang sangat berharga dan perlu kita jaga agar tetap loyal.

Analisis ini membantu memahami perilaku pengguna dan mengelompokkan mereka berdasarkan pola penyewaan sepeda.
    """
    )


