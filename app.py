import streamlit as st

# URLパラメータを受け取る
params = st.query_params
if "field" in params and "value" in params:
    field = params["field"]
    value = "".join(filter(str.isdigit, params["value"]))
    if field in st.session_state:
        st.session_state[field] = value

st.title("日計表集計システム")

# メモ欄
st.subheader("📋 メモ欄")
st.text_area("メモ", placeholder="Live Textでコピーした内容をここに貼り付けてください",
             height=200, label_visibility="collapsed")

st.divider()

# 現金売上
st.subheader("💴 現金売上")
cash_val = st.text_input("現金売上金額", key="cash_amount",
              placeholder="金額を入力", label_visibility="collapsed")

st.divider()

ITEMS = [
    "クレジット",
    "QUICPay",
    "交通系IC",
    "楽天Edy",
    "東急ポイント払い",
    "楽天ポイント払い",
    "東急スマート払い",
]

BARCODE_ITEMS = [
    "PayPay",
    "d払い",
    "au PAY",
    "楽天ペイ",
    "メルペイ",
    "Alipay",
    "WeChat Pay",
]

REGS = ["レジ①", "レジ②", "レジ③"]

# ── 日計表入力フォーム ────────────────────────
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

# ── バーコード決済入力フォーム ────────────────
st.header("バーコード決済")

col1, col2, col3 = st.columns([3, 2, 2])
with col1:
    st.write("**テナント**")
with col2:
    st.write("**件数**")
with col3:
    st.write("**金額（円）**")

for item in BARCODE_ITEMS:
    count_key  = f"bar_{item}_count"
    amount_key = f"bar_{item}_amount"

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

    # 日計表の集計
    st.subheader("日計表（項目別）")
    reg_total_count  = 0
    reg_total_amount = 0

    for item in ITEMS:
        item_count  = 0
        item_amount = 0
        for reg_idx in range(len(REGS)):
            count_val  = st.session_state.get(f"reg{reg_idx}_{item}_count",  "")
            amount_val = st.session_state.get(f"reg{reg_idx}_{item}_amount", "")
            item_count  += int(count_val)  if count_val.strip()  != "" else 0
            item_amount += int(amount_val) if amount_val.strip() != "" else 0
        reg_total_count  += item_count
        reg_total_amount += item_amount
        st.write(f"**{item}**　{item_count}件　¥{item_amount:,}")

    st.divider()
    st.write(f"**日計表合計**　{reg_total_count}件　¥{reg_total_amount:,}")

    # バーコード決済の集計
    st.subheader("バーコード決済（テナント別）")
    bar_total_count  = 0
    bar_total_amount = 0

    for item in BARCODE_ITEMS:
        count_val  = st.session_state.get(f"bar_{item}_count",  "")
        amount_val = st.session_state.get(f"bar_{item}_amount", "")
        item_count  = int(count_val)  if count_val.strip()  != "" else 0
        item_amount = int(amount_val) if amount_val.strip() != "" else 0
        bar_total_count  += item_count
        bar_total_amount += item_amount
        st.write(f"**{item}**　{item_count}件　¥{item_amount:,}")

    st.divider()
    st.write(f"**バーコード決済合計**　{bar_total_count}件　¥{bar_total_amount:,}")

    # 現金売上
    cash_val    = st.session_state.get("cash_amount", "")
    cash_amount = int("".join(filter(str.isdigit, cash_val))) if cash_val.strip() != "" else 0

    # 総合計
    st.divider()
    grand_count  = reg_total_count  + bar_total_count
    grand_amount = reg_total_amount + bar_total_amount
    st.subheader(f"電子マネー総合計　{grand_count}件　¥{grand_amount:,}")
    st.subheader(f"💴 現金売上　¥{cash_amount:,}")
    st.subheader(f"🏆 総売上　¥{grand_amount + cash_amount:,}")
