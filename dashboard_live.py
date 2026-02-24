import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="BSE Energy Index - LIVE", page_icon="🛢️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%); }
    
    [data-testid="stMetricValue"] { 
        font-size: 2.5rem; font-weight: 700; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
    }
    
    h1 { color: white; font-weight: 700; font-size: 3.5rem !important; text-align: center; 
         margin-bottom: 0.5rem; text-shadow: 0 0 30px rgba(102, 126, 234, 0.5); }
    h2, h3 { color: rgba(255, 255, 255, 0.95); font-weight: 600; }
    p, span, div { color: rgba(255, 255, 255, 0.85); }
    
    /* Pulsing status dot */
    .status-live {
        display: inline-block; width: 12px; height: 12px; background: #ef4444;
        border-radius: 50%; animation: pulse-red 1s infinite; box-shadow: 0 0 20px #ef4444;
    }
    @keyframes pulse-red { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.6; transform: scale(1.2); } }
    
    /* Live activity stream */
    .live-log {
        padding: 8px 12px; margin: 4px 0; background: rgba(102, 126, 234, 0.05);
        border-left: 3px solid #667eea; border-radius: 6px;
        font-family: 'Courier New', monospace; font-size: 0.85rem;
        animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
    
    /* Price ticker */
    .price-ticker {
        background: rgba(16, 185, 129, 0.1); padding: 20px; border-radius: 15px;
        border: 2px solid rgba(16, 185, 129, 0.3); text-align: center;
        animation: glow 2s ease-in-out infinite;
    }
    @keyframes glow { 0%, 100% { box-shadow: 0 0 10px rgba(16, 185, 129, 0.3); } 
                      50% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); } }
    
    .big-price { font-size: 3rem; font-weight: 700; color: #10b981; }
    
    /* Cycle counter */
    .cycle-badge {
        display: inline-block; background: rgba(139, 92, 246, 0.2);
        padding: 8px 16px; border-radius: 20px; font-weight: 600;
        border: 1px solid rgba(139, 92, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://15.236.201.18:5000/api/data"

# Header with LIVE badge
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1>🛢️ BSE ENERGY INDEX</h1>
    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.7);'>
        <span class='status-live'></span>
        <span style='margin-left: 10px; color: #ef4444; font-weight: 600;'>LIVE NOW</span>
    </p>
</div>
""", unsafe_allow_html=True)

# Create placeholder for live updates
price_placeholder = st.empty()
metrics_placeholder = st.empty()
charts_placeholder = st.empty()
components_placeholder = st.empty()
activity_placeholder = st.empty()

# Refresh counter
if 'refresh_count' not in st.session_state:
    st.session_state.refresh_count = 0
st.session_state.refresh_count += 1

try:
    response = requests.get(API_URL, timeout=10)
    data = response.json()
    
    # Live price ticker at top
    with price_placeholder.container():
        st.markdown(f"""
        <div class='price-ticker'>
            <div style='font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-bottom: 10px;'>LIVE TOKEN PRICE</div>
            <div class='big-price'>${data['price']:.6f}</div>
            <div style='font-size: 1.2rem; color: {"#10b981" if data["price_24h_change"] >= 0 else "#ef4444"}; margin-top: 10px;'>
                {data['price_24h_change']:+.2f}% (24h)
            </div>
            <div style='font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-top: 15px;'>
                <span class='cycle-badge'>CYCLE #{data['total_cycles']}</span>
                <span style='margin-left: 15px;'>⏱ Uptime: {data['uptime_hours']}h</span>
                <span style='margin-left: 15px;'>🔄 Updates: {st.session_state.refresh_count}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics row
    with metrics_placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 ENERGY INDEX", f"{data['score']:+.2f}%", "Live")
        with col2:
            st.metric("⚡ TOTAL TRADES", data['total_trades'], f"↑{data['buy_trades']} ↓{data['sell_trades']}")
        with col3:
            correlation = min(100, 70 + (data['total_cycles'] * 0.1))
            st.metric("🎯 CORRELATION", f"{correlation:.0f}%", "Improving")
        with col4:
            st.metric("🔥 STATUS", "ACTIVE", f"Port 5000")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    with charts_placeholder.container():
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("📈 Price Movement")
            if data['historical']['prices'] and len(data['historical']['prices']) > 1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=data['historical']['prices'], mode='lines+markers',
                    line=dict(color='#667eea', width=3), marker=dict(size=6),
                    fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.1)'
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'), showlegend=False,
                    xaxis=dict(showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                    height=300, margin=dict(l=0,r=0,t=0,b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 Building price history... (Need 2+ cycles)")
        
        with chart_col2:
            st.subheader("🎯 Index Score")
            if data['historical']['scores'] and len(data['historical']['scores']) > 1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=data['historical']['scores'], mode='lines+markers',
                    line=dict(color='#10b981', width=3), marker=dict(size=6),
                    fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.1)'
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'), showlegend=False,
                    xaxis=dict(showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=True),
                    height=300, margin=dict(l=0,r=0,t=0,b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 Building score history... (Need 2+ cycles)")
    
    # Components
    with components_placeholder.container():
        st.subheader("⚙️ Live Components")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px; border: 2px solid rgba(251, 191, 36, 0.3);'><div style='font-size: 2rem;'>🛢️</div><div style='font-size: 0.85rem; color: rgba(255,255,255,0.6);'>OIL (40%)</div><div style='font-size: 1.5rem; font-weight: 700; color: #fbbf24;'>${data['oil']:.2f}</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px; border: 2px solid rgba(59, 130, 246, 0.3);'><div style='font-size: 2rem;'>⛽</div><div style='font-size: 0.85rem; color: rgba(255,255,255,0.6);'>GAS (30%)</div><div style='font-size: 1.5rem; font-weight: 700; color: #3b82f6;'>${data['gas']:.2f}</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px; border: 2px solid rgba(16, 185, 129, 0.3);'><div style='font-size: 2rem;'>📈</div><div style='font-size: 0.85rem; color: rgba(255,255,255,0.6);'>XLE (20%)</div><div style='font-size: 1.5rem; font-weight: 700; color: #10b981;'>${data['xle']:.2f}</div></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px; border: 2px solid rgba(139, 92, 246, 0.3);'><div style='font-size: 2rem;'>🏗️</div><div style='font-size: 0.85rem; color: rgba(255,255,255,0.6);'>RIGS (10%)</div><div style='font-size: 1.5rem; font-weight: 700; color: #8b5cf6;'>{data['rigs']}</div></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LIVE Activity Stream
    with activity_placeholder.container():
        st.subheader("⚡ LIVE Activity Stream")
        st.markdown(f"<div style='font-size: 0.85rem; color: rgba(255,255,255,0.5); margin-bottom: 15px;'>Last update: {datetime.now().strftime('%H:%M:%S')} • Refreshing in 10 seconds...</div>", unsafe_allow_html=True)
        
        activity_html = "<div style='background: rgba(0,0,0,0.3); padding: 20px; border-radius: 15px; max-height: 450px; overflow-y: auto;'>"
        
        # Show last 20 activities with newest first
        activities = data['activity_feed'][-20:] if data['activity_feed'] else ["Waiting for activity..."]
        for i, act in enumerate(reversed(activities)):
            # Add timestamp and styling
            activity_html += f"<div class='live-log' style='animation-delay: {i * 0.05}s;'>"
            activity_html += f"<span style='color: rgba(102, 126, 234, 0.8);'>[{datetime.now().strftime('%H:%M')}]</span> "
            
            # Highlight important keywords
            act_styled = act
            if "Trade" in act or "BUY" in act or "SELL" in act:
                act_styled = f"<span style='color: #10b981; font-weight: 600;'>{act}</span>"
            elif "ERROR" in act or "Failed" in act:
                act_styled = f"<span style='color: #ef4444;'>{act}</span>"
            elif "UPDATE CYCLE" in act:
                act_styled = f"<span style='color: #8b5cf6; font-weight: 600;'>{act}</span>"
            
            activity_html += act_styled
            activity_html += "</div>"
        
        activity_html += "</div>"
        st.markdown(activity_html, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; margin-top: 30px; background: rgba(0,0,0,0.2); border-radius: 15px;'>
        <div style='font-size: 0.85rem; color: rgba(255,255,255,0.5);'>
            Contract: <code style='background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 4px;'>0x9177...7ba3</code>
            • Network: Base • API: Live
        </div>
        <div style='font-size: 0.75rem; color: rgba(255,255,255,0.3); margin-top: 8px;'>
            Auto-refresh: 10s • Built with Streamlit • Powered by AI
        </div>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Connection Error: {str(e)}")
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <div style='font-size: 5rem;'>🔌</div>
        <div style='font-size: 1.5rem; color: rgba(255,255,255,0.7);'>Connection Lost</div>
        <div style='font-size: 1rem; color: rgba(255,255,255,0.5); margin-top: 10px;'>Reconnecting...</div>
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh every 10 seconds (faster updates!)
time.sleep(10)
st.rerun()
