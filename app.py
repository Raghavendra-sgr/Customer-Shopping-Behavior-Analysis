import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Customer Shopping Analysis",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* AI-themed particle background */
    .main {
        background: #0a0e27;
        background-image: 
            radial-gradient(at 40% 20%, rgba(102, 126, 234, 0.3) 0px, transparent 50%),
            radial-gradient(at 80% 0%, rgba(118, 75, 162, 0.3) 0px, transparent 50%),
            radial-gradient(at 0% 50%, rgba(79, 172, 254, 0.3) 0px, transparent 50%),
            radial-gradient(at 80% 50%, rgba(240, 147, 251, 0.3) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(102, 126, 234, 0.3) 0px, transparent 50%),
            radial-gradient(at 80% 100%, rgba(118, 75, 162, 0.3) 0px, transparent 50%);
        position: relative;
        font-family: 'Inter', sans-serif;
        animation: backgroundPulse 20s ease infinite;
    }
    
    @keyframes backgroundPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.95; }
    }
    
    /* Neural network grid pattern */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(102, 126, 234, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(102, 126, 234, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        z-index: 0;
        pointer-events: none;
    }
    
    /* Glassmorphism effect for containers */
    .block-container {
        background: rgba(10, 14, 39, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 2.5rem;
        box-shadow: 
            0 8px 32px 0 rgba(0, 0, 0, 0.5),
            inset 0 0 0 1px rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        position: relative;
        overflow: visible;
    }
    
    /* AI-style metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2.8rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, #00f5ff 0%, #667eea 50%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s linear infinite;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.9) 0%, rgba(20, 24, 49, 0.9) 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 0 0 1px rgba(102, 126, 234, 0.3),
            0 0 40px rgba(102, 126, 234, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00f5ff, #667eea, #ff00ff, #667eea);
        border-radius: 20px;
        opacity: 0;
        z-index: -1;
        transition: opacity 0.4s;
        animation: rotate 4s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    [data-testid="stMetric"]:hover::before {
        opacity: 1;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(102, 126, 234, 0.4),
            0 0 80px rgba(102, 126, 234, 0.3),
            inset 0 0 0 1px rgba(102, 126, 234, 0.5);
    }
    
    /* Futuristic headers with neon glow */
    h1 {
        color: #ffffff !important;
        text-shadow: 
            0 0 10px rgba(0, 245, 255, 0.8),
            0 0 20px rgba(102, 126, 234, 0.6),
            0 0 30px rgba(102, 126, 234, 0.4),
            0 0 40px rgba(102, 126, 234, 0.3);
        font-size: 4rem !important;
        font-weight: 800 !important;
        text-align: center;
        letter-spacing: -2px;
        animation: neonGlow 2s ease-in-out infinite alternate;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes neonGlow {
        from { 
            text-shadow: 
                0 0 10px rgba(0, 245, 255, 0.8),
                0 0 20px rgba(102, 126, 234, 0.6),
                0 0 30px rgba(102, 126, 234, 0.4);
        }
        to { 
            text-shadow: 
                0 0 20px rgba(0, 245, 255, 1),
                0 0 30px rgba(102, 126, 234, 0.8),
                0 0 40px rgba(102, 126, 234, 0.6),
                0 0 50px rgba(102, 126, 234, 0.4);
        }
    }
    
    h2, h3, h4 {
        color: #00f5ff !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        letter-spacing: -0.5px;
    }
    
    /* AI Command Center Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e27 0%, #141830 50%, #1a1f3a 100%);
        box-shadow: 
            4px 0 30px rgba(0, 0, 0, 0.5),
            inset -1px 0 0 rgba(102, 126, 234, 0.3);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    [data-testid="stSidebar"] label {
        color: #00f5ff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* Sidebar widgets styling */
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stSlider {
        background: rgba(20, 24, 49, 0.6);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin-bottom: 1rem;
    }
    
    /* AI-Style Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(10, 14, 39, 0.8);
        padding: 15px;
        border-radius: 20px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 
            inset 0 0 20px rgba(102, 126, 234, 0.1),
            0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(20, 24, 49, 0.6);
        border-radius: 12px;
        padding: 12px 24px;
        color: #00f5ff;
        font-weight: 600;
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.2) 0%, rgba(102, 126, 234, 0.3) 100%);
        border: 2px solid #00f5ff;
        box-shadow: 
            0 0 20px rgba(0, 245, 255, 0.4),
            0 4px 20px rgba(102, 126, 234, 0.4),
            inset 0 0 20px rgba(0, 245, 255, 0.1);
        color: #ffffff;
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        color: white !important;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Futuristic Buttons */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.2) 0%, rgba(102, 126, 234, 0.3) 100%);
        color: #00f5ff;
        font-weight: 700;
        border-radius: 12px;
        padding: 12px 32px;
        border: 2px solid rgba(0, 245, 255, 0.5);
        box-shadow: 
            0 0 20px rgba(0, 245, 255, 0.3),
            0 4px 20px rgba(0, 0, 0, 0.3),
            inset 0 0 10px rgba(0, 245, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 
            0 0 40px rgba(0, 245, 255, 0.6),
            0 8px 30px rgba(0, 245, 255, 0.4),
            inset 0 0 20px rgba(0, 245, 255, 0.2);
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.3) 0%, rgba(102, 126, 234, 0.4) 100%);
        border-color: #00f5ff;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.2) 0%, rgba(245, 87, 108, 0.3) 100%);
        color: #ff00ff;
        font-weight: 700;
        border-radius: 12px;
        padding: 12px 32px;
        border: 2px solid rgba(255, 0, 255, 0.5);
        box-shadow: 
            0 0 20px rgba(255, 0, 255, 0.3),
            0 4px 20px rgba(0, 0, 0, 0.3),
            inset 0 0 10px rgba(255, 0, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 
            0 0 40px rgba(255, 0, 255, 0.6),
            0 8px 30px rgba(255, 0, 255, 0.4),
            inset 0 0 20px rgba(255, 0, 255, 0.2);
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.3) 0%, rgba(245, 87, 108, 0.4) 100%);
        border-color: #ff00ff;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Info box with modern styling */
    .stAlert {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-left: 4px solid #667eea;
        color: white;
        border-radius: 10px;
    }
    
    /* AI-Enhanced Plotly charts with continuous animation */
    .js-plotly-plot {
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.95) 0%, rgba(20, 24, 49, 0.95) 100%);
        padding: 15px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 0 0 1px rgba(102, 126, 234, 0.2),
            0 0 40px rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        animation: chartPulse 4s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes chartPulse {
        0%, 100% {
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 0 0 1px rgba(102, 126, 234, 0.2),
                0 0 40px rgba(102, 126, 234, 0.1);
        }
        50% {
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.5),
                inset 0 0 0 1px rgba(0, 245, 255, 0.4),
                0 0 60px rgba(0, 245, 255, 0.3);
        }
    }
    
    .js-plotly-plot::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(0, 245, 255, 0.1) 50%,
            transparent 70%
        );
        animation: chartSweep 3s linear infinite;
    }
    
    @keyframes chartSweep {
        0% {
            transform: translateX(-100%) translateY(-100%) rotate(45deg);
        }
        100% {
            transform: translateX(100%) translateY(100%) rotate(45deg);
        }
    }
    
    .js-plotly-plot:hover {
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.5),
            inset 0 0 0 1px rgba(102, 126, 234, 0.4),
            0 0 60px rgba(0, 245, 255, 0.4);
        transform: translateY(-2px) scale(1.01);
        animation: chartPulse 2s ease-in-out infinite;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("""
    <div style='text-align: center; padding: 2.5rem 0 1.5rem 0; position: relative;'>
        <div style='display: inline-block; position: relative;'>
            <h1 style='margin-bottom: 0.5rem; position: relative; z-index: 1;'>
                DATA ANALYTICS
            </h1>
            <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 120%; height: 120%; background: radial-gradient(circle, rgba(0, 245, 255, 0.2) 0%, transparent 70%); filter: blur(30px); z-index: 0;'></div>
        </div>
        <p style='color: #00f5ff; font-size: 1.4rem; text-shadow: 0 0 20px rgba(0, 245, 255, 0.6); font-weight: 400; margin-top: 1rem; letter-spacing: 2px; text-transform: uppercase;'>
            ⚡ Customer Shopping Intelligence Dashboard ⚡
        </p>
        <p style='color: rgba(255, 255, 255, 0.7); font-size: 0.95rem; margin-top: 0.5rem; font-family: "JetBrains Mono", monospace;'>
            [ SQL • POWER BI ]
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("customer_shopping_behavior.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(102, 126, 234, 0.1) 100%); border-radius: 15px; margin-bottom: 1.5rem; border: 1px solid rgba(0, 245, 255, 0.3); box-shadow: 0 0 20px rgba(0, 245, 255, 0.2), inset 0 0 20px rgba(0, 245, 255, 0.05);'>
        <h2 style='color: #00f5ff; margin: 0; font-size: 1.6rem; text-shadow: 0 0 15px rgba(0, 245, 255, 0.6); letter-spacing: 2px; font-weight: 800;'>⚙️ CONTROL PANEL</h2>
        <p style='color: rgba(255, 255, 255, 0.6); font-size: 0.75rem; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 1px;'>Advanced Filtering System</p>
    </div>
""", unsafe_allow_html=True)

