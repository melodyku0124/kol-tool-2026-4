import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網頁基礎設定
st.set_page_config(page_title="KOL 內建數據 PK 系統", layout="wide")

st.title("⚔️ KOL 自動數據 PK 系統 (4.2 內建版)")
st.write("輸入帳號，系統將自動檢索內建資料庫。")
st.markdown("---")

# 2. 這是你的「專屬資料庫」
# 未來你可以把查到的資料傳給我，我幫你加進這裡
DATABASE = {
    "salomon_tw": {"粉絲數": 45000, "女性比例%": 40, "互動率%": 3.8},
    "ski_expert_jp": {"粉絲數": 12000, "女性比例%": 35, "互動率%": 6.2},
    "marketing_queen": {"粉絲數": 89000, "女性比例%": 85, "互動率%": 2.1},
    "running_girl_emily": {"粉絲數": 52000, "女性比例%": 92, "互動率%": 5.5},
    "tokyo_lifestyle": {"粉絲數": 31000, "女性比例%": 60, "互動率%": 4.5}
}

# --- 輸入區 ---
st.subheader("第一步：檢索 KOL")
col1, col2, col3 = st.columns(3)
kol_list = []

for i, col in enumerate([col1, col2, col3], 1):
    with col:
        st.markdown(f"### 選手 {i}")
        name = st.text_input(f"輸入帳號", key=f"n{i}", help="試試看輸入 salomon_tw 或 running_girl_emily")
        
        # 自動檢查資料庫
        if name in DATABASE:
            st.success("✅ 已找到內建數據！")
            data = DATABASE[name]
            fols = st.number_input("粉絲數", value=data["粉絲數"], key=f"f{i}")
            fem = st.slider("女性比例 (%)", 0, 100, data["女性比例%"], key=f"p{i}")
            eng = st.number_input("互動率 (%)", value=data["互動率%"], key=f"e{i}")
        else:
            if name:
                st.warning("⚠️ 尚未建立數據，請手動填入：")
            fols = st.number_input("粉絲數", min_value=0, value=10000, key=f"f{i}")
            fem = st.slider("女性比例 (%)", 0, 100, 50, key=f"p{i}")
            eng = st.number_input("互動率 (%)", value=3.0, key=f"e{i}")
        
        if name:
            kol_list.append({"KOL帳號": name, "粉絲數": fols, "女性比例%": fem, "互動率%": eng})

# --- 圖表分析區 ---
if len(kol_list) >= 2:
    st.markdown("---")
    st.subheader("第二步：數據 PK 分析")
    df = pd.DataFrame(kol_list)
    
    st.dataframe(df, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.bar(df, x="KOL帳號", y="粉絲數", color="KOL帳號", title="規模比較"), use_container_width=True)
    with c2:
        st.plotly_chart(px.scatter(df, x="女性比例%", y="互動率%", size="粉絲數", text="KOL帳號", title="精準度 vs 互動率"), use_container_width=True)
else:
    st.info("💡 提示：輸入 `salomon_tw` 和 `running_girl_emily` 看看自動帶入的效果！")
