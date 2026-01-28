import streamlit as st
import random

st.set_page_config(page_title="Caesar Cipher Tool", page_icon="🔐")

st.title("🔐 Caesar Cipher – File Encryption & Decryption")

choice = st.radio(
    "Choose an option:",
    ("Encryption (Random Key)", "Decryption (Try all 26 combinations)")
)

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    # ---------------- ENCRYPTION ----------------
    if choice == "Encryption (Random Key)":
        key = random.randint(0, 25)
        encrypted = ""

        for ch in text:
            if ch.isupper():
                encrypted += chr((ord(ch) - 65 + key) % 26 + 65)
            elif ch.islower():
                encrypted += chr((ord(ch) - 97 + key) % 26 + 97)
            else:
                encrypted += ch

        st.success("Encryption Successful ✅")
        st.write("🔑 **Random Key Used:**", key)

        st.download_button(
            label="⬇️ Download Encrypted File",
            data=encrypted,
            file_name="encrypted.txt",
            mime="text/plain"
        )

    # ---------------- DECRYPTION ----------------
    elif choice == "Decryption (Try all 26 combinations)":
        output = ""

        for key in range(26):
            decrypted = ""
            for ch in text:
                if ch.isupper():
                    decrypted += chr((ord(ch) - 65 - key) % 26 + 65)
                elif ch.islower():
                    decrypted += chr((ord(ch) - 97 - key) % 26 + 97)
                else:
                    decrypted += ch

            output += f"Key {key}:\n{decrypted}\n\n"

        st.success("Decryption Completed ✅")

        st.download_button(
            label="⬇️ Download Decrypted File",
            data=output,
            file_name="decrypted.txt",
            mime="text/plain"
        )