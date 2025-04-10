import streamlit as st
import re
import urllib
from urllib.parse import urlparse

st.set_page_config(page_title="🛡️ URL Phishing Detector", layout="centered")
st.title("🛡️ Deteksi URL Phishing")
st.write("Masukkan URL di bawah untuk memeriksa apakah URL mencurigakan atau tidak.")

url = st.text_input("🔗 Masukkan URL")

# Cek karakteristik phishing
def is_phishing(url):
    parsed = urlparse(url)
    checks = {
        "Pakai IP address": bool(re.match(r"^http[s]?://\\d+\\.\\d+\\.\\d+\\.\\d+", url)),
        "Terlalu panjang (>75)": len(url) > 75,
        "Mengandung @": "@" in url,
        "Terlalu banyak -": url.count('-') > 5,
        "Mengandung banyak subdomain": parsed.hostname.count('.') > 3,
        "HTTPS valid": parsed.scheme == "https"
    }
    return checks

if st.button("🚨 Cek URL"):
    if not url:
        st.warning("Silakan masukkan URL terlebih dahulu.")
    else:
        try:
            result = is_phishing(url)
            st.subheader("🔍 Hasil Analisis:")
            for k, v in result.items():
                emoji = "✅" if (k == "HTTPS valid" and v) or (k != "HTTPS valid" and not v) else "⚠️"
                st.write(f"{emoji} {k}: {'Mencurigakan' if v else 'Aman'}")

            skor = sum(1 for v in result.values() if v and k != "HTTPS valid")
            st.markdown("---")
            if skor >= 3:
                st.error("⚠️ URL ini **berpotensi phishing**. Harap waspada.")
            elif skor == 2:
                st.warning("🟡 URL ini cukup mencurigakan. Periksa lebih lanjut.")
            else:
                st.success("✅ URL ini tampak aman secara umum.")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memeriksa URL: {e}")
