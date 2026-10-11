import math
import string
import streamlit as st

# -------------------------------
# Matrix-Based Cryptographic System (Styled)
# -------------------------------

st.set_page_config(
    page_title="Matrix AI Crypto",
    page_icon="🔐",
    layout="centered"
)

# Custom CSS for fonts, buttons, background
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 8px 20px;
    }
    .stTextArea textarea {
        border-radius: 10px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo placeholder

import os
import streamlit as st

logo_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "logo.png"
)

if os.path.exists(logo_path):
    st.image(
        logo_path,
        width=120,
        caption="Matrix AI Crypto Logo"
    )
else:
    st.markdown("## 🌌 MATRIX AI CRYPTO")

st.title("🔐 Matrix-Based Cryptographic System")
st.write("Hill Cipher Encryption, Decryption and Security Monitoring")

st.info("Educational prototype with attractive UI and interactive dashboard.")

# Alphabet: A = 0, B = 1, ..., Z = 25
ALPHABET = string.ascii_uppercase

# Secret key matrix
K = [[3, 3],
     [2, 5]]

# Inverse of K modulo 26
K_INV = [[15, 17],
         [20, 9]]

# Store demo information between button clicks
if "last_cipher" not in st.session_state:
    st.session_state.last_cipher = ""

if "last_padding" not in st.session_state:
    st.session_state.last_padding = False

if "attempts" not in st.session_state:
    st.session_state.attempts = {}

def clean_text(text):
    """Keep only letters A-Z."""
    return "".join(ch for ch in text.upper() if ch in ALPHABET)

def encrypt_message(message):
    text = clean_text(message)
    if not text:
        raise ValueError("Please enter a message containing letters A-Z.")
    padded = len(text) % 2 == 1
    if padded:
        text += "X"
    result = ""
    for i in range(0, len(text), 2):
        a = ALPHABET.index(text[i])
        b = ALPHABET.index(text[i + 1])
        c1 = (K[0][0] * a + K[0][1] * b) % 26
        c2 = (K[1][0] * a + K[1][1] * b) % 26
        result += ALPHABET[c1] + ALPHABET[c2]
    return result, padded

def decrypt_message(ciphertext):
    text = clean_text(ciphertext)
    if not text:
        raise ValueError("There is no ciphertext to decrypt.")
    if len(text) % 2 != 0:
        raise ValueError("Ciphertext must contain an even number of letters.")
    result = ""
    for i in range(0, len(text), 2):
        a = ALPHABET.index(text[i])
        b = ALPHABET.index(text[i + 1])
        p1 = (K_INV[0][0] * a + K_INV[0][1] * b) % 26
        p2 = (K_INV[1][0] * a + K_INV[1][1] * b) % 26
        result += ALPHABET[p1] + ALPHABET[p2]
    if (
        text == st.session_state.last_cipher
        and st.session_state.last_padding
        and result.endswith("X")
    ):
        result = result[:-1]
    return result

# Tabs for interactive dashboard
tab1, tab2, tab3 = st.tabs(["🔒 Encryption", "🔓 Decryption", "📊 Security Monitoring"])

with tab1:
    message = st.text_area("Enter your message", placeholder="Example: HELLO WORLD")
    if st.button("Encrypt Message", type="primary"):
        try:
            cleaned = clean_text(message)
            st.session_state.attempts[cleaned] = st.session_state.attempts.get(cleaned, 0) + 1
            ciphertext, was_padded = encrypt_message(message)
            st.session_state.last_cipher = ciphertext
            st.session_state.last_padding = was_padded
            st.success("Encryption successful!")
            st.code(ciphertext, language=None)
            if was_padded:
                st.caption("An X was added internally to complete the final letter pair.")
            st.write("Key matrix:")
            st.code("3  3\n2  5")
            st.write("Matrix determinant:", 9)
            st.write("GCD(9, 26):", math.gcd(9, 26))
            if st.session_state.attempts[cleaned] >= 3:
                st.warning("Security alert: repeated message detected.")
            if len(cleaned) > 100:
                st.warning("Security alert: unusually long message detected.")
        except ValueError as error:
            st.error(str(error))

with tab2:
    if st.session_state.last_cipher:
        st.write("Last encrypted message:")
        st.code(st.session_state.last_cipher, language=None)
        if st.button("Decrypt Last Message"):
            try:
                plaintext = decrypt_message(st.session_state.last_cipher)
                st.success("Decryption successful!")
                st.code(plaintext, language=None)
            except ValueError as error:
                st.error(str(error))
    else:
        st.write("Encrypt a message first to enable decryption.")

with tab3:
    st.write("Monitoring status: Interactive prototype")
    total_attempts = sum(st.session_state.attempts.values())
    repeated_messages = sum(1 for count in st.session_state.attempts.values() if count >= 3)
    st.metric("Encryption requests this session", total_attempts)
    st.metric("Messages submitted 3+ times", repeated_messages)
    st.bar_chart([total_attempts, repeated_messages])
    if repeated_messages > 0:
        st.warning("Repeated-message activity detected.")
    else:
        st.success("No repeated-message alert currently detected.")
    st.caption("This is a classroom prototype, not a production security system.")
