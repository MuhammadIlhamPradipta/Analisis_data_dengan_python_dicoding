import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
st.title('Proyek Analisis Data :sparkles:')
st.header('Bike Sharing')


def create_registered_season_df(df) :
    registered_season = df.groupby('season')['registered'].sum().reset_index()
    return registered_season

def created_borrowers_by_time(df) :
    borrowers_by_time = df.groupby('hr')['cnt'].sum().reset_index()
    return borrowers_by_time


all_df = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by=datetime_columns, inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

temperature_value = all_df['temp'].iloc[0]  # Ambil nilai pertama

# Delta yang dinamis (sesuaikan sesuai kebutuhan)
delta_value = 0.1  # Contoh: Delta 0.1 °C

 
with st.sidebar:
    st.subheader('Filter')
    
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-photo/bikes-rent-street_1187-2187.jpg?w=996&t=st=1701745170~exp=1701745770~hmac=b76562aec9ab8262dcba85d8b52ce9756084fa91c4c4ccd66cbe1d04d38a1c1c")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Tampilkan Stat Card di Streamlit
    st.metric(label="Temperature", value=f"{temperature_value:.2f}", delta=f"{delta_value:.1f} °C")
    
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

registered_season = create_registered_season_df(main_df)
borrowers_by_time = created_borrowers_by_time(main_df)

#visualisasi
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_cnt = all_df['cnt'].sum()
    st.metric("Total Penyewa Sepeda", value=total_cnt)
 
with col2:
    total_casual = all_df['casual'].sum()
    st.metric("Total Penyewa Biasa", value=total_casual)
    
with col3:
    total_registered = all_df['registered'].sum()
    st.metric("Total Penyewa Terdaftar", value=total_registered)
 
st.subheader("Banyak Penyewa")

 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ['green' if val == registered_season['registered'].max() 
          else 'red' if val == registered_season['registered'].min() 
          else 'gray' for val in registered_season['registered']]

#Analisa Penyewa Berdasarkan Musim
st.subheader('Banyaknya Penyewa Berdasarkan Musim')
fig_musim, ax_musim = plt.subplots(figsize=(10, 6))
sns.barplot(x=registered_season['season'], y=registered_season['registered'], data=registered_season, palette=colors, ax=ax_musim)
ax_musim.set_title("Banyak Penyewa Berdasarkan Musim", loc="center")
ax_musim.set_xlabel("Musim")
ax_musim.set_ylabel('Jumlah Penyewa Sepeda')
st.pyplot(fig_musim)
 
#Analisa Penyewa Berdasarkan jam
st.subheader('Analisa Penyewa Sepeda Berdasarkan Jam')
fig_jam, ax_jam = plt.subplots(figsize=(10,6))
sns.lineplot(x=borrowers_by_time['hr'], y=borrowers_by_time['cnt'], data=borrowers_by_time, color='green', marker='o', ax=ax_jam)
ax_jam.set_ylabel('Jumlah Penyewa')
ax_jam.set_xlabel("Jam")
ax_jam.set_title("Banyaknya Penyewa Berdasarkan Jam", loc="center") 
st.pyplot(fig_jam)

# Analisis Pengaruh Cuaca
st.subheader('Analisis Pengaruh Cuaca')
fig_cuaca, ax_cuaca = plt.subplots(figsize=(10, 6))
sns.barplot(data=all_df, x='weathersit', y='cnt', ci=None, ax=ax_cuaca)
ax_cuaca.set_title('Analisis Pengaruh Cuaca')
ax_cuaca.set_xlabel('Weathersit')
ax_cuaca.set_ylabel('Jumlah Pengguna Sepeda')
st.pyplot(fig_cuaca)

# Analisis Pengaruh Hari Libur
st.subheader('Analisis Pengaruh Hari Libur')
fig_hari_libur, ax_hari_libur = plt.subplots(figsize=(8, 6))
sns.barplot(data=all_df, x='holiday', y='cnt', ci=None, ax=ax_hari_libur)
ax_hari_libur.set_title('Analisis Pengaruh Hari Libur')
ax_hari_libur.set_xlabel('Hari Libur')
ax_hari_libur.set_ylabel('Jumlah Pengguna Sepeda')
st.pyplot(fig_hari_libur)