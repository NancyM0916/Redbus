import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import pybase64

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return pybase64.b64encode(data).decode()

img = get_img_as_base64("redbustiny.jpeg")

# Function to connect to the MySQL database and fetch data
def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Redbus_Scrapping"
    )
    query = "SELECT * FROM bus_details"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load the data
df = get_data()

# Setting streamlit page configuration
st.set_page_config(layout="wide", page_icon=":material/directions_bus:", page_title="RedBus Project", initial_sidebar_state="expanded")

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# Streamlit app
st.title("Redbus Data Analysis")

# Sidebar filters
st.sidebar.header("Filters")
selected_route = st.sidebar.selectbox("Select Route", df['route_name'].unique())
min_price, max_price = st.sidebar.slider("Price Range", float(df['price'].min()), float(df['price'].max()), (float(df['price'].min()), float(df['price'].max())))

# Filter the dataframe
filtered_df = df[(df['route_name'] == selected_route) & (df['price'] >= min_price) & (df['price'] <= max_price)]


# Visualizations
st.subheader("Visualizations")

# Function to create a chart with custom layout
def create_chart(fig, title):
    fig.update_layout(
        title=title,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black'),
    )
    return fig

# Price distribution
fig_price = px.histogram(filtered_df, x="price", title="Price Distribution", color="bus_type", color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(create_chart(fig_price, "Price Distribution"))

# Bus types
bus_type_counts = filtered_df['bus_type'].value_counts()
fig_bus_types = px.pie(values=bus_type_counts.values, names=bus_type_counts.index, title="Bus Types", color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(create_chart(fig_bus_types, "Bus Types"))

# Ratings vs Price
fig_ratings = px.scatter(filtered_df, x="price", y="rating", hover_data=["bus_name"], color="bus_type", title="Ratings vs Price", color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(create_chart(fig_ratings, "Ratings vs Price"))

# Bus Type vs Route
bus_type_route_counts = filtered_df.groupby(['bus_type', 'route_name']).size().reset_index(name='count')
fig_bus_type_route = px.bar(bus_type_route_counts, x='route_name', y='count', color='bus_type', title="Bus Type vs Route", barmode='group', color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(create_chart(fig_bus_type_route, "Bus Type vs Route"))

# Price vs Bus Type
fig_price_bus_type = px.box(filtered_df, x="bus_type", y="price", color="bus_type", title="Price Distribution by Bus Type", color_discrete_sequence=px.colors.qualitative.Dark2)
st.plotly_chart(create_chart(fig_price_bus_type, "Price Distribution by Bus Type"))

# Star Rating vs Bus Type
fig_rating_bus_type = px.box(filtered_df, x="bus_type", y="rating", color="bus_type", title="Star Rating Distribution by Bus Type", color_discrete_sequence=px.colors.qualitative.Prism)
st.plotly_chart(create_chart(fig_rating_bus_type, "Star Rating Distribution by Bus Type"))

# Price vs Route
fig_price_route = px.line(filtered_df, x='route_name', y='price', color='bus_type', title="Price vs Route (Line Chart)", markers=True, color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(create_chart(fig_price_route, "Price vs Route (Line Chart)"))

# Star Rating vs Route
fig_rating_route = px.strip(filtered_df, x="route_name", y="rating", color="bus_type", title="Star Rating vs Route", color_discrete_sequence=px.colors.qualitative.Vivid)
st.plotly_chart(create_chart(fig_rating_route, "Star Rating vs Route"))

# Seats Available vs Bus Type
seats_bus_type = filtered_df.groupby('bus_type')['seats_available'].mean().reset_index()
fig_seats_bus_type = px.bar(seats_bus_type, x='bus_type', y='seats_available', title="Average Seats Available by Bus Type", color='bus_type', color_discrete_sequence=px.colors.qualitative.Safe)
st.plotly_chart(create_chart(fig_seats_bus_type, "Average Seats Available by Bus Type"))



