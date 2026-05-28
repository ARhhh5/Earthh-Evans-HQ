import streamlit as st
import pandas as pd
from datetime import date
import requests
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าเว็บศูนย์บัญชาการ
st.set_page_config(page_title="Earthh Evans | BTC Sniper", page_icon="🥷", layout="wide")
st.title("🥷 ศูนย์บัญชาการแผนกสไนเปอร์ BTC (Daily Short Call)")
st.caption("ระบบดึงข้อมูลอัตโนมัติ & สมุดจดบัญชี (ทุน $10,000 | เป้าหมาย 3-5%/เดือน)")

st.markdown("---")

# 2. เรดาร์รับสัญญาณสด (Live Data Feed)
st.markdown("### 📡 เรดาร์จับสัญญาณตลาด (ไม่ต้องเปิดเว็บอื่นแล้วบอส!)")

col_data1, col_data2 = st.columns([1, 2])

with col_data1:
    st.markdown("**1. ค่าความผันผวน & ทิศทางลม (Live)**")
    # ดึง Funding Rate สดๆ จาก Bybit (Public API ไม่ต้องใช้ Key)
    try:
        res = requests.get("https://api.bybit.com/v5/market/funding/history?category=linear&symbol=BTCUSDT&limit=1").json()
        funding_rate = float(res['result']['list'][0]['fundingRate']) * 100
        
        if funding_rate < -0.03:
            st.error(f"🚨 Funding Rate: {funding_rate:.4f}% (อันตราย! ระวังโดนลาก Short Squeeze)")
        elif funding_rate > 0.03:
            st.success(f"🟢 Funding Rate: {funding_rate:.4f}% (ดีมาก! ตลาด Greedy)")
        else:
            st.info(f"🟡 Funding Rate: {funding_rate:.4f}% (ตลาดปกติ สภาพกลางๆ)")
    except:
        st.warning("ระบบดึง Funding Rate กำลังปรับปรุง")

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📊 **IV vs HV Check:** บอสเปิดกระดาน Bybit ควบคู่กัน ถ้าราคาพรีเมียมแพงเว่อร์ (IV สูงกว่าปกติ) จัดการสไนป์ได้เลย!")

with col_data2:
    st.markdown("**2. ปฏิทินข่าว Macro (Live TradingView)**")
    # ฝัง Widget ปฏิทินเศรษฐกิจแบบสดๆ ไว้ดู FOMC, CPI, NFP ในแอปเลย
    components.html("""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
      {
      "colorTheme": "dark",
      "isTransparent": true,
      "width": "100%",
      "height": "250",
      "locale": "th_TH",
      "importanceFilter": "0,1"
      }
      </script>
    </div>
    """, height=250)

st.markdown("---")

# 3. เช็คลิสต์กันตาย
st.markdown("### ✅ เช็คลิสต์ก่อนเหนี่ยวไก (ทำ 2 รอบ: 06:00 น. และ เที่ยงคืน)")
c1, c2 = st.columns(2)
with c1:
    chk1 = st.checkbox("1. 🚫 กวาดตาดูตารางข้างบนแล้ว วันนี้ไม่มีข่าว Macro แรงๆ (FOMC, CPI, NFP)")
    chk2 = st.checkbox("2. 📊 IV > HV (ส่องกระดานแล้ว เบี้ยประกันแพงคุ้มค่าเหนื่อย)")
with c2:
    chk3 = st.checkbox("3. 🟢 เรดาร์ Funding Rate ข้างบนไม่ได้แจ้งเตือนสีแดง (ไม่ติดลบหนัก)")
    chk4 = st.checkbox("4. 🎯 เล็งเป้า Strike Price ที่ค่า Delta 0.13 - 0.15 เรียบร้อย")

if chk1 and chk2 and chk3 and chk4:
    st.success("🟢 ALL SYSTEMS GO! สภาพตลาดปลอดภัย บอสไปเซ็ตเงื่อนไขกดออเดอร์แล้วไปนอนได้เลย!")
    st.balloons()
else:
    st.warning("🚨 เช็คลิสต์ยังไม่ครบ! ถ้าระบบไม่ให้ผ่าน ห้ามฝืนเปิดออเดอร์เด็ดขาด (จำบทเรียน Gamma Squeeze ไว้บอส!)")

st.markdown("---")

# 4. สมุดจดการเทรด (P&L Tracking)
st.markdown("### 📓 สมุดบันทึก P&L (บันทึกเสร็จรอ Settled บ่าย 3)")

if 'btc_journal' not in st.session_state:
    st.session_state.btc_journal = pd.DataFrame({
        "วันที่": [date.today().strftime("%Y-%m-%d")],
        "Strike Price": [75000],
        "ค่าพรีเมียม ($)": [20.0],
        "SL RR 1:2 ($)": [60.0], 
        "สถานะ": ["รอลุ้นบ่าย 3"] 
    })

edited_df = st.data_editor(st.session_state.btc_journal, num_rows="dynamic", use_container_width=True)
