import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網頁基礎設定
st.set_page_config(page_title="KOL 三方 PK 工具", layout="wide")

st.title("⚔️ KOL 受眾三方 PK 儀表板")
st.write("輸入帳號並填入數據，即可進行視覺化比較。")
st.markdown("---")

# --- 輸入區 ---
st.subheader("第一步：輸入 KOL 資訊")
col1, col2, col3 = st.columns(3)
kol_list = []

# 設定三個輸入區塊
for i, col in enumerate([col1, col2, col3], 1):
    with col:
        st.markdown(f"### 選手 {i}")
        name = st.text_input(f"帳號", placeholder="例如: salomon_tw", key=f"n{i}")
        
        if name:
            st.markdown(f"[🔍 IG 傳送門](https://www.instagram.com/{name}/)")
            st.markdown(f"[📊 免費查數據](https://www.modash.io/instagram-analyzer?username={name})")
        
        fols = st.number_input(f"粉絲總數", min_value=0, value=10000, key=f"f{i}")
        fem = st.slider(f"女性受眾 (%)", 0, 100, 50, key=f"p{i}")
        eng = st.number_input(f"互動率 (%)", min_value=0.0, max_value=100.0, value=3.0, step=0.1, key=f"e{i}")
        
        if name:
            kol_list.append({
                "KOL帳號": name,
                "粉絲數": fols,
                "女性比例%": fem,
                "互動率%": eng
            })

# --- 圖表分析區 ---
if len(kol_list) >= 2:
    st.markdown("---")
    st.subheader("第二步：PK 結果分析")
    df = pd.DataFrame(kol_list)
    
    # 顯示數據表格
    st.dataframe(df, use_container_width=True)
    
    # 畫圖
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.bar(df, x="KOL帳號", y="粉絲數", color="KOL帳號", title="粉絲規模對比")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.scatter(df, x="女性比例%", y="互動率%", size="粉絲數", text="KOL帳號", title="性別精準度 vs 互動率")
        st.plotly_chart(fig2, use_container_width=True)
    
    st.success("✅ 數據已生成！你可以截圖這份報表分享給合作夥伴。")
else:
    st.info("💡 請至少填寫兩位 KOL 的名稱，網站將自動為你生成 PK 圖表。")
