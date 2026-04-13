import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網站基礎設定
st.set_page_config(page_title="KOL 粉絲篩選網", layout="wide")
st.title("🌐 KOL 受眾精準篩選器")
st.write("這是專屬你的 KOL 篩選工具。目前的數據包含性別與主要國家分析。")

# 2. 核心數據 (未來我們可以改成讀取 Excel)
# 這裡我先放幾筆範例資料，讓你感受效果
data = {
    "KOL 名稱": ["運動女孩 Emily", "滑雪教練 Ken", "行銷專家 Mark", "東京生活 Aoi", "路跑甜心 Mini"],
    "粉絲數": [52000, 15000, 89000, 31000, 12000],
    "女性粉絲比例(%)": [85, 30, 60, 55, 90],
    "主要國家": ["台灣", "日本", "台灣", "日本", "台灣"],
    "互動率(%)": [5.5, 4.2, 2.1, 4.8, 6.5]
}
df = pd.DataFrame(data)

# 3. 網站側邊欄：你的控制器
st.sidebar.header("🔍 篩選條件")

# 篩選 1：性別
f_ratio = st.sidebar.slider("最低女性粉絲佔比 (%)", 0, 100, 50)

# 篩選 2：國家
selected_country = st.sidebar.multiselect(
    "選擇受眾所在國家", 
    options=df["主要國家"].unique(), 
    default=df["主要國家"].unique()
)

# 執行篩選
filtered_df = df[
    (df["女性粉絲比例(%)"] >= f_ratio) & 
    (df["主要國家"].isin(selected_country))
]

# 4. 網頁顯示內容
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 符合條件的名單")
    st.dataframe(filtered_df, use_container_width=True)

with col2:
    st.subheader("📊 數據統計")
    st.metric("搜尋到人數", len(filtered_df))
    if not filtered_df.empty:
        st.metric("平均互動率", f"{filtered_df['互動率(%)'].mean():.1f}%")

# 視覺化圖表
st.markdown("### 粉絲分佈視覺化")
fig = px.pie(filtered_df, values='粉絲數', names='KOL 名稱', hole=.3, title="篩選名單佔比")
st.plotly_chart(fig, use_container_width=True)

st.info("💡 提示：你可以點擊側邊欄調整數值，網站會即時更新結果。")
