import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網頁基礎設定
st.set_page_config(page_title="KOL 數據決策中心", layout="wide")

st.title("📊 KOL 自動化比較儀表板")
st.write("只需輸入帳號，系統將自動比對內建數據庫，無需手動輸入數值。")
st.markdown("---")

# 2. 你的專屬數據庫 (這裡是你目前觀察的清單)
# 你可以隨時傳新的數據給我，我幫你更新這段
DATABASE = {
    "salomon_tw": {"粉絲數": 45000, "女性比例%": 40, "互動率%": 3.8, "類別": "品牌官方"},
    "ski_expert_jp": {"粉絲數": 12000, "女性比例%": 35, "互動率%": 6.2, "類別": "滑雪教練"},
    "marketing_queen": {"粉絲數": 89000, "女性比例%": 85, "互動率%": 2.1, "類別": "行銷/科技"},
    "running_girl_emily": {"粉絲數": 52000, "女性比例%": 92, "互動率%": 5.5, "類別": "路跑運動員"},
    "tokyo_lifestyle": {"粉絲數": 31000, "女性比例%": 60, "互動率%": 4.5, "類別": "生活旅遊"}
}

# --- 檢索區 ---
st.subheader("🔍 輸入要比較的帳號")
col1, col2, col3 = st.columns(3)
selected_kols = []

# 建立三個純文字輸入框
for i, col in enumerate([col1, col2, col3], 1):
    with col:
        name = st.text_input(f"KOL 帳號 {i}", key=f"user_input_{i}", placeholder="輸入帳號...")
        
        if name:
            name_clean = name.lower().strip() # 自動處理大小寫與空格
            if name_clean in DATABASE:
                data = DATABASE[name_clean]
                st.success(f"✅ {name_clean} 數據已載入")
                # 僅顯示數據，不提供輸入框
                st.write(f"📌 **類別：** {data['類別']}")
                st.write(f"👥 **粉絲：** {data['粉絲數']:,}")
                st.write(f"👩 **女性：** {data['女性比例%']}%")
                st.write(f"📈 **互動：** {data['互動率%']}%")
                
                # 存入列表準備畫圖
                data_for_df = data.copy()
                data_for_df["KOL帳號"] = name_clean
                selected_kols.append(data_for_df)
            else:
                st.error("❌ 資料庫中無此帳號")
                st.info("請聯絡技術長更新數據庫。")

# --- 自動繪圖區 ---
if len(selected_kols) >= 1:
    st.markdown("---")
    df = pd.DataFrame(selected_kols)
    
    # 如果有兩個人以上，就顯示 PK 圖表
    if len(selected_kols) >= 2:
        st.subheader("⚔️ PK 數據分析")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.bar(df, x="KOL帳號", y="粉絲數", color="KOL帳號", title="粉絲規模對比"), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df, x="KOL帳號", y="互動率%", color="KOL帳號", title="互動表現對比"), use_container_width=True)
    else:
        st.info("再輸入一個帳號即可開啟 PK 圖表。")