gender = st.sidebar.multiselect(
    "👥 Select Gender",
    options=sorted(df["Gender"].unique()),
    default=list(df["Gender"].unique())
)

category = st.sidebar.multiselect(
    "🏷️ Select Category",
    options=sorted(df["Category"].unique()),
    default=list(df["Category"].unique())
)

season = st.sidebar.multiselect(
    "🌦️ Select Season",
    options=sorted(df["Season"].unique()),
    default=list(df["Season"].unique())
)

# Age range filter
age_range = st.sidebar.slider(
    "🎂 Age Range",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(int(df["Age"].min()), int(df["Age"].max()))
)

# Purchase amount filter
purchase_range = st.sidebar.slider(
    "💰 Purchase Amount (USD)",
    min_value=int(df["Purchase Amount (USD)"].min()),
    max_value=int(df["Purchase Amount (USD)"].max()),
    value=(int(df["Purchase Amount (USD)"].min()), int(df["Purchase Amount (USD)"].max()))
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(0, 245, 255, 0.1) 100%); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(0, 245, 255, 0.3); box-shadow: 0 0 20px rgba(0, 245, 255, 0.2);'>
        <p style='color: #00f5ff; margin: 0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 0.5rem;'>
            📊 DATA INSIGHTS
        </p>
        <p style='color: rgba(255, 255, 255, 0.85); margin: 0; font-size: 0.85rem; line-height: 1.5;'>
            Utilize advanced filters to segment customer data and uncover predictive patterns in real-time.
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["Gender"].isin(gender)) &
    (df["Category"].isin(category)) &
    (df["Season"].isin(season)) &
    (df["Age"].between(age_range[0], age_range[1])) &
    (df["Purchase Amount (USD)"].between(purchase_range[0], purchase_range[1]))
]

