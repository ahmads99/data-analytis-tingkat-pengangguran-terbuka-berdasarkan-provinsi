import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

# Helper function to process data
def create_monthly_unemployment_df(df):
    # Mengelompokkan data berdasarkan provinsi dan menghitung rata-rata tingkat pengangguran per bulan
    monthly_unemployment_df = df.groupby("Provinsi").agg({
        "Februari": "mean",
        "Agustus": "mean",
        "total_tingkat": "mean"
    }).reset_index()
    return monthly_unemployment_df

# Load dataset
df = pd.read_csv("./dataset/all_data_tingkatpeng.csv")

# Replace '-' with 0 and convert columns to numeric
df.replace('-', '0', inplace=True)
df[['Februari', 'Agustus']] = df[['Februari', 'Agustus']].apply(pd.to_numeric)
df['total_tingkat'] = df['Februari'] + df['Agustus']

# Prepare the DataFrame
monthly_unemployment_df = create_monthly_unemployment_df(df)

# Streamlit app
st.title("Tingkat Pengangguran Terbuka Menurut Provinsi (Persen), 2024")

# Sidebar
st.sidebar.image("./img/penga.jpg")
st.sidebar.header("Filter Data")

# Get unique provinces for filter
provinces = monthly_unemployment_df['Provinsi'].unique()
selected_provinces = st.sidebar.multiselect('Pilih Provinsi', provinces, default=provinces)

# Filter the DataFrame based on the selected provinces
filtered_df = monthly_unemployment_df[monthly_unemployment_df['Provinsi'].isin(selected_provinces)]

# Show metrics
st.header("Overview")

total_provinces = filtered_df['Provinsi'].nunique()
st.metric("Jumlah Provinsi", value=total_provinces)

avg_february = round(filtered_df['Februari'].mean(), 2)
avg_august = round(filtered_df['Agustus'].mean(), 2)
st.metric("Rata-rata Tingkat Pengangguran Februari", value=f"{avg_february}%")
st.metric("Rata-rata Tingkat Pengangguran Agustus", value=f"{avg_august}%")

# Plotting total tingkat pengangguran per provinsi
st.header("Total Tingkat Pengangguran Per Provinsi")

fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(x='total_tingkat', y='Provinsi', data=filtered_df, palette='viridis', ax=ax)
ax.set_title("Total Tingkat Pengangguran Per Provinsi")
ax.set_xlabel("Total Tingkat Pengangguran")
ax.set_ylabel("Provinsi")
st.pyplot(fig)

# Plotting monthly unemployment rate trends
st.header("Tren Tingkat Pengangguran Bulanan")

fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(filtered_df['Provinsi'], filtered_df['Februari'], marker='o', label='Februari', color='blue')
ax.plot(filtered_df['Provinsi'], filtered_df['Agustus'], marker='o', label='Agustus', color='red')
ax.set_title("Tren Tingkat Pengangguran")
ax.set_xlabel("Provinsi")
ax.set_ylabel("Tingkat Pengangguran")
ax.legend()
plt.xticks(rotation=90)
st.pyplot(fig)

# Setup for the Streamlit app
st.header('Visualisasi Data Tingkat Pengangguran')

# Plot scatter plot
st.subheader('Tingkat Pengangguran Februari vs Agustus Per Provinsi')

fig, ax = plt.subplots(figsize=(14, 8))  # Ukuran yang lebih besar untuk tampilan yang lebih baik

sns.scatterplot(
    x='Februari', 
    y='Agustus', 
    hue='Provinsi', 
    data=df, 
    palette='tab10', 
    s=100, 
    edgecolor='w', 
    ax=ax
)

ax.set_title('Tingkat Pengangguran Februari vs Agustus Per Provinsi', fontsize=16)
ax.set_xlabel('Tingkat Pengangguran Februari', fontsize=14)
ax.set_ylabel('Tingkat Pengangguran Agustus', fontsize=14)
ax.legend(title='Provinsi', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()  # Mengatur layout agar tidak ada elemen yang terpotong

st.pyplot(fig)

st.caption('Copyright © Benzodiahmads 2024')

