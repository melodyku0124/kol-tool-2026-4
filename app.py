import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網站基礎設定
st.set_page_config(page_title="KOL 數據決策中心", layout="wide")

st.title("🚀 KOL 受眾數據決策中心 (3.1版)")
st.write("目前居住地：日本 | 目標市場：台灣運動品牌")
st.markdown("---")

# --- 側邊欄：進階篩選 ---
st.sidebar.header("🔍 受眾精密篩選")
uploaded_file = st.sidebar.file_uploader("上傳 KOL 名單 (CSV)", type=["csv"])

# 初始數據
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    data = {
        "KOL帳號": ["Emily_Run", "Ski_Ken", "Marketing_Mark", "Tokyo_Aoi", "Mini_RoadRun", "Salomon_Fan"],
        "粉絲數": [52000, 15000, 89000, 31000, 12000, 45000],
        "女性比例%": [85, 30, 60, 55, 90, 40],
        "主要受眾國家": ["台灣", "日本", "台灣", "日本", "台灣", "台灣"],
        "類型": ["運動", "滑雪", "行銷", "旅遊", "運動", "品牌活動"],
        "互動率%": [5.5, 4.2, 2.1, 4.8, 6.5, 3.8]
    }
    df = pd.DataFrame(data)

# 確保欄位名稱正確無誤
country_col = "主要受眾國家"

# 篩選控制器
f_min = st.sidebar.slider("目標女性受眾 > (%)", 0, 100, 50)

# 這裡修正了剛才的錯字
available_countries = df[country_col].unique()
countries = st.sidebar.multiselect("目標市場", options=available_countries, default=available_countries)

# 執行過濾
mask = (df["女性比例%"] >= f_min) & (df[country_col].isin(countries))
res = df[mask]

# --- 主畫面：新增快速查詢區 ---
st.subheader("🔗 KOL 快速調查員")
col_input, col_link = st.columns([3, 1])
with col_input:
    ig_handle = st.text_input("輸入 IG 帳號 (不需加 @)", placeholder="例如: salomon_tw")
with col_link:
    if ig_handle:
        st.markdown(f"<br><a href='https://www.instagram.com/{ig_handle}/' target='_blank'><button style='background-color:#FF4B4B; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;'>開啟個人檔案</button></a>", unsafe_allow_html=True)

st.markdown("---")

# 顯示表格
st.subheader("📋 篩選名單")
st.dataframe(res, use_container_width=True)

# 統計分析
if not res.empty:
    st.subheader("📊 受眾組成分析")
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.bar(res, x="KOL帳號", y="粉絲數", color="女性比例%", title="規模與性別比", color_continuous_scale="Purples")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.scatter(res, x="女性比例%", y="互動率%", size="粉絲數", hover_name="KOL帳號", title="受眾精準度 vs 互動率")
        st.plotly_chart(fig2, use_container_width=True)

st.info("💡 專業建議：對於運動品牌，建議找女性比例 > 60% 且互動率高於 3% 的 KOL。")