# ---------------- KPIs ----------------
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem; padding: 1.5rem; background: rgba(10, 14, 39, 0.6); border-radius: 20px; border: 1px solid rgba(0, 245, 255, 0.3); box-shadow: 0 0 30px rgba(0, 245, 255, 0.2);'>
        <h2 style='color: #00f5ff; font-size: 2.2rem; margin-bottom: 0.3rem; text-transform: uppercase; letter-spacing: 3px; font-weight: 800;'>⚡ LIVE METRICS</h2>
        <p style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; font-family: "JetBrains Mono", monospace; text-transform: uppercase; letter-spacing: 2px;'>Real-time Performance Dashboard</p>
        <div style='margin-top: 0.8rem; padding: 0.5rem; background: rgba(0, 245, 255, 0.05); border-radius: 10px; display: inline-block;'>
            <span style='color: #00ff00; font-size: 0.75rem; font-family: "JetBrains Mono", monospace;'>● SYSTEM ACTIVE</span>
            <span style='color: rgba(255, 255, 255, 0.5); margin: 0 1rem;'>|</span>
            <span style='color: rgba(255, 255, 255, 0.6); font-size: 0.75rem; font-family: "JetBrains Mono", monospace;'>DATA STREAM: ONLINE</span>
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div style='text-align: center; padding: 0.8rem 0;'>
            <p style='color: #00f5ff; font-size: 0.75rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);'>
                👥 CUSTOMERS
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.metric(
        label="",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df)}" if len(filtered_df) != len(df) else None,
        label_visibility="collapsed"
    )

