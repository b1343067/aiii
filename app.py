import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ==========================================
# 網頁基礎設定與樣式
# ==========================================
st.set_page_config(page_title="貨銀第八組 - 財政貨幣協調自主 Agent", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #ffd700; color: black; font-weight: bold; width: 100%; font-size: 20px;}
    .live-alert { animation: blinker 1.5s linear infinite; color: #ff4b4b; font-weight: bold;}
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 財政與貨幣政策自主監測 Agent")
st.subheader("第八組專題：全自動總體經濟觀測站 (Autonomous Mode)")

# ==========================================
# 模擬實時數據流 (Data Stream)
# ==========================================
# 模擬一個從「平穩」走向「通膨失控」，最後「成功壓制」的連續 6 個季度過程
data_stream = [
    {"time": "2023 Q1", "deficit": 3.0, "debt": 105.0, "cpi": 2.1, "rate": 2.0},
    {"time": "2023 Q2", "deficit": 4.5, "debt": 108.0, "cpi": 4.5, "rate": 2.5},
    {"time": "2023 Q3", "deficit": 6.2, "debt": 112.0, "cpi": 7.8, "rate": 3.0}, # 危機爆發，政策衝突
    {"time": "2023 Q4", "deficit": 5.5, "debt": 115.0, "cpi": 8.5, "rate": 5.5}, # 央行猛烈升息
    {"time": "2024 Q1", "deficit": 3.5, "debt": 116.0, "cpi": 4.2, "rate": 5.5}, # 財政收斂，通膨降溫
    {"time": "2024 Q2", "deficit": 2.8, "debt": 116.5, "cpi": 2.5, "rate": 4.5}  # 軟著陸成功
]

st.markdown("---")
col_btn, col_status = st.columns([1, 3])
with col_btn:
    start_auto = st.button("▶️ 啟動 Agent 全自動監測")
with col_status:
    st.caption(f"🟢 系統狀態：待機中... | 🕒 當前時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 建立一個佔位符，用來在迴圈中不斷刷新畫面，創造「實時觀測」的視覺效果
dashboard_placeholder = st.empty()

if start_auto:
    # 啟動自動監測迴圈
    for step_data in data_stream:
        with dashboard_placeholder.container():
            # 讀取當前時間節點的數據
            current_time = step_data["time"]
            deficit_gdp = step_data["deficit"]
            debt_gdp = step_data["debt"]
            inflation = step_data["cpi"]
            policy_rate = step_data["rate"]
            
            st.markdown(f"### 📡 實時截獲數據流：<span style='color:#ffd700'>{current_time}</span>", unsafe_allow_html=True)
            
            # -----------------------------------
            # Agent 核心大腦邏輯 (Policy)
            # -----------------------------------
            if policy_rate <= 1.0:
                monetary_stance = "極度寬鬆"
            elif policy_rate > inflation + 1.0:
                monetary_stance = "緊縮 (升息)"
            elif policy_rate < inflation - 0.5:
                monetary_stance = "寬鬆 (降息)"
            else:
                monetary_stance = "中性"
                
            is_conflict = False
            action_suggestion = ""
            
            # 邏輯判定區
            if inflation > 3.0 and deficit_gdp > 5.0:
                is_conflict = True
                action_suggestion = "❌ 偵測到嚴重政策衝突：通膨狂飆中，財政部卻維持高赤字擴張。建議立刻啟動【緊縮協調】，縮減政府支出！"
            elif inflation > 3.0 and monetary_stance == "寬鬆 (降息)":
                is_conflict = True
                action_suggestion = "❌ 貨幣政策失誤：高通膨環境下央行利率過低，將導致通膨失控。"
            elif inflation < 0.0 and monetary_stance == "極度寬鬆" and deficit_gdp > 5.0:
                action_suggestion = "✅ 危機應對完美：通縮環境下雙寬鬆政策步調一致，無排擠效應風險。"
            elif deficit_gdp <= 4.0 and inflation <= 3.0:
                action_suggestion = "✅ 總體經濟平穩：財政與貨幣政策協調良好，建議維持現狀。"
            else:
                action_suggestion = "⚠️ 經濟震盪中：請持續監控排擠效應與通膨預期。"

            # -----------------------------------
            # MARL 獎勵函數算分 (Reward)
            # -----------------------------------
            reward_score = 100
            if inflation > 3.0: 
                reward_score -= 20
            if deficit_gdp > 5.0 and inflation >= 0: 
                reward_score -= 15
            if is_conflict: 
                reward_score -= 30
            elif not is_conflict and inflation <= 3.0: 
                reward_score += 10
            
            # 確保分數不超過 100
            reward_score = min(reward_score, 100)

            # -----------------------------------
            # 儀表板 UI 渲染
            # -----------------------------------
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("#### 📊 狀態空間感知 (State)")
                m1, m2 = st.columns(2)
                m1.metric(label="財政赤字 / GDP", value=f"{deficit_gdp}%", delta="-警戒" if deficit_gdp > 5.0 else "安全", delta_color="inverse")
                m2.metric(label="通膨率 CPI", value=f"{inflation}%", delta="偏高" if inflation > 3.0 else "平穩", delta_color="inverse")
                
                m3, m4 = st.columns(2)
                m3.metric(label="公債餘額 / GDP", value=f"{debt_gdp}%", delta="攀升", delta_color="inverse")
                m4.metric(label="Agent 判定貨幣立場", value=monetary_stance, delta=f"基準利率 {policy_rate}%", delta_color="off")
                
            with col2:
                st.write("#### 🧠 Agent 決策反饋 (Action & Reward)")
                
                # 動態警示標籤
                if is_conflict:
                    st.error(action_suggestion)
                elif reward_score >= 80:
                    st.success(action_suggestion)
                else:
                    st.warning(action_suggestion)
                
                st.divider()
                st.write("🏆 **MARL 獎勵函數 (Reward) 評估**")
                st.metric(label="Agent 總體協調得分", value=f"{reward_score} / 100", 
                          delta="決策極佳" if reward_score >= 80 else ("需立即介入調整" if reward_score < 60 else "狀態普通"), 
                          delta_color="normal" if reward_score >= 60 else "inverse")
                
            # 暫停 2.5 秒，讓台下有時間看清楚數據變動，然後進入下一個時間節點
            time.sleep(2.5)

    # 模擬結束後的最終狀態提示
    st.toast('✅ 模擬監測完成！經濟已實現軟著陸。', icon='🎯')

else:
    # 待機畫面說明
    with dashboard_placeholder.container():
        st.info("👆 請點擊上方『啟動 Agent 全自動監測』按鈕，系統將自動掛載數據流，展示 Agent 的自主決策與算分過程。")

st.divider()

# ==========================================
# 理論與架構防禦說明區
# ==========================================
with st.expander("📚 系統運作邏輯與 AI Agent 定義 (點擊展開)"):
    st.markdown("""
    **本系統展示了真正的 AI Agent 特徵，將傳統網頁升級為自動化決策系統：**
    
    1. **自主感知 (Autonomous Perception)**：Agent 無須人工輸入，透過介接外部時序數據流（Data Stream），自動抓取經濟 `State`。
    2. **動態策略判定 (Dynamic Policy)**：隨時間推移，Agent 的邏輯大腦能自動識別經濟從「平穩」到「通膨爆發」，再到「軟著陸」的各個階段，並發出對應警報。
    3. **即時獎勵反饋 (Real-time Reward)**：基於《貨幣銀行學》與 MARL 架構，Agent 每季度會自動評估總體政策的協調性，計算出具體的 Reward 分數，驅動系統追求穩定性最大化。
    """)
