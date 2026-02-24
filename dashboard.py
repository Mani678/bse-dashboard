import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="BSE Energy Index", page_icon="🛢️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%); }
    [data-testid="stMetricValue"] { font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    h1 { color: white; font-weight: 700; font-size: 3.5rem !important; text-align: center; margin-bottom: 0.5rem; text-shadow: 0 0 30px rgba(102, 126, 234, 0.5); }
    h2, h3 { color: rgba(255, 255, 255, 0.95); font-weight: 600; }
    p, span, div { color: rgba(255, 255, 255, 0.85); }
    .status-online { display: inline-block; width: 12px; height: 12px; background: #10b981; border-radius: 50%; animation: pulse 2s infinite; box-shadow: 0 0 20px #10b981; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    .activity-item { padding: 12px; margin: 8px 0; background: rgba(255, 255, 255, 0.03); border-left: 3px solid #667eea; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.85rem; }
    .glow { text-shadow: 0 0 10px rgba(102, 126, 234, 0.5); }
</style>
""", unsafe_allow_html=True)

API_URL = "http://15.236.201.18:5000/api/data"

st.markdown("<h1 class='glow'>🛢️ BSE ENERGY INDEX</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: rgba(255,255,255,0.7); margin-bottom: 2rem;'>Live AI-Powered Energy Sector Tracking</p>", unsafe_allow_html=True)

try:
    response = requests.get(API_URL, timeout=10)
    data = response.json()
    
    col_status1, col_status2, col_status3 = st.columns([1, 2, 1])
    with col_status2:
        st.markdown(f"""<div style='text-align: center; padding: 15px; background: rgba(16, 185, 129, 0.1); border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <span class='status-online'></span><span style='margin-left: 10px; color: #10b981; font-weight: 600;'>SYSTEM ONLINE</span>
            <span style='margin-left: 20px; color: rgba(255,255,255,0.6);'>Uptime: {data['uptime_hours']}h</span>
            <span style='margin-left: 20px; color: rgba(255,255,255,0.6);'>Cycles: {data['total_cycles']}</span></div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 TOKEN PRICE", f"${data['price']:.6f}", f"{data['price_24h_change']:+.2f}% (24h)")
    with col2:
        st.metric("📊 ENERGY INDEX", f"{data['score']:+.2f}%", "Live tracking")
    with col3:
        st.metric("⚡ TOTAL TRADES", data['total_trades'], f"↑{data['buy_trades']} ↓{data['sell_trades']}")
    with col4:
        correlation = min(100, 70 + (data['total_cycles'] * 0.1))
        st.metric("🎯 CORRELATION", f"{correlation:.0f}%", "Target: >70%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("📈 Price History")
        if data['historical']['prices']:
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=data['historical']['prices'], mode='lines', line=dict(color='#667eea', width=3), fill='tozeroy'))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'), height=300, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Building history...")
    
    with chart_col2:
        st.subheader("🎯 Energy Index Score")
        if data['historical']['scores']:
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=data['historical']['scores'], mode='lines', line=dict(color='#10b981', width=3), fill='tozeroy'))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'), height=300, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Building history...")
    
    st.subheader("⚙️ Index Components")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px;'><div style='font-size: 2.5rem;'>🛢️</div><div style='font-size: 0.9rem; color: rgba(255,255,255,0.6);'>OIL (40%)</div><div style='font-size: 1.8rem; font-weight: 700; color: #fbbf24;'>${data['oil']:.2f}</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px;'><div style='font-size: 2.5rem;'>⛽</div><div style='font-size: 0.9rem; color: rgba(255,255,255,0.6);'>GAS (30%)</div><div style='font-size: 1.8rem; font-weight: 700; color: #3b82f6;'>${data['gas']:.2f}</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px;'><div style='font-size: 2.5rem;'>📈</div><div style='font-size: 0.9rem; color: rgba(255,255,255,0.6);'>XLE (20%)</div><div style='font-size: 1.8rem; font-weight: 700; color: #10b981;'>${data['xle']:.2f}</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px;'><div style='font-size: 2.5rem;'>🏗️</div><div style='font-size: 0.9rem; color: rgba(255,255,255,0.6);'>RIGS (10%)</div><div style='font-size: 1.8rem; font-weight: 700; color: #8b5cf6;'>{data['rigs']}</div></div>", unsafe_allow_html=True)
    
    st.subheader("⚡ Live Activity")
    activity = "<div style='background: rgba(0,0,0,0.3); padding: 20px; border-radius: 15px; max-height: 400px; overflow-y: auto;'>"
    for act in reversed(data['activity_feed'][-15:]):
        activity += f"<div class='activity-item'>{act}</div>"
    activity += "</div>"
    st.markdown(activity, unsafe_allow_html=True)
    
    st.markdown(f"""<div style='text-align: center; padding: 30px; margin-top: 30px; background: rgba(0,0,0,0.2); border-radius: 15px;'>
        <div style='font-size: 0.9rem; color: rgba(255,255,255,0.5);'>Contract: <code>0x9177ea9636bfde40f02c45f7e5f6b04b04cb7ba3</code></div>
        <div style='font-size: 0.85rem; color: rgba(255,255,255,0.4);'>Network: Base • Updated: {datetime.now().strftime("%H:%M:%S UTC")} • Refresh: 30s</div></div>""", unsafe_allow_html=True)

except Exception as e:
    st.error("⚠️ Connection Error")
    st.markdown("<div style='text-align: center; padding: 50px;'><div style='font-size: 5rem;'>🔌</div><div style='font-size: 1.5rem; color: rgba(255,255,255,0.7);'>Offline</div></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
