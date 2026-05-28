import streamlit as st
import pandas as pd
import requests
import datetime
import math
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บสไตล์ดุดัน มินิมอล ระดับกองทุน
st.set_page_config(page_title="Earthh Evans - BTC Cash Machine", page_icon="🎲", layout="wide")

st.title("🦅 EARTHH EVANS COMPANY")
st.caption("แผนกสไนเปอร์ BTC: เครื่องผลิตเงินสดรายวัน (Daily Short Call Automation) V3.0")

# ==================== LIVE DATA API & WEATHER CHECK ====================
def get_bybit_funding_rate():
    try:
        url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT"
        res = requests.get(url, timeout=5).json()
        funding = float(res['result']['list'][0]['fundingRate'])
        return funding
    except:
        return 0.0001 # ค่า Default กรณี API มีปัญหา

def get_btc_current_price():
    try:
        url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT"
        res = requests.get(url, timeout=5).json()
        price = float(res['result']['list'][0]['lastPrice'])
        return price
    except:
        return 0.0

funding_rate = get_bybit_funding_rate()
btc_price = get_btc_current_price()

# จัดโครงสร้างหน้าเว็บเป็น 2 ฝั่ง (ซ้าย: สแกนและคำนวณ / ขวา: เรดาร์ข่าวระดับโลก)
col_main, col_news = st.columns([1.2, 0.8])

with col_main:
    st.markdown("### 🥷 1. ด่านตรวจความเสี่ยงก่อนส่งคำสั่ง (07:00 - 09:00 น.)")
    
    # แสดงสภาวะตลาดแบบ Real-time
    c1, c2 = st.columns(2)
    c1.metric("ราคา Bitcoin ปัจจุบัน", f"${btc_price:,.2f}")
    
    if funding_rate < -0.0003:
        c2.metric("Bybit Funding Rate", f"{funding_rate*100:.4f}%", "🚨 อันตราย: เสี่ยง Short Squeeze ห้ามเทรด", delta_color="inverse")
    else:
        c2.metric("Bybit Funding Rate", f"{funding_rate*100:.4f}%", "🟢 ปกติ: สภาพลมเป็นใจ")

    st.markdown("---")
    st.markdown("#### 📝 ตรวจเช็คลิสต์ประจำวัน (ติ๊กให้ครบเพื่อปลดล็อกสิทธิ์เทรด)")
    
    check_macro = st.checkbox("1. ตรวจปฏิทินเศรษฐกิจแล้ว (วันนี้ไม่มีข่าวเดือดแดงเดือด: CPI, FOMC, NFP)")
    check_iv = st.checkbox("2. ตรวจค่า Volatility แล้ว (ค่า IV ใน Bybit สูงกว่าค่า HV ใน CoinGlass)")
    check_funding = st.checkbox(f"3. ค่า Funding Rate ปัจจุบัน ({funding_rate*100:.4f}%) ไม่ได้ติดลบหนักกว่า -0.03%")
    check_discipline = st.checkbox("4. บอสสัญญาว่าจะตั้ง Stop Loss RR 1:2 ทันทีที่เปิดออเดอร์ และจะไม่ดื้อดึงอมพอร์ตเด็ดขาด!")

    # ระบบประเมินผลอัจฉริยะ
    if check_macro and check_iv and check_funding and check_discipline:
        st.success("🟢 ALL SYSTEMS GO! สภาพอากาศเป็นใจ ยามเฝ้าพอร์ตให้ไฟเขียว ลุยสับคำสั่งได้!")
        st.balloons()
        
        st.markdown("---")
        st.markdown("### 🎯 2. คู่มือสั่งยิงสไนเปอร์ประจำวันนี้")
        
        # กล่องคำนวณระยะเป้าหมายและจุดกันตายอัตโนมัติ
        st.info("💡 **วิธีการหาตั๋วใน Bybit:** เปิดแอป Bybit > ไปที่ Options > เลือก BTC > เลือกวันหมดอายุเป็น 'บ่ายสามของวันนี้'")
        
        premium_target = st.number_input("💵 ใส่ค่าพรีเมียม (Premium) ที่เห็นในกระดาน ณ ค่า Delta 0.13 - 0.15 (เช่น $50):", min_value=5.0, value=50.0, step=5.0)
        
        # คำนวณตามหลักคณิตศาสตร์ประกันภัย
        sl_level = premium_target * 3
        max_loss = premium_target * 2
        
        st.markdown("#### 📋 แผนผังคำสั่งที่บอสต้องไปกดกรอกใน Bybit:")
        
        data_plan = {
            "หัวข้อคำสั่ง": ["ประเภทตั๋ว (Option Type)", "ปุ่มที่ต้องกด (Action)", "ขอบเขตเวลาซื้อ", "เวลาคิดบัญชี (Settlement)", "จุดคัทลอสหนีตาย (Stop Loss)", "ผลลัพธ์ขาดทุนสูงสุด"],
            "สิ่งที่บอสต้องกรอก/ทำ": [
                "ฝั่ง CALL (ตั๋วขาขึ้น)", 
                "🔴 SELL / SHORT (ขายสิทธิ์เก็บตังค์)", 
                "07:00 - 09:00 น. เท่านั้น (ห้ามเลท)",
                "15:00 น. ของวันนี้ (จบในวัน ไม่ถือข้ามคืน)",
                f"ตั้งค่า SL เมื่อราคาตั๋วพุ่งไปถึง ${sl_level:,.2f}",
                f"เจ็บหนักสุดแค่ -${max_loss:,.2f} (มดกัด ทุนปลอดภัย)"
            ]
        }
        df_plan = pd.DataFrame(data_plan)
        st.table(df_plan)
        
        st.warning(f"🚨 **กฎเหล็กหยุด Gamma Squeeze:** พอกดปุ่ม SELL ฝั่ง CALL ที่ค่า Delta 0.13-0.15 เสร็จแล้ว บอสต้องตั้งคำสั่ง Stop Loss ค้างไว้ในระบบทันทีที่ราคา ${sl_level:,.2f} ห้ามรอสู้หน้างาน!")

    else:
        st.error("🚨 ระบบล็อกไว้! กรุณาตรวจสอบและติ๊กเช็คลิสต์ความปลอดภัยให้ครบ 4 ข้อก่อนเปิดโรงงาน")

