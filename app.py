import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網站基礎設定
st.set_page_config(page_title="KOL 三方 PK 工具", layout="wide")

st.title("⚔️ KOL 受眾三方 PK 儀表板")
st.write("輸入三個 KOL 帳號，手動填入數據後即可進行視覺化比較。")
st.markdown("---")

# --- 第一步：輸入區 ---
st.subheader("第一步：輸入要比較的 KOL 資訊")

col1, col2, col3 = st.columns(3)

# 準備存儲資料的清單
kol_data = []

for i, col in enumerate([col1, col2, col3], 1):
    with col:
        st.markdown(f"### KOL {i}")
        name = st.text_input(f"帳號 {i}", placeholder="例如: salomon_tw", key=f"name_{i}")
        
        # 快速輔助查詢按鈕
        if name:
            st.markdown(f"[🔍 去 IG 查看](https://www.instagram.com/{name}/) | [📊 查數據](https://www.modash.io/instagram-analyzer?username={name})")
        
        followers = st.number_input(f"粉絲總數", min_value=0, value=10000, key=f"fol_{i}")
        female_p = st.slider(f"女性受眾比例 (%)", 0, 100, 50, key=f"fem_{i}")
        eng_r = st.number_input(f"互動率 (%)", min_value=0.0, max_value=100.0, value=3.0, step=0.1, key=f"eng_{i}")
        
        if name:
            kol_data.append({
                "KOL帳號": name,
                "粉絲總數": followers,
                "女性比例%": female_p,
                "互動率%": eng_r
            })

# --- 第二步：比較分析 ---
if len(kol_data) >= 2:
    st.markdown("---")
    st.subheader("第二步：PK 結果分析")
    
    df_compare = pd.DataFrame(kol_data)
    
    # 數據表格
    st.table(df_compare)
    
    # 視覺化圖表
    c_chart1, c_chart2 = st.columns(2)
    
    with c_chart1:
        # 粉絲規模比較
        fig_size = px.bar(df_compare, x="KOL帳號", y="粉絲總數", color="KOL帳號
