import streamlit as st
import random
import json
import os

st.set_page_config(page_title="eat what", layout="centered")

st.title("🎯 今天吃啥")

st.markdown("为每个选项设置概率，点击抽选按钮即可。")

# -------------------
# 配置部分
# -------------------
st.subheader("⚙️ 配置抽选项")

# 默认示例
default_items = [
    {"name": "当虹", "prob": 0.25},
    {"name": "pingpong", "prob": 0.1},
    {"name": "纳爱斯", "prob": 0.2},
    {"name": "沙县", "prob": 0.15},
    {"name": "5A", "prob": 0.2},
    {"name": "西北面", "prob": 0.1},
]

# 加载已有配置
config_file = "lottery_config.json"
if os.path.exists(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        default_items = json.load(f)

# 动态编辑
items = []
num_items = st.number_input("选项数量", 1, 20, len(default_items))

for i in range(num_items):
    col1, col2 = st.columns([3, 2])
    with col1:
        name = st.text_input(f"选项 {i+1} 名称", 
                             value=default_items[i]["name"] if i < len(default_items) else "")
    with col2:
        prob = st.number_input(f"概率 {i+1}", 0.0, None, 
                               value=default_items[i]["prob"] if i < len(default_items) else 0.0)

    items.append({"name": name, "prob": prob})


# 保存配置按钮
if st.button("💾 保存配置"):
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    st.success("配置已保存！")

# -------------------
# 抽选部分
# -------------------
st.subheader("🎰 开始抽选")

# 归一化
total_prob = sum(item["prob"] for item in items)
if total_prob == 0:
    st.error("概率总和不能为 0，请调整配置。")
else:
    weights = [item["prob"] / total_prob for item in items]

    if st.button("🎲 抽一次"):
        result = random.choices([i["name"] for i in items], weights=weights, k=1)[0]
        st.success(f"⭐ 抽选结果：**{result}**")