with col2:
    total_revenue = filtered_df["Purchase Amount (USD)"].sum()
    st.markdown("""
        <div style='text-align: center; padding: 0.8rem 0;'>
            <p style='color: #00f5ff; font-size: 0.75rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);'>
                💰 REVENUE
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.metric(
        label="",
        value=f"${total_revenue:,.0f}",
        delta=None,
        label_visibility="collapsed"
    )

with col3:
    avg_purchase = filtered_df["Purchase Amount (USD)"].mean()
    st.markdown("""
        <div style='text-align: center; padding: 0.8rem 0;'>
            <p style='color: #00f5ff; font-size: 0.75rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);'>
                📈 AVG PURCHASE
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.metric(
        label="",
        value=f"${avg_purchase:.2f}",
        delta=None,
        label_visibility="collapsed"
    )

with col4:
    avg_rating = filtered_df["Review Rating"].mean()
    st.markdown("""
        <div style='text-align: center; padding: 0.8rem 0;'>
            <p style='color: #00f5ff; font-size: 0.75rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);'>
                ⭐ RATING
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.metric(
        label="",
        value=f"{avg_rating:.2f}",
        delta=None,
        label_visibility="collapsed"
    )

st.markdown("---")

# ---------------- MAIN CHARTS SECTION ----------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💳 Purchase Analysis", "👥 Customer Insights", "📈 Trends"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='padding: 1rem 0 0.5rem 0;'>
                <h4 style='margin: 0; font-size: 1.2rem;'>🏷️ REVENUE BY CATEGORY</h4>
                <p style='color: rgba(255, 255, 255, 0.6); font-size: 0.75rem; margin-top: 0.3rem;'>Product Performance Analysis</p>
            </div>
        """, unsafe_allow_html=True)
        category_revenue = filtered_df.groupby("Category")["Purchase Amount (USD)"].sum().sort_values(ascending=True)
        fig1 = px.bar(
            x=category_revenue.values,
            y=category_revenue.index,
            orientation='h',
            labels={'x': 'Revenue (USD)', 'y': 'Category'},
            color=category_revenue.values,
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            transition={'duration': 800, 'easing': 'cubic-in-out'}
        )
        fig1.update_traces(
            marker=dict(line=dict(color='rgba(0, 245, 255, 0.3)', width=1)),
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
        )
        st.plotly_chart(fig1, use_container_width=True, key="chart1", config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
            <div style='padding: 1rem 0 0.5rem 0;'>
                <h4 style='margin: 0; font-size: 1.2rem;'>👥 GENDER DISTRIBUTION</h4>
                <p style='color: rgba(255, 255, 255, 0.6); font-size: 0.75rem; margin-top: 0.3rem;'>Customer Demographics</p>
            </div>
        """, unsafe_allow_html=True)
        gender_counts = filtered_df["Gender"].value_counts()
        fig2 = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig2.update_layout(
            height=400,
            transition={'duration': 800, 'easing': 'elastic-out'}
        )
        fig2.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>',
            pull=[0.08] * len(gender_counts),
            rotation=90
        )
        st.plotly_chart(fig2, use_container_width=True, key="chart2", config={'displayModeBar': False})
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 🌦️ Seasonal Revenue")
        season_revenue = filtered_df.groupby("Season")["Purchase Amount (USD)"].sum()
        fig3 = px.bar(
            x=season_revenue.index,
            y=season_revenue.values,
            labels={'x': 'Season', 'y': 'Revenue (USD)'},
            color=season_revenue.values,
            color_continuous_scale='Sunset'
        )
        fig3.update_layout(
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            transition={'duration': 800, 'easing': 'cubic-in-out'}
        )
        fig3.update_traces(
            marker=dict(line=dict(color='rgba(0, 245, 255, 0.3)', width=1)),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        )
        st.plotly_chart(fig3, use_container_width=True, key="chart3", config={'displayModeBar': False})
    
    with col4:
        st.markdown("#### ⭐ Rating Distribution")
        fig4 = px.histogram(
            filtered_df,
            x="Review Rating",
            nbins=10,
            labels={'Review Rating': 'Rating'},
            color_discrete_sequence=['#667eea']
        )
        fig4.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            transition={'duration': 800, 'easing': 'cubic-in-out'}
        )
        fig4.update_traces(
            marker=dict(line=dict(color='rgba(0, 245, 255, 0.3)', width=1)),
            hovertemplate='<b>Rating: %{x}</b><br>Count: %{y}<extra></extra>'
        )
        st.plotly_chart(fig4, use_container_width=True, key="chart4", config={'displayModeBar': False})

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💳 Payment Method Usage")
        payment_counts = filtered_df["Payment Method"].value_counts()
        fig5 = px.pie(
            values=payment_counts.values,
            names=payment_counts.index,
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig5.update_layout(
            height=400,
            transition={'duration': 800, 'easing': 'elastic-out'}
        )
        fig5.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>',
            pull=[0.08] * len(payment_counts),
            rotation=45
        )
        st.plotly_chart(fig5, use_container_width=True, key="chart5", config={'displayModeBar': False})
    
    with col2:
        st.markdown("#### 🎯 Discount vs Non-Discount")
        discount_revenue = filtered_df.groupby("Discount Applied")["Purchase Amount (USD)"].sum()
        fig6 = go.Figure(data=[go.Pie(
            labels=['Discount Applied' if x == 'Yes' else 'No Discount' for x in discount_revenue.index],
            values=discount_revenue.values,
            hole=.3,
            marker_colors=['#667eea', '#764ba2'],
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Percent: %{percent}<extra></extra>',
            pull=[0.05, 0.05]
        )])
        fig6.update_layout(
            height=400,
            transition={'duration': 800, 'easing': 'elastic-out'}
        )
        st.plotly_chart(fig6, use_container_width=True, key="chart6", config={'displayModeBar': False})
    
    st.markdown("#### 📦 Category vs Gender - Purchase Amount")
    category_gender = filtered_df.groupby(["Category", "Gender"])["Purchase Amount (USD)"].sum().reset_index()
    fig7 = px.bar(
        category_gender,
        x="Category",
        y="Purchase Amount (USD)",
        color="Gender",
        barmode="group",
        color_discrete_sequence=['#667eea', '#764ba2']
    )
    fig7.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition={'duration': 800, 'easing': 'cubic-in-out'}
    )
    fig7.update_traces(
        marker=dict(line=dict(color='rgba(0, 245, 255, 0.3)', width=1)),
        hovertemplate='<b>%{x}</b><br>%{fullData.name}<br>Revenue: $%{y:,.0f}<extra></extra>'
    )
    st.plotly_chart(fig7, use_container_width=True, key="chart7", config={'displayModeBar': False})

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎂 Age Distribution")
        fig8 = px.histogram(
            filtered_df,
            x="Age",
            nbins=20,
            color_discrete_sequence=['#667eea']
        )
        fig8.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            transition={'duration': 800, 'easing': 'cubic-in-out'}
        )
        fig8.update_traces(
            marker=dict(line=dict(color='rgba(0, 245, 255, 0.3)', width=1)),
            hovertemplate='<b>Age: %{x}</b><br>Count: %{y}<extra></extra>'
        )
        st.plotly_chart(fig8, use_container_width=True, key="chart8", config={'displayModeBar': False})
    
    with col2:
        st.markdown("#### 📍 Top 10 Locations")
        location_counts = filtered_df["Location"].value_counts().head(10)
        fig9 = px.bar(
            x=location_counts.values,
            y=location_counts.index,
            orientation='h',
            labels={'x': 'Number of Purchases', 'y': 'Location'},
            color=location_counts.values,
            color_continuous_scale='Teal'
        )
        fig9.update_layout(
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            transition={'duration': 800, 'easing': 'cubic-in-out'}
        )
        fig9.update_traces(
            marker=dict(line=dict(color='rgba(0, 245, 255, 0.3)', width=1)),
            hovertemplate='<b>%{y}</b><br>Purchases: %{x}<extra></extra>'
        )
        st.plotly_chart(fig9, use_container_width=True, key="chart9", config={'displayModeBar': False})
    
    st.markdown("#### 📊 Purchase Amount vs Age")
    # Filter out rows with NaN Review Rating for scatter plot
    scatter_data = filtered_df.dropna(subset=['Review Rating'])
    if len(scatter_data) > 0:
        sample_size = min(1000, len(scatter_data))
        fig10 = px.scatter(
            scatter_data.sample(sample_size),
            x="Age",
            y="Purchase Amount (USD)",
            color="Gender",
            size="Review Rating",
            hover_data=["Category", "Season"],
            color_discrete_sequence=['#667eea', '#764ba2']
        )
        fig10.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            transition={'duration': 800, 'easing': 'elastic-out'}
        )
        fig10.update_traces(
            marker=dict(line=dict(color='rgba(0, 245, 255, 0.3)', width=0.5)),
            hovertemplate='<b>Age: %{x}</b><br>Purchase: $%{y:,.2f}<br>Rating: %{marker.size}<extra></extra>'
        )
        st.plotly_chart(fig10, use_container_width=True, key="chart10", config={'displayModeBar': False})
    else:
        st.info("No data available for this chart with current filters.")

with tab4:
    st.markdown("#### 🔁 Frequency of Purchases")
    freq_counts = filtered_df["Frequency of Purchases"].value_counts()
    fig11 = px.bar(
        x=freq_counts.index,
        y=freq_counts.values,
        labels={'x': 'Frequency', 'y': 'Count'},
        color=freq_counts.values,
        color_continuous_scale='Purples'
    )
    fig11.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition={'duration': 800, 'easing': 'cubic-in-out'}
    )
    fig11.update_traces(
        marker=dict(line=dict(color='rgba(0, 245, 255, 0.3)', width=1)),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    )
    st.plotly_chart(fig11, use_container_width=True, key="chart11", config={'displayModeBar': False})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📦 Subscription Status")
        sub_counts = filtered_df["Subscription Status"].value_counts()
        fig12 = px.pie(
            values=sub_counts.values,
            names=sub_counts.index,
            hole=0.4,
            color_discrete_sequence=['#667eea', '#764ba2']
        )
        fig12.update_layout(
            height=400,
            transition={'duration': 800, 'easing': 'elastic-out'}
        )
        fig12.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>',
            pull=[0.08] * len(sub_counts),
            rotation=135
        )
        st.plotly_chart(fig12, use_container_width=True, key="chart12", config={'displayModeBar': False})
    
    with col2:
        st.markdown("#### 🚚 Shipping Type Distribution")
        shipping_counts = filtered_df["Shipping Type"].value_counts()
        fig13 = px.bar(
            x=shipping_counts.index,
            y=shipping_counts.values,
            labels={'x': 'Shipping Type', 'y': 'Count'},
            color=shipping_counts.values,
            color_continuous_scale='Magma'
        )
        fig13.update_layout(
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            transition={'duration': 800, 'easing': 'cubic-in-out'}
        )
        fig13.update_traces(
            marker=dict(line=dict(color='rgba(0, 245, 255, 0.3)', width=1)),
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
        st.plotly_chart(fig13, use_container_width=True, key="chart13", config={'displayModeBar': False})

# ---------------- DATA PREVIEW ----------------
st.markdown("---")
st.markdown("### 📄 Filtered Dataset Preview")
with st.expander("Click to view detailed data table"):
    st.dataframe(
        filtered_df.style.background_gradient(cmap='Purples', subset=['Purchase Amount (USD)']),
        use_container_width=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_customer_data.csv',
        mime='text/csv',
    )

# ---------------- FOOTER ----------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; background: linear-gradient(135deg, rgba(10, 14, 39, 0.8) 0%, rgba(20, 24, 49, 0.8) 100%); backdrop-filter: blur(20px); padding: 2.5rem; border-radius: 20px; margin-top: 2rem; border: 1px solid rgba(0, 245, 255, 0.3); box-shadow: 0 0 40px rgba(0, 245, 255, 0.2);'>
        <div style='margin-bottom: 1.5rem;'>
            <h3 style='color: #00f5ff; margin-bottom: 0.5rem; font-size: 1.8rem; text-transform: uppercase; letter-spacing: 3px; text-shadow: 0 0 20px rgba(0, 245, 255, 0.6);'>DATA ANALYTICS</h3>
            <p style='color: rgba(255, 255, 255, 0.6); font-size: 0.85rem; font-family: "JetBrains Mono", monospace; text-transform: uppercase; letter-spacing: 2px;'>Customer Intelligence Platform</p>
        </div>
        <div style='padding: 1rem; background: rgba(0, 245, 255, 0.05); border-radius: 10px; margin-bottom: 1rem; border: 1px solid rgba(0, 245, 255, 0.2);'>
            <p style='color: rgba(255, 255, 255, 0.9); font-size: 0.95rem; margin: 0;'>
                Built with 💙 using <span style='color: #00f5ff; font-weight: 600;'>Streamlit</span> & <span style='color: #00f5ff; font-weight: 600;'>Plotly</span>
            </p>
        </div>
        <div style='display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;'>
            <div style='padding: 0.8rem 1.5rem; background: rgba(102, 126, 234, 0.2); border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.3);'>
                <span style='color: #00f5ff; font-size: 0.8rem; font-family: "JetBrains Mono", monospace;'>🚀 REAL-TIME PROCESSING</span>
            </div>
            <div style='padding: 0.8rem 1.5rem; background: rgba(102, 126, 234, 0.2); border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.3);'>
                <span style='color: #00f5ff; font-size: 0.8rem; font-family: "JetBrains Mono", monospace;'>⚡ INSTANT INSIGHTS</span>
            </div>
            <div style='padding: 0.8rem 1.5rem; background: rgba(102, 126, 234, 0.2); border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.3);'>
                <span style='color: #00f5ff; font-size: 0.8rem; font-family: "JetBrains Mono", monospace;'>🧠 ML-READY</span>
            </div>
        </div>
        <div style='margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(0, 245, 255, 0.2);'>
            <p style='color: rgba(255, 255, 255, 0.5); font-size: 0.75rem; font-family: "JetBrains Mono", monospace;'>
                © 2026 CUSTOMER ANALYTICS | VERSION 2.0.1 | ALL SYSTEMS OPERATIONAL
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)
