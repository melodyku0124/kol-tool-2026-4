import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網站基礎設定
st.set_page_config(page_title="KOL 數據決策中心", layout="wide")

st.title("🛡️ KOL 數據決策中心 (實戰版)")
st.write("輸入帳號後，若資料庫已有資料將自動對比；若無，請點擊下方工具查詢。")
st.markdown("---")

# 2. 💎 這是你的「黃金資料庫」 💎
# 請直接把你想加入的 KOL 數據跟我說，我幫你填在這裡
# 格式： "帳號": {"粉絲數": 數字, "女性比例%": 數字, "互動率%": 數字, "類別": "標籤"}
DATABASE = {
    "salomon_tw": {"粉絲數": 45000, "女性比例%": 40, "互動率%": 3.8, "類別": "品牌官方"},
    "runwithmomo": {"粉絲數": 28000, "女性比例%": 70, "互動率%": 4.5, "類別": "馬拉松跑者"},
    "gemma_811": {"粉絲數": 120000, "女性比例%": 80, "互動率%": 3.2, "類別": "運動藝人"},
    "ski_ken": {"粉絲數": 15000, "女性比例%": 30, "互動率%": 5.8, "類別": "滑雪教練"}
}

# --- 檢索區 ---
st.subheader("🔍 KOL 快速檢索")
col1, col2, col3 = st.columns(3)
selected_kols = []

for i, col in enumerate([col1, col2, col3], 1):
    with col:
        name = st.text_input(f"KOL 帳號 {i}", key=f"input_{i}", placeholder="例如: gemma_811")
        
        if name:
            name_clean = name.lower().strip().replace('@', '')
            
            # --- 查詢按鈕區 (換成較少強制登入的工具) ---
            st.markdown(f"**🔗 外部數據查詢：**")
            # Speakrj 通常不需要登入就能看到粉絲增長趨勢
            st_url = f"https://www.speakrj.com/audit/report/{name_clean}/instagram"
            # Inflact 可以看最近的發文頻率與互動
            in_url = f"https://inflact.com/tools/profile-analyzer/user/{name_clean}/"
            
            st.markdown(f"""
            <a href="{st_url}" target="_blank"><button style="width:100%; margin-bottom:5px; background-color:#6c5ce7; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">📊 查粉絲數據 (Speakrj)</button></a>
            <a href="{in_url}" target="_blank"><button style="width:100%; margin-bottom:5px; background-color:#fab1a0; color:black; border:none; padding:8px; border-radius:5px; cursor:pointer;">💡 查互動表現 (Inflact)</button></a>
            """, unsafe_allow_html=True)
            
            if name_clean in DATABASE:
                data = DATABASE[name_clean]
                st.success(f"✅ 數據已載入")
                st.write(f"**類別：** {data['類別']}")
                st.write(f"**粉絲：** {data['粉絲數']:,}")
                
                data_for_df = data.copy()
                data_for_df["KOL帳號"] = name_clean
                selected_kols.append(data_for_df)
            else:
                st.warning("⚠️ 此帳號尚未錄入內建資料庫")

# --- PK 圖表區 ---
if len(selected_kols) >= 1:
    st.markdown("---")
    df = pd.DataFrame(selected_kols)
    if len(selected_kols) >= 2:
        st.subheader("⚔️ 自動 PK 分析")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.bar(df, x="KOL帳號", y="粉絲數", color="KOL帳號", title="粉絲量對比"), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df, x="KOL帳號", y="互動率%", color="KOL帳號", title="互動率對比"), use_container_width=True)
