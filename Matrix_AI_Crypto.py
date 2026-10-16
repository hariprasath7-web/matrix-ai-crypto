import math
import string
import streamlit as st

st.set_page_config(
    page_title="MATRIX AI CRYPTO",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --bg:#070914; --panel:#101426; --panel2:#151b32; --line:rgba(157,146,255,.20); --purple:#9B8CFF; --cyan:#56E0F0; --text:#F4F5FF; --muted:#9BA5C7; }
html, body, [class*="css"] { font-family:'Space Grotesk',sans-serif; }
.stApp { background:
 radial-gradient(ellipse at 8% 0%, rgba(90,62,190,.20), transparent 35%),
 radial-gradient(ellipse at 92% 8%, rgba(34,174,202,.10), transparent 28%),
 var(--bg); color:var(--text); }
.block-container { max-width:1450px; padding-top:1.8rem; padding-bottom:3rem; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0D1020 0%,#0A0D19 100%); border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { font-family:'Space Grotesk',sans-serif; }
h1,h2,h3 { letter-spacing:-.035em; }
h1 { font-weight:700 !important; }
p, label, .stCaption { color:var(--muted); }
div[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(24,30,55,.95),rgba(13,17,34,.95)); border:1px solid var(--line); border-radius:18px; padding:18px 20px; box-shadow:0 8px 30px rgba(0,0,0,.16); }
div[data-testid="stMetricLabel"] { color:#AAB4D4; }
div[data-testid="stMetricValue"] { color:#F7F7FF; font-weight:700; }
.stButton > button { border-radius:12px; min-height:46px; font-weight:700; border:1px solid rgba(155,140,255,.45); background:linear-gradient(100deg,#7565ED,#9B6DFF); color:white; transition:all .2s ease; }
.stButton > button:hover { border-color:#67E8F9; box-shadow:0 0 22px rgba(86,224,240,.22); transform:translateY(-1px); color:white; }
.stTextArea textarea, .stTextInput input { background:#0D1224 !important; border:1px solid rgba(155,140,255,.28) !important; border-radius:12px !important; color:#F4F5FF !important; }
.stTextArea textarea:focus, .stTextInput input:focus { border-color:#8D80FF !important; box-shadow:0 0 0 1px #8D80FF !important; }
.stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid var(--line); }
.stTabs [data-baseweb="tab"] { background:#11162A; border:1px solid transparent; border-radius:12px 12px 0 0; padding:12px 18px; color:#B8C0DD; }
.stTabs [aria-selected="true"] { background:#211C46 !important; border-color:rgba(155,140,255,.38) !important; color:white !important; }
div[data-testid="stAlert"] { border-radius:12px; }
hr { border-color:var(--line); }
[data-testid="stDataFrame"], .stPlotlyChart { border-radius:14px; overflow:hidden; }
.smallcaps { color:#8F8AFF; font-size:.73rem; letter-spacing:.20em; font-weight:700; text-transform:uppercase; }
.hero { border:1px solid rgba(155,140,255,.28); border-radius:26px; padding:30px 32px; background:linear-gradient(115deg,rgba(31,27,72,.96),rgba(13,21,43,.94) 62%,rgba(10,38,51,.88)); box-shadow:0 18px 55px rgba(0,0,0,.24); position:relative; overflow:hidden; }
.hero:after { content:''; position:absolute; width:230px; height:230px; border:1px solid rgba(86,224,240,.15); border-radius:50%; right:-55px; top:-80px; box-shadow:0 0 0 25px rgba(86,224,240,.025),0 0 0 55px rgba(155,140,255,.025); }
.hero-title { font-size:clamp(2rem,4vw,3.5rem); line-height:1.02; font-weight:700; letter-spacing:-.06em; color:#fff; margin:10px 0 12px; }
.gradient-text { background:linear-gradient(90deg,#B8AFFF,#63E8F3); -webkit-background-clip:text; background-clip:text; color:transparent; }
.hero-sub { max-width:690px; color:#B7C1E0; font-size:1.04rem; line-height:1.65; }
.pill { display:inline-block; border:1px solid rgba(86,224,240,.35); background:rgba(86,224,240,.08); color:#8EEBF3; border-radius:999px; padding:6px 11px; font-size:.75rem; font-weight:700; letter-spacing:.08em; }
.panel { border:1px solid var(--line); border-radius:18px; padding:20px; background:linear-gradient(150deg,rgba(20,26,48,.94),rgba(12,16,31,.96)); height:100%; }
.panel-label { color:#A2ACCC; font-size:.82rem; }
.panel-value { color:#F5F6FF; font-size:1.35rem; font-weight:700; margin-top:5px; }
.panel-note { color:#8F9ABA; font-size:.82rem; margin-top:7px; }
.code-result { border:1px solid rgba(86,224,240,.28); border-radius:14px; padding:18px; background:rgba(8,18,30,.8); }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

ALPHABET = string.ascii_uppercase
K = [[3, 3], [2, 5]]
K_INV = [[15, 17], [20, 9]]

def clean_text(value: str) -> str:
    return "".join(ch for ch in value.upper() if ch in ALPHABET)

def _put_letters_back(template: str, letters: str) -> str:
    """Replace A-Z slots with transformed letters, keeping spaces/punctuation."""
    letter_iter = iter(letters)
    formatted = []
    for char in template:
        if char.upper() in ALPHABET:
            formatted.append(next(letter_iter, ""))
        else:
            formatted.append(char)
    # The extra letter, if any, is the padding character appended during encryption.
    formatted.extend(letter_iter)
    return "".join(formatted)

def encrypt_message(message: str):
    text = clean_text(message)
    if not text:
        raise ValueError("Enter a message containing letters A–Z.")

    padded = len(text) % 2 == 1
    if padded:
        text += "X"

    out = []
    for i in range(0, len(text), 2):
        a, b = ALPHABET.index(text[i]), ALPHABET.index(text[i + 1])
        out.append(ALPHABET[(K[0][0]*a + K[0][1]*b) % 26])
        out.append(ALPHABET[(K[1][0]*a + K[1][1]*b) % 26])

    # Keep spaces and punctuation in their original positions for display.
    formatted_cipher = _put_letters_back(message, "".join(out))
    return formatted_cipher, padded, clean_text(message)

def decrypt_message(ciphertext: str, remove_padding=False):
    text = clean_text(ciphertext)
    if not text:
        raise ValueError("Enter ciphertext containing letters A–Z.")
    if len(text) % 2:
        raise ValueError("Ciphertext must contain an even number of letters.")

    out = []
    for i in range(0, len(text), 2):
        a, b = ALPHABET.index(text[i]), ALPHABET.index(text[i + 1])
        out.append(ALPHABET[(K_INV[0][0]*a + K_INV[0][1]*b) % 26])
        out.append(ALPHABET[(K_INV[1][0]*a + K_INV[1][1]*b) % 26])
    result = "".join(out)

    # Encryption appends its padding letter at the very end of the formatted text.
    # Remove that slot too, so spaces and punctuation remain correctly positioned.
    template = ciphertext
    if remove_padding and result.endswith("X") and template and template[-1].upper() in ALPHABET:
        result = result[:-1]
        template = template[:-1]

    return _put_letters_back(template, result)

if "history" not in st.session_state:
    st.session_state.history = []
if "encrypt_count" not in st.session_state:
    st.session_state.encrypt_count = 0
if "last_cipher" not in st.session_state:
    st.session_state.last_cipher = ""
if "last_plain" not in st.session_state:
    st.session_state.last_plain = ""
if "last_padded" not in st.session_state:
    st.session_state.last_padded = False
if "attempts" not in st.session_state:
    st.session_state.attempts = {}

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin:4px 0 22px">
      <div style="width:48px;height:48px;border-radius:15px;background:linear-gradient(135deg,#6D5AE8,#43D6E8);display:flex;align-items:center;justify-content:center;box-shadow:0 0 24px #7866d644">
        <svg width="30" height="30" viewBox="0 0 32 32" fill="none"><path d="M16 3L27 8V15C27 22 22 27 16 29C10 27 5 22 5 15V8L16 3Z" stroke="white" stroke-width="2"/><path d="M11 12H21M11 16H21M13 20H19" stroke="white" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="2" fill="#9EF4FF"/></svg>
      </div>
      <div><div style="font-weight:700;color:#fff;font-size:1.02rem">MATRIX <span style="color:#8F85FF">AI</span></div><div style="font-size:.68rem;color:#8995B8;letter-spacing:.15em">CRYPTO LAB</div></div>
    </div>
    <div class="smallcaps">Workspace</div>
    """, unsafe_allow_html=True)
    page = st.radio("Navigate", ["Overview", "Encrypt Message", "Decrypt Message", "Security Center", "About Project"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div class="smallcaps">System status</div>', unsafe_allow_html=True)
    st.markdown("🟢 **Cipher engine**  \n`READY`")
    st.markdown("🔷 **Matrix key**  \n`2 × 2`")
    st.markdown("🛡️ **Rule monitoring**  \n`ENABLED`")
    st.markdown("---")
    st.caption("Educational demonstration • Not for real confidential data")

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <span class="pill">✦ CRYPTOGRAPHY LAB / PROTOTYPE</span>
  <div class="hero-title">MATRIX <span class="gradient-text">AI CRYPTO</span></div>
  <div class="hero-sub">A matrix-powered encryption playground with message transformation, reverse decryption, and rule-based security activity monitoring.</div>
</div>
""", unsafe_allow_html=True)
st.write("")

total = len(st.session_state.history)
alerts = sum(1 for item in st.session_state.history if item.get("alert"))
unique = len(set(item.get("input", "") for item in st.session_state.history if item.get("input")))
m1, m2, m3, m4 = st.columns(4)
m1.metric("Encryption runs", st.session_state.encrypt_count, help="Number of encryption requests in this browser session")
m2.metric("Unique messages", unique)
m3.metric("Security alerts", alerts)
m4.metric("Cipher block", "2 × 2")

st.write("")
if page == "Overview":
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        st.markdown("### ◈ Control room")
        st.markdown('<div class="panel"><div class="smallcaps">Quick start</div><h3 style="margin:8px 0;color:#F5F6FF">Transform a message</h3><p>Try the demo below, or choose an operation from the left navigation. Letters are converted into numeric pairs and transformed using the secret matrix.</p></div>', unsafe_allow_html=True)
        demo = st.text_area("Message to encrypt", placeholder="Try: HELLO WORLD", key="overview_input", height=105)
        if st.button("⚡ Encrypt demo message", use_container_width=True):
            try:
                cipher, padded, cleaned = encrypt_message(demo)
                st.session_state.encrypt_count += 1
                st.session_state.attempts[cleaned] = st.session_state.attempts.get(cleaned, 0) + 1
                alert = st.session_state.attempts[cleaned] >= 3 or len(cleaned) > 100
                st.session_state.last_cipher, st.session_state.last_plain, st.session_state.last_padded = cipher, cleaned, padded
                st.session_state.history.append({"operation":"Encrypt", "input":cleaned, "output":cipher, "alert":alert})
                st.markdown('<div class="code-result"><div class="smallcaps">Encrypted output</div></div>', unsafe_allow_html=True)
                st.code(cipher, language=None)
                if padded: st.info("An X was added to complete the final pair.")
                if alert: st.warning("Rule-based alert: repeated message or unusually long input.")
            except ValueError as e:
                st.error(str(e))
    with right:
        st.markdown("### ◈ Encryption pipeline")
        st.markdown("""
        <div class="panel" style="margin-bottom:12px"><div style="display:flex;gap:14px;align-items:center"><div style="font-size:1.7rem;color:#A99CFF">01</div><div><b style="color:#F4F5FF">Normalize</b><div class="panel-note">Keep letters A–Z and group into pairs.</div></div></div></div>
        <div style="text-align:center;color:#56E0F0;font-size:1.2rem">↓</div>
        <div class="panel" style="margin:12px 0"><div style="display:flex;gap:14px;align-items:center"><div style="font-size:1.7rem;color:#A99CFF">02</div><div><b style="color:#F4F5FF">Matrix transform</b><div class="panel-note">Multiply each pair by the key matrix modulo 26.</div></div></div></div>
        <div style="text-align:center;color:#56E0F0;font-size:1.2rem">↓</div>
        <div class="panel" style="margin-top:12px"><div style="display:flex;gap:14px;align-items:center"><div style="font-size:1.7rem;color:#A99CFF">03</div><div><b style="color:#F4F5FF">Cipher output</b><div class="panel-note">Display the transformed message.</div></div></div></div>
        """, unsafe_allow_html=True)
    st.write("")
    st.markdown("### ◈ Key matrix")
    a, b, c = st.columns([1, 1, 1.4])
    with a:
        st.markdown('<div class="panel"><div class="smallcaps">Key</div><div class="panel-value" style="font-family:monospace;font-size:1.8rem;line-height:1.6">[ 3&nbsp; 3 ]<br>[ 2&nbsp; 5 ]</div></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="panel"><div class="smallcaps">Determinant</div><div class="panel-value">9 mod 26</div><div class="panel-note">GCD(9, 26) = 1</div></div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="panel"><div class="smallcaps">Method</div><div class="panel-value">Hill Cipher</div><div class="panel-note">Classroom demonstration only; not modern secure cryptography.</div></div>', unsafe_allow_html=True)

elif page == "Encrypt Message":
    st.markdown("### 🔐 Encrypt a message")
    st.write("Enter text to transform it into a matrix-based ciphertext.")
    with st.container(border=True):
        message = st.text_area("Plaintext", placeholder="Type a message, e.g. HELLO WORLD", height=160, key="encrypt_page_input")
        if st.button("⚡ Encrypt message", type="primary", use_container_width=True):
            try:
                cipher, padded, cleaned = encrypt_message(message)
                st.session_state.encrypt_count += 1
                st.session_state.attempts[cleaned] = st.session_state.attempts.get(cleaned, 0) + 1
                alert = st.session_state.attempts[cleaned] >= 3 or len(cleaned) > 100
                st.session_state.last_cipher, st.session_state.last_plain, st.session_state.last_padded = cipher, cleaned, padded
                st.session_state.history.append({"operation":"Encrypt", "input":cleaned, "output":cipher, "alert":alert})
                st.success("Encryption completed.")
                st.markdown("**Ciphertext output**")
                st.code(cipher, language=None)
                if padded: st.info("An X was added internally to complete the last letter pair.")
                if alert: st.warning("Rule-based security alert: repeated message or unusually long input.")
                with st.expander("View transformation details"):
                    st.code("Key matrix K = [[3, 3], [2, 5]]\nAlphabet mapping: A=0, B=1, ..., Z=25\nOperation: C = K × P (mod 26)", language="text")
            except ValueError as e:
                st.error(str(e))

elif page == "Decrypt Message":
    st.markdown("### 🔓 Decrypt a ciphertext")
    st.write("Paste ciphertext generated by this demo to reverse the matrix transformation.")
    default_cipher = st.session_state.last_cipher
    ciphertext = st.text_area("Ciphertext", value=default_cipher, placeholder="Enter an even number of letters", height=130, key="decrypt_page_input")
    remove_x = st.checkbox("Remove one trailing X if it was added as padding", value=False)
    if st.button("↩ Decrypt message", type="primary", use_container_width=True):
        try:
            plain = decrypt_message(ciphertext, remove_padding=remove_x)
            st.success("Decryption completed.")
            st.markdown("**Plaintext output**")
            st.code(plain, language=None)
            st.session_state.history.append({"operation":"Decrypt", "input":clean_text(ciphertext), "output":plain, "alert":False})
        except ValueError as e:
            st.error(str(e))
    st.caption("Spaces and punctuation are preserved in the displayed message. If encryption added an X for padding, select the checkbox above to remove it. A real final X can be ambiguous in this educational cipher.")

elif page == "Security Center":
    st.markdown("### 🛡️ Security center")
    st.write("A transparent, rule-based activity view for this demo session—not a trained AI detector.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total operations", len(st.session_state.history))
    c2.metric("Encryption attempts", st.session_state.encrypt_count)
    c3.metric("Flagged events", sum(1 for item in st.session_state.history if item.get("alert")))
    if st.session_state.history:
        st.markdown("#### Recent activity")
        st.dataframe([{"Operation":x["operation"], "Input":x["input"][:32], "Output":x["output"][:32], "Alert": "⚠️ Flagged" if x.get("alert") else "—"} for x in reversed(st.session_state.history[-20:])], use_container_width=True, hide_index=True)
    else:
        st.info("No activity yet. Encrypt a message to populate the session dashboard.")
    st.markdown("#### Rules being monitored")
    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<div class="panel"><div class="smallcaps">Rule 01</div><div class="panel-value">Repeated input</div><div class="panel-note">Flags the same normalized message after three or more encryption attempts.</div></div>', unsafe_allow_html=True)
    with r2:
        st.markdown('<div class="panel"><div class="smallcaps">Rule 02</div><div class="panel-value">Long input</div><div class="panel-note">Flags a normalized message containing more than 100 letters.</div></div>', unsafe_allow_html=True)
    if st.button("Clear session activity"):
        st.session_state.history = []
        st.session_state.attempts = {}
        st.session_state.encrypt_count = 0
        st.session_state.last_cipher = ""
        st.session_state.last_plain = ""
        st.session_state.last_padded = False
        st.rerun()

else:
    st.markdown("### ◈ About this project")
    st.markdown("""
    This mini project demonstrates how a classical matrix cipher can be wrapped in a modern-looking interactive dashboard.

    **Core concepts**
    - Alphabet-to-number mapping (`A = 0` through `Z = 25`)
    - 2×2 matrix multiplication modulo 26
    - Modular matrix inverse for decryption
    - Session-based rule monitoring for repeated and unusually long inputs

    **Important limitations**
    - The activity checks are rule-based and do not use a trained AI model.
    - The Hill Cipher is vulnerable to cryptanalysis and must not be used to protect real confidential information.
    - Session metrics are temporary and reset when the app session restarts.
    """)

st.markdown("---")
st.markdown("""
<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:#7984A7;font-size:.8rem">
  <span>◆ MATRIX AI CRYPTO <span style="color:#A99CFF">/</span> EDUCATIONAL PROTOTYPE</span>
  <span>Built with Python + Streamlit · No real secrets stored</span>
</div>
""", unsafe_allow_html=True)
