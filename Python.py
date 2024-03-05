import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import streamlit as st
import warnings

warnings.filterwarnings("ignore")

def load_data():
    return pd.read_csv('day.csv', delimiter=',')

day_df = load_data()

business_questions = {
    "Pertanyaan 1": "Bagaimana distribusi pengguna biasa dan pengguna terdaftar dari waktu ke waktu?",
    "Pertanyaan 2": "Apa korelasi antara situasi cuaca dan jumlah penyewaan sepeda?"
}

# Sidebar untuk select pertanyaan
selected_question = st.sidebar.selectbox("Pilih Pertanyaan Bisnis:", list(business_questions.keys()))

st.title("Proyek Analisis Data: Bike Sharing Dataset")
st.write("Dibuat oleh: Agung Muhammad Sholeh", style="font-size: smaller;")
st.write("")
st.write("Link Dataset [Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset).")
st.write("")

st.subheader("Variabel dan Cuplikan Data")

# Display data
st.write("Cuplikan Data:")
st.write(day_df.head())

#Question
st.subheader("**Pertanyaan yang Dipilih:**")
st.write(f"{business_questions[selected_question]}")

# Exploratory Data Analysis
if selected_question == "Pertanyaan 1":
    st.subheader("Pertanyaan 1: Distribusi Pengguna Biasa dan Pengguna Terdaftar dari Waktu ke Waktu")
    if (day_df['casual'] > day_df['registered']).any():
        indexes = list(set(day_df.loc[day_df['casual'] > day_df['registered']].index))
        st.write("Ada nilai variabel 'casual' (Pengguna Biasa) yang melebihi nilai variabel 'registered' (Pengguna Terdaftar).")
        st.write("Tanggal 'dteday' di mana casual melebihi registered:")
        for index in indexes:
            date = day_df.loc[index, 'dteday']
            
            st.markdown(f'<span style="color:green;">{date}</span>', unsafe_allow_html=True)
    else:
        st.write("Tidak ada nilai variabel 'casual' yang melebihi nilai variabel 'registered'.")
    
    st.write("Hal ini menandakan bahwa selama periode 2 tahun dari awal tahun 2011 hingga akhir tahun 2012, hanya terjadi 3 hari di mana jumlah pengguna casual (tidak terdaftara) melebihi jumlah pengguna terdaftar. Artinya, sepanjang periode tersebut, kecuali pada 3 hari itu, jumlah pengguna terdaftar selalu lebih tinggi daripada jumlah pengguna casual (tidak terdaftar).")

elif selected_question == "Pertanyaan 2":
    st.subheader("Pertanyaan 2: Korelasi Antara Situasi Cuaca dan Jumlah Penyewaan Sepeda")
    correlation = day_df[['cnt', 'weathersit']].corr().iloc[0, 1] 
    st.write(f"<span style='color:green'>Korelasi antara situasi cuaca dan jumlah penyewaan sepeda: {correlation:.2f}</span>", unsafe_allow_html=True)

    st.write("Korelasi antara jumlah penyewaan sepeda dengan situasi cuaca adalah -0.30, yang menunjukkan adanya korelasi negatif antara kedua variabel tersebut. Ini berarti, secara umum, ketika situasi cuaca memburuk, jumlah penyewaan sepeda cenderung menurun, dan sebaliknya. Meskipun nilai korelasi tidak terlalu kuat, namun adanya korelasi negatif menunjukkan adanya pengaruh situasi cuaca terhadap pola penyewaan sepeda.")

st.header("Visualisasi")

# Display visualisasi berdasarkan selected question
if selected_question == "Pertanyaan 1":
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    date_format = day_df['dteday'].dt.to_period('M')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    sns.lineplot(x='dteday', y='casual', data=day_df, label='Casual', ax=ax)
    sns.lineplot(x='dteday', y='registered', data=day_df, label='Registered', ax=ax)
    
    ax.set_title('Distribusi Pengguna Biasa dan Pengguna Terdaftar dari Waktu ke Waktu')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Pengguna')
    ax.legend()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    
    st.pyplot(fig)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    st.write("Line chart di atas menunjukkan bahwa Pengguna registered (terdaftar) hampir selalu di atas casual dan pengguna registered (terdaftar) memiliki karakteristik dan pola penggunaan yang berbeda. Faktor eksternal seperti musim, kelembapan, atau yang lainnya dapat memengaruhi jumlah pengunjung. Maka, dapat disimpulkan pengunjung registered (terdaftar) memiliki intensitas penyewaan lebih banyak daripada pengunjung casual (tidak terdaftar).")

elif selected_question == "Pertanyaan 2":
    grouped_df = day_df.groupby('weathersit')['cnt'].agg(['count', 'mean', 'median', 'min', 'max', 'std']).round(2)
    grouped_df['q1'] = day_df.groupby('weathersit')['cnt'].quantile(0.25)
    grouped_df['q3'] = day_df.groupby('weathersit')['cnt'].quantile(0.75)
    grouped_df['iqr'] = grouped_df['q3'] - grouped_df['q1']
    
    plt.figure(figsize=(10, 5))
    
    sns.boxplot(x='weathersit', y='cnt', data=day_df)
    
    plt.title('Korelasi Antara Situasi Cuaca dan Jumlah Penyewaan Sepeda')
    plt.xlabel('Situasi Cuaca')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    
    st.pyplot()
    
    st.write(grouped_df)
    
    st.write("Boxplot di atas menunjukkan perbedaan yang signifikan dalam distribusi jumlah penyewaan sepeda di antara berbagai situasi cuaca. Situasi cuaca 1 (Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian) memiliki nilai median, kuartil pertama, dan kuartil ketiga yang secara signifikan lebih tinggi dibandingkan dengan situasi cuaca 2 (Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut) dan 3 (Salju Ringan, Hujan Ringan + Badai Petir + Awan berserakan, Hujan Ringan + Awan berserakan). Situasi cuaca 4 (Hujan Lebat + Palet Es + Badai Petir + Kabut, Salju + Kabut) tidak memiliki penyewa sepeda, mungkin karena situasi cuaca yang cukup ekstrim. Maka, situasi cuaca 1 akan menghasilkan banyak penyewa")