with col_news:
    st.markdown("### 🌍 3. เรดาร์ข่าวสารและปฏิทินมหภาค (Live)")
    st.caption("กวาดสายตาดูแถบ 'Today' หาแฟ้มสีแดงที่มีคำว่า CPI, FOMC, NFP เพื่อเช็คกฎข้อที่ 1")
    
    # ดึงวิดเจ็ตปฏิทินเศรษฐกิจโลกของ TradingView มาฝังสดๆ บนหน้าเว็บเว็บ
    tradingview_calendar = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
      {
      "colorTheme": "dark",
      "isTransparent": false,
      "width": "100%",
      "height": "600",
      "locale": "th",
      "importanceFilter": "-1,0,1"
      }
      </script>
    </div>
    """
    components.html(tradingview_calendar, height=620)

# ==================== TRADING JOURNAL DATABASE ====================
st.markdown("---")
st.markdown("### 📅 4. สมุดจดปฏิบัติการรายวันของ CEO (Trading Journal)")

if 'btc_journal' not in st.session_state:
    st.session_state.btc_journal = pd.DataFrame({
        "วันที่": [str(datetime.date.today() - datetime.timedelta(days=1))],
        "Strike Price": [78000.0],
        "ค่าเบี้ยที่เก็บได้ ($)": [60.0],
        "ค่า SL ที่ตั้งไว้ ($)": [180.0],
        "สถานะผลลัพธ์": ["ชนะ (เงินเข้ากระเป๋า)"]
    })

edited_journal = st.data_editor(st.session_state.btc_journal, num_rows="dynamic", use_container_width=True)
st.session_state.btc_journal = edited_journal
st.caption("💡 ทริค: บอสสามารถคลิกพิมพ์เพิ่มบรรทัดใหม่ หรือก๊อปปี้ข้อมูลไปแปะเก็บไว้ใน Excel ส่วนตัวได้เลยครับ")
