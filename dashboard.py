import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Dashboard Penjualan", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("Data_Penjualan_Superstore.xlsx")

df = load_data()

# Judul dashboard
st.title("📊 Dashboard Penjualan Superstore")
st.markdown("Dashboard interaktif berdasarkan **Kategori Produk**, **Segmen Pelanggan**, dan **Waktu**.")

# Sidebar Filter
st.sidebar.header("🎛️ Filter Data")
kategori = st.sidebar.multiselect("Pilih Kategori Produk:", df["Kategori Produk"].unique(), default=df["Kategori Produk"].unique())
segmen = st.sidebar.multiselect("Pilih Segmen Pelanggan:", df["Segmen Pelanggan"].unique(), default=df["Segmen Pelanggan"].unique())
tanggal_awal = pd.to_datetime(df["Tanggal Pemesanan"]).min()
tanggal_akhir = pd.to_datetime(df["Tanggal Pemesanan"]).max()
tanggal = st.sidebar.date_input("Rentang Tanggal Pemesanan:", [tanggal_awal, tanggal_akhir])

# Filter data
df["Tanggal Pemesanan"] = pd.to_datetime(df["Tanggal Pemesanan"])
filtered_df = df[
    (df["Kategori Produk"].isin(kategori)) &
    (df["Segmen Pelanggan"].isin(segmen)) &
    (df["Tanggal Pemesanan"] >= pd.to_datetime(tanggal[0])) &
    (df["Tanggal Pemesanan"] <= pd.to_datetime(tanggal[1]))
]

# KPI
total_sales = filtered_df["Penjualan"].sum()
total_profit = filtered_df["Keuntungan"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales else 0
total_orders = filtered_df.shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penjualan", f"Rp {total_sales:,.0f}")
col2.metric("Total Keuntungan", f"Rp {total_profit:,.0f}")
col3.metric("Margin Keuntungan", f"{profit_margin:.2f}%")
col4.metric("Jumlah Transaksi", total_orders)

# Penjualan per Kategori Produk
st.subheader("📦 Penjualan per Kategori Produk")
sales_kat = filtered_df.groupby("Kategori Produk")["Penjualan"].sum().reset_index()
fig1, ax1 = plt.subplots()
sns.barplot(data=sales_kat, x="Penjualan", y="Kategori Produk", ax=ax1, palette="viridis")
st.pyplot(fig1)

# Keuntungan per Segmen
st.subheader("👥 Keuntungan per Segmen Pelanggan")
profit_seg = filtered_df.groupby("Segmen Pelanggan")["Keuntungan"].sum().reset_index()
fig2, ax2 = plt.subplots()
sns.barplot(data=profit_seg, x="Keuntungan", y="Segmen Pelanggan", ax=ax2, palette="pastel")
st.pyplot(fig2)

# Tren Penjualan Bulanan
st.subheader("📈 Tren Penjualan Bulanan")
df_trend = filtered_df.copy()
df_trend["Bulan"] = df_trend["Tanggal Pemesanan"].dt.to_period("M").astype(str)
monthly_sales = df_trend.groupby("Bulan")["Penjualan"].sum().reset_index()
fig3, ax3 = plt.subplots()
sns.lineplot(data=monthly_sales, x="Bulan", y="Penjualan", marker="o", ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

# Tabel Data
st.subheader("📄 Data Penjualan (Hasil Filter)")
st.dataframe(filtered_df)

# Download CSV
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Data sebagai CSV", data=csv, file_name="data_penjualan_filtered.csv", mime="text/csv")
