


import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image




# df = pd.read_excel('/common/home/avp126/hackhers/finalEmp.xls', engine='openpyxl')  

# # Save it as CSV
# df.to_csv('/common/home/avp126/hackhers/finalEmp.xls', index=False)

df = pd.read_csv("/common/home/avp126/hackhers/emp.csv", delimiter=",")  

emotion_map = {
    "neutral": 0,
    "disgust": -1,
    "joy": 1,
    "anger": -2,
    "sadness": -1,
    "surprise": 0.5,
    "fear": -0.5
}


df['chat_emotion_numeric'] = df['chat_emotion'].map(emotion_map)
df['feedback_emotion_numeric'] = df['feedback_emotion'].map(emotion_map)

st.set_page_config(page_title="Employee Sentiment Dashboard", layout="wide")
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #000000;
    }
    .keycard {
        background-color: #1E2A47;  
        color: white;  
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        width: 250px;  
        height: 250px;
        margin-right: 20px; /* Adds space between keycard and the next element */
    }

    .keycard:hover {
        background-color: red;
        cursor: pointer;
    }
    .st-bb {
        background-color: #1E2A47;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

with st.sidebar:
    st.title("EmotoMetrics 😎")
    division_filter = st.selectbox("Select Office Division", df["Division/Organization"].unique())

filtered_df = df[df["Division/Organization"] == division_filter]

avg_chat_emotion = filtered_df['chat_emotion_numeric'].mean()
avg_feedback_emotion = filtered_df['feedback_emotion_numeric'].mean()
avg_chat_sentiment = filtered_df['chat_sentiment'].mean()
avg_feedback_sentiment = filtered_df['feedback_sentiment'].mean()

st.markdown("<h2 style='text-align: center; color: #FF6347;'>Key Metrics</h2>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)


def get_emoji(sentiment_value):
    if sentiment_value >= 0.5:
        return "😀"
    elif sentiment_value >= 0.0 and sentiment_value < 0.5:
        return "😲"  
    elif sentiment_value == 0:
        return "😐"  
    elif sentiment_value > -0.5 and sentiment_value < 0:
        return "😭"  
    elif sentiment_value <= -0.5:
        return "🤬"  
    elif sentiment_value == -1:
        return "🤢" 
    else:
        return "😐" 


chat_emoji = get_emoji(avg_chat_emotion)
feedback_emoji = get_emoji(avg_feedback_emotion)
chat_sentiment_emoji = get_emoji(avg_chat_sentiment)
feedback_sentiment_emoji = get_emoji(avg_feedback_sentiment)

with col1:
    st.markdown(f"<div class='keycard'><h3>Average Chat Emotion</h3><h4>{avg_chat_emotion:.2f}</h4><h3>{chat_emoji}</h3></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='keycard'><h3>Average Feedback Emotion</h3><h4>{avg_feedback_emotion:.2f}</h4><h3>{feedback_emoji}</h3></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='keycard'><h3>Average Chat Sentiment</h3><h4>{avg_chat_sentiment:.2f}</h4><h3>{chat_sentiment_emoji}</h3></div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='keycard'><h3>Average Feedback Sentiment</h3><h4>{avg_feedback_sentiment:.2f}</h4><h3>{feedback_sentiment_emoji}</h3></div>", unsafe_allow_html=True)


location_sentiment = df.groupby("Location of Office")[["chat_sentiment", "feedback_sentiment"]].mean().reset_index()

location_coords = {
    "Atlanta, GA": {"lat": 33.749, "lon": -84.388},
    "Los Angeles, CA": {"lat": 34.052, "lon": -118.243},
    "Boston, MA": {"lat": 42.360, "lon": -71.058},
    "New York, NY": {"lat": 40.7128, "lon": -74.006},
    "Dallas, TX": {"lat": 32.7767, "lon": -96.797},
    "Washington, D.C.": {"lat": 38.907, "lon": -77.037},
    "Denver, CO": {"lat": 39.739, "lon": -104.990},
    "Chicago, IL": {"lat": 41.8781, "lon": -87.6298},
    "Seattle, WA": {"lat": 47.6062, "lon": -122.3321},
    "San Francisco, CA": {"lat": 37.7749, "lon": -122.4194},
    "Austin, TX": {"lat": 30.2672, "lon": -97.7431},
    "Miami, FL": {"lat": 25.7617, "lon": -80.1918},
}

location_sentiment["lat"] = location_sentiment["Location of Office"].map(lambda x: location_coords.get(x, {}).get("lat", None))
location_sentiment["lon"] = location_sentiment["Location of Office"].map(lambda x: location_coords.get(x, {}).get("lon", None))

location_sentiment = location_sentiment.dropna()

location_sentiment["hover_text"] = location_sentiment.apply(
    lambda row: f"{row['Location of Office']}<br>Chat Sentiment: {row['chat_sentiment']:.2f}<br>Feedback Sentiment: {row['feedback_sentiment']:.2f}", axis=1
)

fig = px.scatter_geo(
    location_sentiment,
    lat="lat",
    lon="lon",
    hover_name="hover_text",
    color="chat_sentiment",
    color_continuous_scale="RdYlGn",  
    scope="usa",
)

fig.update_layout(
    autosize=True,
    geo=dict(showland=True, landcolor="lightgray", bgcolor="#1E2A47"),
    title_x=0.5,
    height=600,
    margin={"r":0,"t":0,"l":0,"b":0},  
    paper_bgcolor="#1E2A47", 
    plot_bgcolor="#1E2A47",  
    title="",  
)

st.plotly_chart(fig)
