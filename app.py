import streamlit as st
# URLパラメータを受け取る
params = st.query_params
if "field" in params and "value" in params:
    field = params["field"]
    value = "".join(filter(str.isdigit, params["value"]))
    if field in st.session_state:
        st.session_state[field] = value
st.title("日計表集計システム")

ITEMS = [
    "クレジット",
    "QUICPay",
    "交通系IC",
    "楽天Edy",
    "東急ポイント払い",
    "楽天ポイント払い",
    "東急スマート払い",
]

REGS = ["レジ①", "レジ②", "レジ③"]

# ── 入力フォーム ──────────────────────────────
for reg_idx, reg_name in enumerate(REGS):
    st.header(reg_name)

    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.write("**項目**")
    with col2:
        st.write("**件数**")
    with col3:
        st.write("**金額（円）**")

    for item in ITEMS:
        count_key  = f"reg{reg_idx}_{item}_count"
        amount_key = f"reg{reg_idx}_{item}_amount"

        # 数字以外を自動で除去
        for key in [count_key, amount_key]:
            if key in st.session_state:
                cleaned = "".join(filter(str.isdigit, str(st.session_state[key])))
                if cleaned != st.session_state[key]:
                    st.session_state[key] = cleaned

        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(item)
        with col2:
            st.text_input("件数", key=count_key,
                          placeholder="件数", label_visibility="collapsed")
        with col3:
            st.text_input("金額", key=amount_key,
                          placeholder="金額", label_visibility="collapsed")

    st.divider()

# ── 合計計算 ──────────────────────────────────
st.header("集計結果")

if st.button("合計を計算する"):
    total_count  = 0
    total_amount = 0

    for item in ITEMS:
        item_count  = 0
        item_amount = 0

        for reg_idx in range(len(REGS)):
            count_val  = st.session_state.get(f"reg{reg_idx}_{item}_count",  "")
            amount_val = st.session_state.get(f"reg{reg_idx}_{item}_amount", "")

            item_count  += int(count_val)  if count_val.strip()  != "" else 0
            item_amount += int(amount_val) if amount_val.strip() != "" else 0

        total_count  += item_count
        total_amount += item_amount

        st.write(f"**{item}**　{item_count}件　¥{item_amount:,}")

    st.divider()
    st.subheader(f"総合計　{total_count}件　¥{total_amount:,}")