import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ==========================================
# 網頁基礎設定與樣式
# ==========================================
st.set_page_config(page_title="貨銀第八組 - 財政貨幣協調 AI Agent", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #ffd700; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 財政與貨幣政策協調 AI Agent")
st.subheader("第八組專題：總體政策模擬決策系統")

# ==========================================
# 側邊欄：一鍵載入歷史經典情境與數據輸入
# ==========================================
with st.sidebar:
    st.header("📂 情境資料庫")
    # 專業版命名，無贅字
    scenario = st.selectbox("快速載入歷史情境", [
        "2026年6月 最新總經現況", 
        "自訂輸入 (當前現況)", 
        "2022 疫情後大通膨", 
        "2008 金融海嘯"
    ])
    
    # 根據選擇載入對應數據
    if scenario == "2026年6月 最新總經現況":
        # 2026 最新真實數據：Fed 點陣圖 + CBO 財政展望
        def_val, debt_val, cpi_val, rate_val = 6.0, 105.0, 2.4, 3.5
    elif scenario == "2022 疫情後大通膨":
        def_val, debt_val, cpi_val, rate_val = 12.3, 120.0, 9.1, 2.5
    elif scenario == "2008 金融海嘯":
        def_val, debt_val, cpi_val, rate_val = 9.8, 67.0, -0.4, 0.25
    else:
        def_val, debt_val, cpi_val, rate_val = 6.0, 123.0, 2.1, 5.5

    st.markdown("---")
    st.header("📊 經濟數據觀測站")
    
    deficit_gdp = st.slider("財政赤字 / GDP (%)", min_value=0.0, max_value=20.0, value=float(def_val), step=0.1)
    debt_gdp = st.slider("公債餘額 / GDP (%)", min_value=0.0, max_value=150.0, value=float(debt_val), step=0.1)
    inflation = st.slider("通膨率 CPI (%)", min_value=-5.0, max_value=15.0, value=float(cpi_val), step=0.1)
    policy_rate = st.slider("政策基準利率 (%)", min_value=0.0, max_value=10.0, value=float(rate_val), step=0.1)
    
    analyze_btn = st.button("啟動 AI 決策演算法")
    
    st.markdown("---")
    st.caption(f"🕒 系統最後同步時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ==========================================
# 核心邏輯：AI 自動判斷貨幣政策立場 (實質利率)
# ==========================================
if policy_rate <= 1.0:
    monetary_stance = "極度寬鬆"
    rate_desc = f"零利率/QE ({policy_rate}%)" 
elif policy_rate > inflation + 1.0:
    monetary_stance = "緊縮 (升息)"
    rate_desc = f"基準利率 {policy_rate}%"
elif policy_rate < inflation - 0.5:
    monetary_stance = "寬鬆 (降息)"
    rate_desc = f"基準利率 {policy_rate}%"
else:
    monetary_stance = "中立"
    rate_desc = f"基準利率 {policy_rate}%"

# ==========================================
# 主畫面內容：狀態空間看板 (State)
# ==========================================
col1, col2 = st.columns([1, 1])

with col1:
    st.write("## 🏦") 
    st.write("### 狀態空間 (State) 看板")
    m1, m2 = st.columns(2)
    m1.metric(label="財政赤字 / GDP", value=f"{deficit_gdp}%", delta="-警戒" if deficit_gdp > 5.0 else "安全", delta_color="inverse")
    m2.metric(label="公債餘額 / GDP", value=f"{debt_gdp}%", delta="持續攀升", delta_color="inverse")
    
    st.caption("公債壓力指數")
    progress_val = min(debt_gdp / 150.0, 1.0) 
    st.progress(progress_val)
    
    m3, m4 = st.columns(2)
    cpi_status = "偏高" if inflation > 2.0 else ("通縮警戒" if inflation < 0 else "達標")
    m3.metric(label="通膨率 CPI", value=f"{inflation}%", delta=cpi_status, delta_color="inverse")
    m4.metric(label="自動判定貨幣立場", value=monetary_stance, delta=rate_desc, delta_color="off")

with col2:
    st.write("### AI 決策網路 (Policy)")
    if inflation < 0.0:
        st.error("❄️ 觀測狀態：嚴重通縮與衰退風險，建議『全面寬鬆與擴張刺激』")
    elif inflation > 3.0:
        st.warning("⚠️ 觀測狀態：通膨偏高，系統優先尋求『緊縮協調』以穩定物價")
    elif deficit_gdp > 5.0:
        st.warning("🚨 觀測狀態：財政赤字偏高，啟動『排擠效應』風險預警")
    else:
        st.success("✅ 觀測狀態：總體經濟指標穩定")

st.divider()

# ==========================================
# AI 輸出區 (Action & Reward)
# ==========================================
if analyze_btn:
    with st.spinner('🤖 AI Agent 正在進行政策模擬與協調性運算...'):
        time.sleep(1.5) 
    st.toast('決策分析完成！', icon='✅')
    
    st.write("## 🎯 AI Agent 決策報告 (Action)")
    
    tab1, tab2 = st.tabs(["🎯 政策協調與調整建議", "📈 資本市場影響 (股市/債市)"])
    
    is_conflict = False
    
    # [Tab 1] 政策協調性分析 + 調整建議
    with tab1:
        st.markdown("### 1. 政策協調性評估")
        
        if inflation < 0.0 and monetary_stance == "極度寬鬆" and deficit_gdp > 5.0:
            st.success("✅ **非常規政策協調 (危機應對)**：系統偵測到通縮與衰退危機，央行已啟動極度寬鬆救市。此時政府擴大財政支出是必要手段，雙寬鬆政策完美協調。")
        elif inflation > 3.0 and deficit_gdp > 5.0:
            st.error("❌ **政策衝突 (不協調)**：系統偵測到通膨依然高於目標，但政府卻維持高赤字 (大撒幣)。擴張性財政政策將抵銷抗通膨的努力！建議政府必須縮減支出，配合央行步調。")
            is_conflict = True
        elif inflation <= 3.0 and deficit_gdp > 5.0 and ("緊縮" in monetary_stance):
            st.warning("⚠️ **財政拖累風險**：通膨已逐漸受控，央行維持高利率，但政府赤字依然過高。這將導致市場利率居高不下，引發長期排擠效應。")
        elif inflation > 2.0 and ("寬鬆" in monetary_stance):
            st.error("❌ **嚴重不協調**：目前通膨偏高，但貨幣政策卻放水，等於提油救火，將導致通膨失控。")
            is_conflict = True
        elif inflation < 0.0 and ("緊縮" in monetary_stance):
            st.error("❌ **經濟衰退危機**：已出現通縮現象，央行卻持續緊縮，將引發嚴重經濟衰退。")
            is_conflict = True
        elif inflation < 2.0 and deficit_gdp < 3.0 and monetary_stance == "緊縮 (升息)":
            st.warning("⚠️ **過度緊縮風險**：通膨已偏低且財政保守，若央行仍持續升息，恐壓抑經濟動能。")
        else:
            st.success("✅ **目前政策尚屬協調**：貨幣與財政步調相對一致，有助於維持總體經濟穩定。")
            
        st.divider()
        
        st.markdown("### 2. 排擠效應與調整建議")
        if inflation < 0.0:
            st.write("由於目前處於通縮與流動性陷阱邊緣，民間投資意願低落。此時政府擴大支出**不會產生排擠效應**。👉 **建議財政部持續發力刺激需求**。")
        else:
            st.write("若政府在此刻擴大財政刺激，預計會導致市場利率居高不下，進而產生**排擠效應 (Crowding-out Effect)**。👉 **強烈建議政府縮減赤字，防止債務負擔加劇並讓渡資金給民間投資**。")
        
    # [Tab 2] 資本市場分析
    with tab2:
        st.markdown("### 資本市場風向預測")
        if inflation > 3.0 or "緊縮" in monetary_stance:
            st.error("📉 **股市預警**：通膨與高利率環境將大幅提升企業資金成本。對於大型科技股的估值將面臨下修壓力。建議關注大盤指數 ETF (如 VOO) 分散風險，並轉向防禦性板塊。")
            st.success("📈 **債市預測**：由於處於高息環境，債券殖利率將維持高檔，短天期公債 (如 TLT/SHY) 具備防禦性吸引力。")
        elif "寬鬆" in monetary_stance:
            st.success("📈 **股市利多**：資金成本降低將有效挹注市場流動性。大盤指數 ETF 有望受惠於資金行情，科技巨頭預期將迎來強勁反彈。")
            st.error("📉 **債市預測**：降息預期將帶動既有債券價格上漲，但新發行債券的殖利率將下滑。")
        else:
            st.info("⚖️ **市場觀望**：目前政策偏向中立，市場將回歸基本面檢視，大盤預期呈現區間震盪，建議維持既有步調與定期定額策略。")
        
    st.divider()
    
    # ==========================================
    # 神級優化：MARL 系統獎勵函數 (Reward) 算分機制
    # ==========================================
    reward_score = 100 
    score_reasons = []

    # 1. 總體環境狀態評估 (State)
    if inflation > 3.0:
        reward_score -= 20
        score_reasons.append("高通膨環境 (-20)")
    elif inflation < 0:
        reward_score -= 30
        score_reasons.append("通縮衰退環境 (-30)")

    # 2. 財政健康度評估 (排除通縮救市時的高赤字特例)
    if deficit_gdp > 5.0 and inflation >= 0:
        reward_score -= 15
        score_reasons.append("排擠效應風險 (-15)")

    # 3. 政策協調度評估 (Action)
    if is_conflict:
        reward_score -= 30
        score_reasons.append("政策衝突懲罰 (-30)")
    elif inflation < 0.0 and monetary_stance == "極度寬鬆" and deficit_gdp > 5.0:
        reward_score += 15 
        score_reasons.append("危機完美救市獎勵 (+15)")
    else:
        score_reasons.append("政策維持協調 (+0)")

    reward_score = min(reward_score, 100)

    st.markdown("#### 🏆 MARL 系統獎勵函數 (Reward) 評估")
    st.write("Agent 在多智能體強化學習中，透過最大化總體經濟的穩定性來獲取最高 Reward。")
    
    st.metric(label="Agent 當前決策網路總得分", value=f"{reward_score} / 100", 
              delta="決策極佳" if reward_score >= 85 else ("需調整政策" if reward_score < 70 else "狀態普通"), 
              delta_color="normal" if reward_score >= 70 else "inverse")
    
    st.caption(f"🧠 **模型算分依據**：基礎分數 100 分。本次結算包含：{', '.join(score_reasons)}。")

else:
    st.info("👈 請於左側設定觀測指標，並點擊『啟動 AI 決策演算法』")

# ==========================================
# 理論補充區
# ==========================================
with st.expander("📚 系統核心理論與 MARL 架構對照 (點擊展開)"):
    st.markdown("""
    **本系統基於《貨幣銀行學》理論與 MARL 架構開發：**
    * **Agent (智能體)**：G8 財政貨幣協調決策系統。
    * **State (狀態)**：左側輸入之赤字率、債務比、通膨率與利率。
    * **Policy (策略)**：透過實質利率判定貨幣立場，並比對赤字水位判斷是否發生衝突。
    * **Reward (獎勵)**：將通膨、赤字與政策協調度量化為具體分數，驅使 Agent 追求經濟穩定。
    """)
