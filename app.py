import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網頁基礎設定
st.set_page_config(page_title="KOL 跨平台數據分析中心", layout="wide")

st.title("🛡️ KOL 數據決策中心 (方案A版)")
st.write("輸入帳號，系統將為你準備好所有深度分析的傳送門。")
st.markdown("---")

# 2. 你的專屬數據庫 (目前暫存你手邊已有的數據)
DATABASE = {
    "salomon_tw": {"粉絲數": 45000, "女性比例%": 40, "互動率%": 3.8, "類別": "品牌官方"},
    "running_girl_emily": {"粉絲數": 52000, "女性比例%": 92, "互動率%": 5.5, "類別": "路跑運動員"},
    "tokyo_lifestyle": {"粉絲數": 31000, "女性比例%": 60, "互動率%": 4.5, "類別": "生活旅遊"}
}

# --- 檢索區 ---
st.subheader("🔍 KOL 深度調查與比較")
col1, col2, col3 = st.columns(3)
selected_kols = []

for i, col in enumerate([col1, col2, col3], 1):
    with col:
        name = st.text_input(f"KOL 帳號 {i}", key=f"input_{i}", placeholder="例如: gemma_811")
        
        if name:
            name_clean = name.lower().strip()
            
            # --- 深度分析按鈕區 ---
            st.markdown(f"#### 📊 數據快速查詢")
            st.markdown(f"""
            <a href="https://www.modash.io/instagram-analyzer?username={name_clean}" target="_blank"><button style="width:100%; margin-bottom:5px; background-color:#4CAF50; color:white; border:none; padding:8px; border-radius:5px;">🔍 查性別/國家 (Modash)</button></a>
            <a href="https://hypeauditor.com/ig/{name_clean}/" target="_blank"><button style="width:100%; margin-bottom:5px; background-color:#2196F3; color:white; border:none; padding:8px; border-radius:5px;">📈 查品質評分 (HypeAuditor)</button></a>
            <a href="https://www.instagram.com/{name_clean}/" target="_blank"><button style="width:100%; background-color:#E1306C; color:white; border:none; padding:8px; border-radius:5px;">📸 開啟 IG 原生頁面</button></a>
            """, unsafe_allow_html=True)
            
            # 檢查是否在資料庫中
            if name_clean in DATABASE:
                data = DATABASE[name_clean]
                st.info(f"內建數據已加載：{data['粉絲數']:,} 粉絲")
                data_for_df = data.copy()
                data_for_df["KOL帳號"] = name_clean
                selected_kols.append(data_for_df)
            else:
                st.caption("💡 查完數據了嗎？若需將此人加入長期資料庫，請聯繫技術長更新代碼。")

# --- 自動分析區 ---
if len(selected_kols) >= 1:
    st.markdown("---")
    df = pd.DataFrame(selected_kols)
    
    if len(selected_kols) >= 2:
        st.subheader("⚔️ 已存檔數據對比")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.bar(df, x="KOL帳號", y="粉絲數", color="KOL帳號", title="粉絲規模"), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df, x="KOL帳號", y="互動率%", color="KOL帳號", title="互動表現"), use_container_width=True)
