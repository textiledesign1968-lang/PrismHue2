import streamlit as st

# -----------------------------
# Conversion Functions
# -----------------------------

def hex_to_rgb(hex_code):
    hex_code = hex_code.strip().lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join([c*2 for c in hex_code])
    if len(hex_code) != 6:
        return None
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return r, g, b

def rgb_to_cmyk(r, g, b):
    r_p, g_p, b_p = r/255, g/255, b/255
    k = 1 - max(r_p, g_p, b_p)
    if k == 1:
        return 0, 0, 0, 100
    c = (1 - r_p - k) / (1 - k)
    m = (1 - g_p - k) / (1 - k)
    y = (1 - b_p - k) / (1 - k)
    return round(c*100), round(m*100), round(y*100), round(k*100)

def cmyk_to_rgb(c, m, y, k):
    c, m, y, k = c/100, m/100, y/100, k/100
    r = round(255 * (1 - c) * (1 - k))
    g = round(255 * (1 - m) * (1 - k))
    b = round(255 * (1 - y) * (1 - k))
    return r, g, b

def rgb_to_hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="HEX ⇄ CMYK Converter", page_icon="🎨")

st.title("🎨 HEX ⇄ CMYK Converter")
st.write("Convert between HEX and CMYK instantly with live color preview.")

# HEX → CMYK
st.subheader("HEX → CMYK")
hex_input = st.text_input("Enter HEX code", "#D4B39A")

if hex_input:
    rgb = hex_to_rgb(hex_input)
    if rgb:
        cmyk = rgb_to_cmyk(*rgb)
        st.write(f"**RGB:** {rgb}")
        st.write(f"**CMYK:** C {cmyk[0]}%, M {cmyk[1]}%, Y {cmyk[2]}%, K {cmyk[3]}%")
        st.color_picker("Preview", rgb_to_hex(*rgb), disabled=True)
    else:
        st.error("Invalid HEX format. Use something like #D4B39A.")

# CMYK → HEX
st.subheader("CMYK → HEX")
c = st.number_input("C (%)", 0, 100, 0)
m = st.number_input("M (%)", 0, 100, 0)
y = st.number_input("Y (%)", 0, 100, 0)
k = st.number_input("K (%)", 0, 100, 0)

if st.button("Convert CMYK → HEX"):
    rgb = cmyk_to_rgb(c, m, y, k)
    hex_code = rgb_to_hex(*rgb)
    st.write(f"**RGB:** {rgb}")
    st.write(f"**HEX:** {hex_code}")
    st.color_picker("Preview", hex_code, disabled=True)
