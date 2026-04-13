import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網站基礎設定
st.set_page_config(page_title="KOL 數據決策中心", layout="wide")

st.title("🛡️ KOL 數據決策中心 (方案A 強化版)")
st.write("輸入帳號，直接跳轉至第三方工具的『數據報告頁』。")
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
            # 移除帳號前的 @ 符號，避免網址錯誤
            if name_clean.startswith('@'):
                name_clean = name_clean[1:]
            
            # --- 深度分析按鈕區 (優化網址結構) ---
            st.markdown(f"#### 📊 數據快速查詢")
            
            # Modash: 使用正確的搜尋參數
            modash_url = f"https://www.modash.io/instagram-analyzer?username={name_clean}"
            # HypeAuditor: 需要特定的網址路徑
            hype_url = f"https://hypeauditor.com/ig/{name_clean}/"
            # SocialBlade: 另一個強大的免費數據站
            social_blade_url = f"https://socialblade.com/instagram/user/{name_clean}"
            
            st.markdown(f"""
            <a href="{modash_url}" target="_blank"><button style="width:100%; margin-bottom:5px; background-color:#4CAF50; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">🔍 查受眾性別 (Modash)</button></a>
            <a href="{hype_url}" target="_blank"><button style="width:100%; margin-bottom:5px; background-color:#2196F3; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">📈 查品質評分 (HypeAuditor)</button></a>
            <a href="{social_blade_url}" target="_blank"><button style="width:100%; margin-bottom:5px; background-color:#333333; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">📊 查粉絲增長 (SocialBlade)</button></a>
            <a href="https://www.instagram.com/{name_clean}/" target="_blank"><button style="width:100%; background-color:#E1306C; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">📸 前往 IG 頁面</button></a>
            """, unsafe_allow_html=True)
            
            if name_clean in DATABASE:
                data = DATABASE[name_clean]
                st.info(f"✅ 內建數據：{data['粉絲數']:,} 粉絲")
                data_for_df = data.copy()
                data_for_df["KOL帳號"] = name_clean
                selected_kols.append(data_for_df)
            else:
                st.warning("⚠️ 此人尚未加入內建比較表")

# --- 自動分析區 ---
if len(selected_kols) >= 1:
    st.markdown("---")
    df = pd.DataFrame(selected_kols)
    if len(selected_kols) >= 2:
        st.subheader("⚔️ 已存檔數據快速對比")
        st.dataframe(df, use_container_width=True)
        st.plotly_chart(px.bar(df, x="KOL帳號", y="粉絲數", color="KOL帳號", title="粉絲規模對比"), use_container_width=True)
