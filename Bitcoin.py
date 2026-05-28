import streamlit as st
import pandas as pd
from datetime import date

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="BTC Cash Machine", page_icon="🪙", layout="wide")
st.title("🪙 BTC Cash Machine (Startup Phase)")
st.caption("สมุดจดบัญชีและเช็คลิสต์ปั๊มเงินสดรายวัน (BTC Daily Short Call)")

st.markdown("---")

# 2. กระสุนในคลัง (Capital Tracker)
st.markdown("### 💰 บัญชีคลังแสง (Bybit USDT)")
col1, col2, col3 = st.columns(3)
capital = col1.number_input("💸 ทุนตั้งต้น (USDT):", value=100.0, step=10.0)
current_port = col2.number_input("📈 ยอดพอร์ตปัจจุบัน (USDT):", value=100.0, step=10.0)

profit = current_port - capital
profit_pct = (profit / capital) * 100 if capital > 0 else 0

if profit >= 0:
    col3.metric("🎯 กำไรสุทธิ (Net Profit)", f"${profit:,.2f}", f"+{profit_pct:.2f}%")
else:
    col3.metric("🩸 ขาดทุนสุทธิ (Net Loss)", f"${profit:,.2f}", f"{profit_pct:.2f}%")

st.markdown("---")

# 3. เช็คลิสต์กันตาย (Pre-Trade Checklist)
st.markdown("### ✅ เช็คลิสต์สแกนจุดตาย (ทำทุกเช้า 07:00 น.)")
st.info("💡 ท่องไว้: โอกาสมีทุกวัน ถ้าเช็คลิสต์ไม่ผ่าน ปิดจอไปนอนซะ อย่าฝืนก้มเก็บเหรียญสิบหน้าสิบล้อ!")

c1, c2 = st.columns(2)
with c1:
    st.checkbox("1. 🚫 วันนี้ไม่มีประกาศตัวเลข Macro ใหญ่ๆ (เช่น FOMC, CPI, NFP)")
    st.checkbox("2. 📊 IV > HV (ค่าความกลัวสูงกว่าความจริง = ค่าพรีเมียมคุ้มที่จะเสี่ยง)")
with c2:
    st.checkbox("3. 🟢 Funding Rate ไม่ติดลบหนัก (ป้องกันตลาดโดนบีบ Short Squeeze)")
    st.checkbox("4. 🎯 เลือก Strike Price ที่ค่า Delta อยู่ระหว่า 0.13 - 0.15 เท่านั้น")

st.markdown("---")

# 4. สมุดจดการเทรดรายวัน (Trade Journal)
st.markdown("### 📓 สมุดบันทึกปฏิบัติการรายวัน (Trade Journal)")
st.caption("กรอกบันทึกทุกครั้งที่เข้าเทรด เพื่อดูสถิติ Win Rate ของตัวเอง")

# สร้างตารางเปล่าๆ ไว้ให้กรอกข้อมูล
if 'btc_journal' not in st.session_state:
    st.session_state.btc_journal = pd.DataFrame({
        "วันที่": [date.today().strftime("%Y-%m-%d")],
        "Strike Price": [75000],
        "ค่าพรีเมียมที่รับ ($)": [20.0],
        "จุดยอมตาย SL 1:2 ($)": [60.0], # Option price x3
        "สถานะ": ["รอลุ้นบ่าย 3"] # ชนะ (เก็บเต็ม), แพ้ (ชน SL), รอลุ้นบ่าย 3
    })

# ใช้ data_editor ให้ลูกพี่พิมพ์แก้ข้อมูลลงไปตรงๆ บนหน้าเว็บได้เลย
edited_df = st.data_editor(st.session_state.btc_journal, num_rows="dynamic", use_container_width=True)

st.markdown("---")

# 5. กฎเหล็ก
st.markdown(
    """
    <div style="background-color: rgba(255, 94, 94, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #ff5e5e;">
        <h4 style="margin-top: 0; color: #ff5e5e;">🚨 กฎเหล็กประจำบริษัท (ห้ามแหกเด็ดขาด)</h4>
        <ol style="margin-bottom: 0;">
            <li><b>จุดตัดไฟ:</b> ทันทีที่ราคาออปชันวิ่งขึ้นไปถึง 3 เท่าของราคาที่เราขาย (ขาดทุน 2 เท่าของกำไร) ต้องกดซื้อคืนเพื่อ Cut Loss ทันที!</li>
            <li><b>หยุดพัก:</b> ถ้าซวยจัด โดน Stop Loss กินติดกัน 3 วันรวด ให้สั่งปิดแผนกนี้ไปพักร้อน 2-3 วันเพื่อดึงสติ</li>
        </ol>
    </div>
    """, unsafe_allow_html=True
)