import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 
import seaborn as sns
import streamlit as st
from sklearn.linear_model import LinearRegression

st.title("Dashboard Penyewaan Sepeda")

def create_sum_count_df(df):
    create_sum_count_df = df.groupby("cnt").quantity_x.sum().sort_values(ascending=False).reset_index()
    return create_sum_count_df

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

day_df['date_day'] = pd.to_datetime(day_df['dteday'])
day_df.drop(columns=['dteday'], inplace=True)

hour_df['date_hour'] = pd.to_datetime(hour_df['dteday'])
hour_df.drop(columns=['dteday'], inplace=True)

min_date = min(day_df["date_day"].min(), hour_df["date_hour"].min())
max_date = max(day_df["date_day"].max(), hour_df["date_hour"].max())

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date, value=[min_date, max_date]
    )

filtered_day_df = day_df[(day_df["date_day"] >= str(start_date)) & 
                          (day_df["date_day"] <= str(end_date))]

filtered_hour_df = hour_df[(hour_df["date_hour"] >= str(start_date)) & 
                            (hour_df["date_hour"] <= str(end_date))]

st.subheader("Bagaimana Perkembangan penyewaan sepeda dari waktu ke waktu?")

tab1, tab2 = st.tabs(["Day Version Timeline", "Hour Version Timeline"])

with tab1:
    st.subheader("Jumlah penyewa per-waktu (Day Version)")
    plt.figure(figsize=(10, 5))
    plt.plot(
        filtered_day_df["date_day"],
        filtered_day_df["cnt"],
        marker='o', 
        linewidth=2,
        color="#72BCD4")
    plt.title("Jumlah penyewa per-waktu (Day Version)", loc="center", fontsize=20)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    st.pyplot(plt)

with tab2:
    st.subheader("Jumlah penyewa per-waktu (Hour Version)")
    plt.figure(figsize=(10, 5))
    plt.plot(
        filtered_hour_df["date_hour"],
        filtered_hour_df["cnt"],
        marker='o', 
        linewidth=2,
        color="#72BCD4"
    )
    plt.title("Jumlah penyewa per-waktu (Hour Version)", loc="center", fontsize=20)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    st.pyplot(plt)
    
st.subheader("Apakah ada perbedaan dalam weekday vs weekends?")

tab1, tab2 = st.tabs(["Timeline Jam", "Bar Chart"])

with tab1:
    weekdays_df = filtered_hour_df[filtered_hour_df['weekday'] < 5]  
    weekends_df = filtered_hour_df[filtered_hour_df['weekday'] >= 5]  

    hourly_rentals_weekdays = weekdays_df.groupby('hr')['cnt'].mean()
    hourly_rentals_weekends = weekends_df.groupby('hr')['cnt'].mean()
    
    plt.figure(figsize=(14, 6))

    # Weekdays plot
    plt.subplot(1, 2, 1)
    hourly_rentals_weekdays.plot(kind='line', color='blue', marker='o', linewidth=2)
    plt.title('Trend penyewaan sepeda dalam jam (Weekdays)')
    plt.xlabel('jam dalam hari')
    plt.ylabel('Rata-rata penyewaan')
    plt.xticks(range(24))  
    plt.grid(True)  

    # Weekends plot
    plt.subplot(1, 2, 2)
    hourly_rentals_weekends.plot(kind='line', color='green', marker='o', linewidth=2)
    plt.title('Trend penyewaan sepeda dalam jam (Weekends)')
    plt.xlabel('jam dalam hari')
    plt.ylabel('Rata-rata penyewaan')
    plt.xticks(range(24))  
    plt.grid(True)  

    plt.tight_layout()
    st.pyplot(plt)
    
with tab2:
    st.subheader("Bar Chart")
    average_rentals = filtered_day_df.groupby('holiday')['cnt'].mean()

    plt.figure(figsize=(4, 3))
    average_rentals.plot(kind='bar', color=['skyblue', 'lightgreen'])
    plt.title('Rata-rata penyewaan sepeda pada Hari Kerja vs Hari Libur')
    plt.xlabel('Holiday')
    plt.ylabel('Rata-rata penyewaan')
    plt.xticks([0, 1], ['Working Day', 'Holiday'], rotation=0)  
    plt.grid(axis='y')  
    st.pyplot(plt.gcf())
    
st.subheader("Apakah musim/kondisi cuaca mempengaruhi penyewa sepeda?")

tab1, tab2 = st.tabs(["Per-Musim", "Kondisi Cuaca"])

with tab1:
    season_avg_rentals = filtered_day_df.groupby('season')['cnt'].mean()
    season_labels = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']

    plt.figure(figsize=(8, 6))
    plt.bar(season_labels, season_avg_rentals, color='#72BCD4')
    plt.title('Rata-rata penyewaan sepeda per musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata penyewaan')
    plt.xticks(rotation=45)
    plt.grid(axis='y')  
    st.pyplot(plt)

with tab2:
    weather_variables = ['temp', 'atemp', 'hum', 'windspeed']
    bike_rentals = 'cnt'

    plt.figure(figsize=(12, 8))

    for i, weather_var in enumerate(weather_variables, 1):
        plt.subplot(2, 2, i)
        x = filtered_day_df[weather_var].values.reshape(-1, 1)
        y = filtered_day_df[bike_rentals]
        
        # Check for NaN values
        if filtered_day_df[weather_var].isnull().values.any() or filtered_day_df[bike_rentals].isnull().values.any():
            st.warning("Data contains NaN (missing) values. Linear regression cannot be performed.")
        else:
            plt.scatter(x, y, alpha=0.5, color='blue')
        
            model = LinearRegression()
            model.fit(x, y)
                
            plt.plot(x, model.predict(x), color='red', linewidth=2)
                
            plt.title(f'{weather_var.capitalize()} vs Penyewaan Sepeda')
            plt.xlabel(weather_var.capitalize())
            plt.ylabel('Penyewaan Sepeda')

    plt.tight_layout()
    st.pyplot(plt)

