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
st.subheader("第八組專題：總體政策模擬與未來推演系統")

# ==========================================
# 側邊欄：一鍵載入歷史經典情境與數據輸入
# ==========================================
with st.sidebar:
    st.header("📂 情境資料庫")
    scenario = st.selectbox("快速載入歷史情境", [
        "最新總經現況", 
        "自訂輸入 (當前現況)", 
        "2022 疫情後大通膨", 
        "2008 金融海嘯"
    ])
    
    # 根據選擇載入對應數據 (已更新為指定數據)
    if scenario == "最新總經現況":
        def_val, debt_val, cpi_val, rate_val = 6.0, 123.0, 3.8, 3.5
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
    
    analyze_btn = st.button("啟動 AI 決策與未來預測")
    
    st.markdown("---")
    st.caption(f"🕒 系統最後同步時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ==========================================
# 核心邏輯：AI 自動判斷貨幣政策立場
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
# AI 輸出區 (Action, Forecast & Reward)
# ==========================================
if analyze_btn:
    with st.spinner('🤖 AI Agent 正在建立時間序列預測模型...'):
        time.sleep(1.5) 
    st.toast('動態推演完成！', icon='✅')
    
    st.write("## 🎯 AI Agent 預測與決策報告 (Action & Forecast)")
    
    tab1, tab2, tab3 = st.tabs(["🎯 當前政策協調評估", "📈 資本市場影響 (股市/債市)", "🔮 未來三個季度推演"])
    
    is_conflict = False
    
    # [Tab 1] 當前政策協調性分析
    with tab1:
        st.markdown("### 1. 政策協調性評估")
        if inflation < 0.0 and monetary_stance == "極度寬鬆" and deficit_gdp > 5.0:
            st.success("✅ **非常規政策協調 (危機應對)**：系統偵測到通縮與衰退危機，央行啟動極度寬鬆救市。此時擴大財政支出是必要手段，雙寬鬆政策完美協調。")
        elif inflation > 3.0 and deficit_gdp > 5.0:
            st.error("❌ **政策衝突 (不協調)**：通膨高於目標，政府卻維持大撒幣。擴張性財政政策將抵銷抗通膨努力！建議必須縮減支出。")
            is_conflict = True
        elif inflation > 2.0 and ("寬鬆" in monetary_stance):
            st.error("❌ **嚴重不協調**：通膨偏高貨幣卻放水，將導致通膨失控。")
            is_conflict = True
        elif inflation < 0.0 and ("緊縮" in monetary_stance):
            st.error("❌ **經濟衰退危機**：通縮現象下央行持續緊縮，將引發嚴重衰退。")
            is_conflict = True
        elif inflation <= 3.0 and deficit_gdp > 5.0:
            st.warning("⚠️ **財政拖累風險**：通膨已降溫，但政府赤字過高，長期將引發排擠效應。")
        else:
            st.success("✅ **目前政策尚屬協調**：貨幣與財政步調相對一致。")
        
    # [Tab 2] 資本市場分析
    with tab2:
        st.markdown("### 資本市場風向預測")
        if inflation > 3.0 or "緊縮" in monetary_stance:
            st.error("📉 **股市預警**：高息環境將提升企業資金成本，大型科技股估值面臨下修壓力。建議關注防禦性大盤 ETF (如 VOO)。")
            st.success("📈 **債市預測**：債券殖利率維持高檔，短天期公債 (如 SHY) 具防禦性吸引力。")
        elif "寬鬆" in monetary_stance:
            st.success("📈 **股市利多**：資金成本降低挹注流動性，科技巨頭預期迎來強勁反彈。")
            st.error("📉 **債市預測**：降息預期將帶動既有債券價格上漲。")
        else:
            st.info("⚖️ **市場觀望**：政策中立，大盤預期區間震盪，建議維持定期定額。")
            
    # [Tab 3] 未來三個季度推演
    with tab3:
        st.markdown("### 🔮 基於當前 State 的未來經濟路徑推演模型")
        
        # 定義時間序列與預測邏輯
        periods = ["0. 當前 (Now)", "1. Q1 (預測)", "2. Q2 (預測)", "3. Q3 (預測)"]
        
        if inflation > 3.0 and deficit_gdp > 5.0:
            # 高通膨+高赤字：螺旋上升
            cpi_trend = [inflation, inflation+0.5, inflation+1.2, inflation+1.8]
            rate_trend = [policy_rate, policy_rate+0.5, policy_rate+1.25, policy_rate+2.0]
            def_trend = [deficit_gdp, deficit_gdp+0.2, deficit_gdp+0.5, deficit_gdp+0.8]
            status_title = "🚨 預測結果：【高通膨與高赤字失控螺旋】"
            desc_1 = "通膨預期僵化，央行被迫持續猛烈升息。"
            desc_2 = "高赤字導致政府大舉發債，長天期殖利率狂飆。"
            desc_3 = "爆發嚴重『排擠效應』，民間企業融資成本過高引發倒閉潮，經濟面臨硬著陸。"
            
        elif inflation < 0.0 and monetary_stance == "極度寬鬆" and deficit_gdp > 5.0:
            # 完美救市：通膨回穩，赤字下降
            cpi_trend = [inflation, inflation+1.0, inflation+2.0, 2.0] 
            rate_trend = [policy_rate, policy_rate, policy_rate+0.25, policy_rate+0.5]
            def_trend = [deficit_gdp, deficit_gdp-1.0, deficit_gdp-2.0, deficit_gdp-3.0]
            status_title = "🚀 預測結果：【完美雙寬鬆復甦】"
            desc_1 = "央行流動性注入，恐慌情緒消退。"
            desc_2 = "財政擴張帶動就業，民眾實質購買力回升。"
            desc_3 = "成功脫離流動性陷阱，通膨溫和回升至 2% 目標。"
            
        elif inflation <= 3.0 and deficit_gdp > 5.0:
            # 軟著陸但財政拖累
            cpi_trend = [inflation, inflation+0.2, inflation+0.5, inflation+0.8] 
            rate_trend = [policy_rate, policy_rate, policy_rate+0.25, policy_rate+0.25] 
            def_trend = [deficit_gdp, deficit_gdp, deficit_gdp+0.2, deficit_gdp+0.5] 
            status_title = "⚠️ 預測結果：【財政拖累與排擠效應發酵】"
            desc_1 = "通膨雖暫時受控，但政府持續發債開始吸乾市場流動性。"
            desc_2 = "民間企業發覺融資困難，實質民間投資(I)開始出現衰退。"
            desc_3 = "若不縮減赤字，經濟將從目前的『軟著陸』轉為『停滯性增長』。"
            
        else:
            # 平穩擴張
            cpi_trend = [inflation, 2.0, 2.0, 2.0]
            rate_trend = [policy_rate, policy_rate, policy_rate, policy_rate]
            def_trend = [deficit_gdp, max(0, deficit_gdp-0.5), max(0, deficit_gdp-1.0), 3.0]
            status_title = "⚖️ 預測結果：【平穩擴張期】"
            desc_1 = "政策協調良好，通膨與利率維持在良性區間。"
            desc_2 = "企業投資意願穩定，失業率維持低檔。"
            desc_3 = "國家經濟維持健康擴張步調。"

        # 建立 DataFrame 並繪製折線圖
        df_forecast = pd.DataFrame({
            "預估通膨率 CPI (%)": cpi_trend,
            "預估基準利率 (%)": rate_trend,
            "預估財政赤字 (%)": def_trend
        }, index=periods)
        
        st.write(f"#### {status_title}")
        
        # 顯示圖表
        st.line_chart(df_forecast, use_container_width=True)
        
        # 顯示文字說明
        st.markdown(f"- **近期 (Q1)**：{desc_1}")
        st.markdown(f"- **中期 (Q2)**：{desc_2}")
        st.markdown(f"- **遠期 (Q3)**：{desc_3}")
        
    st.divider()
    
    # ==========================================
    # 神級優化：MARL 系統獎勵函數 (Reward) 算分機制
    # ==========================================
    reward_score = 100 
    score_reasons = []

    if inflation > 3.0:
        reward_score -= 20
        score_reasons.append("高通膨環境 (-20)")
    elif inflation < 0:
        reward_score -= 30
        score_reasons.append("通縮衰退環境 (-30)")

    if deficit_gdp > 5.0 and inflation >= 0:
        reward_score -= 15
        score_reasons.append("排擠效應隱憂 (-15)")

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
    
    if reward_score >= 90:
        score_label = "決策極佳"
        label_color = "normal"
    elif reward_score >= 80:
        score_label = "良好但具隱患" 
        label_color = "normal"
    elif reward_score >= 60:
        score_label = "狀態普通，需盡快調整"
        label_color = "off"
    else:
        score_label = "🚨 嚴重危機，需立即介入"
        label_color = "inverse"

    st.metric(label="Agent 預測未來經濟穩定總得分", 
              value=f"{reward_score} / 100", 
              delta=score_label, 
              delta_color=label_color)
    
    st.caption(f"🧠 **模型算分依據**：基礎分數 100 分。本次預測結算包含：{', '.join(score_reasons)}。")

else:
    st.info("👈 請於左側設定觀測指標，並點擊『啟動 AI 決策與未來預測』")
