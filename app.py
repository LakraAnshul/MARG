# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st
from structures.streamlit_login_auth_ui.widgets import __login__
from structures.essentials import load_model

# Local Modules
import settings
import helper
from locales.settings_languages import COMPONENTS

# Setting page layout
st.set_page_config(
    page_title="M.A.R.G.",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Global CSS and theming (Arvo, dark/green gradient, green accent, glassmorphism)
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Arvo:ital,wght@0,400;0,700;1,400;1,700&display=swap');

:root {
  --bg-0: #0b0b0c;
  --bg-1: #121314;
  --bg-2: #151718;
  --fg: #e9edf1;
  --muted: #a8b0b8;
  --accent: #22c55e; /* green */
  --accent-contrast: #052e16;
  --card: rgba(255,255,255,0.05);
  --border: rgba(255,255,255,0.24);
  --shadow: 0 12px 40px rgba(0,0,0,0.32);
  --grad-1: #000000;
  --grad-2: #0a2a0f;
  --grad-3: #0f3a18;
}

html, body, [class^="css"], .main {
  font-family: 'Arvo', serif !important;
  color: var(--fg) !important;
  background: radial-gradient(1000px 800px at 10% 0%, var(--grad-2), transparent 60%),
              radial-gradient(1200px 900px at 90% 10%, var(--grad-3), transparent 60%),
              linear-gradient(160deg, var(--grad-1), var(--bg-0) 60%, var(--bg-2));
  background-attachment: fixed !important;
}

/* Reduce general vertical whitespace */
h1, h2, h3 { margin: 0.35rem 0 0.5rem 0; }
section { margin: 0; padding: 0; }

/* Links */
a { color: var(--accent) !important; text-decoration-color: rgba(34,197,94,0.5); }

/* Buttons */
.stButton button, .stDownloadButton button {
  background: linear-gradient(135deg, var(--accent), #16a34a);
  border: none; color: #ffffff; padding: 0.55rem 0.95rem; border-radius: 12px;
  box-shadow: var(--shadow);
  transition: transform 120ms ease, box-shadow 120ms ease, filter 200ms ease;
}
.stButton button:hover, .stDownloadButton button:hover { transform: translateY(-1px); filter: brightness(1.05); }

/* Sidebar glass + green accents */
section[data-testid="stSidebar"] > div:first-child {
  background: linear-gradient(180deg, rgba(5, 20, 10, 0.65), rgba(5, 20, 10, 0.25));
  border-right: 1px solid var(--border);
  backdrop-filter: blur(12px) saturate(120%);
  -webkit-backdrop-filter: blur(12px) saturate(120%);
}
section[data-testid="stSidebar"] .stButton button,
section[data-testid="stSidebar"] .stDownloadButton button { background: linear-gradient(135deg, var(--accent), #16a34a); }

/* REMOVING BORDER AROUND SELECTBOX AND RADIO FOR A CLEANER LOOK */
/* Targeting selectbox and radio containers inside the sidebar to remove the border */
section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb],
section[data-testid="stSidebar"] .stRadio > div,
section[data-testid="stSidebar"] .stCheckbox > div {
    background: var(--card);
    border: none !important; /* Force removal of border */
    border-radius: 12px;
    padding: 4px;
}

/* INPUT/TEXTAREA styling */
section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stNumberInput input,
section[data-testid="stSidebar"] .stTextArea textarea {
    background: rgba(255,255,255,0.06);
    border: 1px solid var(--border);
    color: var(--fg);
    border-radius: 12px;
}

/* SLIDER TRACK AND HANDLE TO GREEN */
section[data-testid="stSidebar"] .stSlider > div > div > div[role=slider] { background: var(--accent) !important; } /* Handle */
section[data-testid="stSidebar"] .stSlider > div > div > div:nth-of-type(2) { background: var(--accent) !important; } /* Track (filled portion) */

/* FIX FOR 100% HIGHLIGHT - Target the internal bar that might be using the accent color */
section[data-testid="stSidebar"] .stSlider > div > div > div > div:nth-of-type(2) {
    background: transparent !important; /* Ensures the percentage tooltip is transparent */
}


/* Force green accents for form controls globally */
:root { accent-color: var(--accent); }
input[type="checkbox"], input[type="radio"], select, textarea { accent-color: var(--accent) !important; }
.stCheckbox input, .stRadio input { accent-color: var(--accent) !important; }
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus { outline: 2px solid var(--accent); outline-offset: 1px; }

/* Glassmorphism card */
.glass-card {
  width: 240px; height: 360px; background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1),
              inset 0 1px 0 rgba(255, 255, 255, 0.5),
              inset 0 -1px 0 rgba(255, 255, 255, 0.1),
              inset 0 0 0px 0px rgba(255, 255, 255, 0);
  position: relative; overflow: hidden;
}
.glass-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent); }
.glass-card::after { content: ''; position: absolute; top: 0; left: 0; width: 1px; height: 100%; background: linear-gradient(180deg, rgba(255,255,255,0.8), transparent, rgba(255,255,255,0.3)); }

/* Flexible card variant */
.glass-flex { width: 100%; height: auto; padding: 18px; border-radius: 20px; }

/* Hero */
.hero { text-align: center; padding: 18px 12px; margin-bottom: 12px; }
.hero-title { font-weight: 800; letter-spacing: 3px; text-shadow: 0 6px 24px rgba(0,0,0,0.45); }
.hero-sub { color: var(--muted); margin-top: 4px; }

@keyframes float { 0% { transform: translateY(0); } 50% { transform: translateY(-4px); } 100% { transform: translateY(0); } }
</style>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR CONTENT START ---

# 1. Sidebar branding (centered, bold) - Increased font size (24px)
with st.sidebar:
    st.markdown(
        """
        <div style="width:100%;text-align:center;margin:6px 0 15px 0;">
          <span style="font-family:'Arvo',serif;font-weight:800;letter-spacing:2px;font-size:24px;background: linear-gradient(135deg, #a7f3d0, #22c55e); -webkit-background-clip: text; background-clip: text; color: transparent; text-shadow: 0 2px 6px rgba(34,197,94,0.22);">M.A.R.G.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 2. Language Selection (Top)
language = st.sidebar.selectbox(
    "Language: ",
    [
        "English",
        "ಕನ್ನಡ",
        "हिंदी",
        "বাংলা",
        "ગુજરાતી",
        "മലയാളം",
        "മराठी",
        "தமிழ்",
        "తెలుగు",
        "اردو",
        "ਪੰਜਾਬੀ",
        "സംസ്കൃത",
        "অসমীয়া",
        "भोजपुरी",
        "डोगरी",
        "मैथिली",
        "Mizo tawng",
        "Manipuri",
    ],
)
language_dict = {
    "English": "en",
    "हिंदी": "hi",
    "ಕನ್ನಡ": "kn",
    "অসমীয়া": "as",
    "বাংলা": "bn",
    "ગુજરાતી": "gu",
    "മലയാളം": "ml",
    "മराठी": "mr",
    "தமிழ்": "ta",
    "తెలుగు": "te",
    "اردו": "ur",
    "ਪੰਜਾਬੀ": "pa",
    "സംസ്കൃത": "sanskrit",
    "भोजपुरी": "bhojpuri",
    "डോഗਰੀ": "dogri",
    "मैथिली": "maithili",
    "Mizo tawng": "mizo",
    "Manipuri": "manipuri",
}

# Main App Header (outside sidebar)
st.markdown(
    """
    <div class="glass-card glass-flex hero" style="animation: float 5s ease-in-out infinite;">
      <h1 class="hero-title" style="font-size: clamp(28px, 5vw, 56px); margin: 0;">
        <span style="background: linear-gradient(135deg, #ffffff, #dcdcdc 60%); -webkit-background-clip: text; background-clip: text; color: transparent;">
          <b>M.A.R.G.</b>
        </span>
      </h1>
      <div class="hero-sub">Modern Analytics for Road Guidance</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Login UI initialization
__login__obj = __login__(
    auth_token="pk_prod_PVY78PYNS84M1SPFKZSCHD1D32BS",
    company_name="M.A.R.G.",
    width=200,
    height=250,
    logout_button_name=COMPONENTS[language_dict[language]]["LOGOUT"],
    hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url="https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json",
    language=language_dict[language],
)

LOGGED_IN = __login__obj.build_login_ui()


if LOGGED_IN == True:
    st.sidebar.markdown("---")  # Separator

    # 3. Model Configuration Group (Image/Video Config)
    st.sidebar.header(COMPONENTS[language_dict[language]]["CONFIGURATION"])
    helper.startup()  # Assuming this is a necessary startup call

    # Model Options: Using selectbox (dropdown)
    model_options = [
        COMPONENTS[language_dict[language]]["DETECTION"],
        COMPONENTS[language_dict[language]]["SEGMENTATION"],
    ]
    model_type = st.sidebar.selectbox(
        COMPONENTS[language_dict[language]]["MODEL_TYPE"], options=model_options
    )

    # Confidence Slider
    confidence = (
        float(
            st.sidebar.slider(
                COMPONENTS[language_dict[language]]["CONFIDENCE"], 25, 100, 40
            )
        )
        / 100
    )

    # Selecting Detection Or Segmentation
    if model_type == COMPONENTS[language_dict[language]]["DETECTION"]:
        model_path = Path(settings.DETECTION_MODEL)
    elif model_type == COMPONENTS[language_dict[language]]["SEGMENTATION"]:
        model_path = Path(settings.SEGMENTATION_MODEL)

    # Load Pre-trained ML Model
    try:
        model = load_model(model_path)
    except Exception as ex:
        st.error(COMPONENTS[language_dict[language]]["LOAD_ERROR"] + str(model_path))
        st.error(ex)

    st.sidebar.markdown("---")  # Separator

    # 4. Source/Content Configuration Group (Configuration)
    st.sidebar.header(COMPONENTS[language_dict[language]]["CONFIG_SUBTITLE"])

    # Source Selection: Using selectbox (dropdown)
    source_options = [
        COMPONENTS[language_dict[language]]["IMAGE"],
        COMPONENTS[language_dict[language]]["VIDEO"],
        COMPONENTS[language_dict[language]]["RTSP"],
        COMPONENTS[language_dict[language]]["YOUTUBE"],
        COMPONENTS[language_dict[language]]["ENCROACHMENT"],
        COMPONENTS[language_dict[language]]["JUNCTION"],
        COMPONENTS[language_dict[language]]["JUNCTIONEVAL"],
        COMPONENTS[language_dict[language]]["BENCHMARKING"],
        "Analyze",
    ]
    source_radio = st.sidebar.selectbox(
        COMPONENTS[language_dict[language]]["SELECT_SOURCE"], options=source_options
    )

    source_img = None
    # If image is selected
    if source_radio == COMPONENTS[language_dict[language]]["IMAGE"]:
        source_img = st.sidebar.file_uploader(
            COMPONENTS[language_dict[language]]["SOURCE_IMG"],
            type=("jpg", "jpeg", "png", "bmp", "webp"),
        )

        col1, col2 = st.columns(2)

        with col1:
            try:
                if source_img is None:
                    default_image_path = str(settings.DEFAULT_IMAGE)
                    default_image = PIL.Image.open(default_image_path)
                    st.image(
                        default_image_path,
                        caption="Default Image",
                        use_column_width=True,
                    )
                else:
                    uploaded_image = PIL.Image.open(source_img)
                    st.image(
                        source_img, caption="Uploaded Image", use_column_width=True
                    )
            except Exception as ex:
                st.error(COMPONENTS[language_dict[language]]["IMG_ERROR"])
                st.error(ex)

        with col2:
            if source_img is None:
                default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
                default_detected_image = PIL.Image.open(default_detected_image_path)
                st.image(
                    default_detected_image_path,
                    caption="Detected Image",
                    use_column_width=True,
                )
            else:
                if st.sidebar.button(COMPONENTS[language_dict[language]]["DETECT_OBJ"]):
                    res = model.predict(uploaded_image, conf=confidence)
                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(
                        res_plotted, caption="Detected Image", use_column_width=True
                    )
                    try:
                        with st.expander(
                            COMPONENTS[language_dict[language]]["DETECTION_RES"]
                        ):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as ex:
                        # st.write(ex)
                        st.write(COMPONENTS[language_dict[language]]["NO_IMG"])

    elif source_radio == COMPONENTS[language_dict[language]]["VIDEO"]:
        helper.play_stored_video(confidence, model, language_dict[language])

    elif source_radio == COMPONENTS[language_dict[language]]["RTSP"]:
        helper.play_rtsp_stream(confidence, model, language_dict[language])

    elif source_radio == COMPONENTS[language_dict[language]]["YOUTUBE"]:
        helper.play_youtube_video(confidence, model, language_dict[language])

    elif source_radio == COMPONENTS[language_dict[language]]["ENCROACHMENT"]:
        helper.enchroachment(confidence, language_dict[language])

    elif source_radio == COMPONENTS[language_dict[language]]["JUNCTION"]:
        helper.junctionEvaluationDataset(language_dict[language])

    elif source_radio == COMPONENTS[language_dict[language]]["JUNCTIONEVAL"]:
        helper.junctionEvaluation(language_dict[language])

    elif source_radio == COMPONENTS[language_dict[language]]["BENCHMARKING"]:
        helper.benchMarking(confidence, language_dict[language])
    elif source_radio == "Analyze":
        helper.Analyze(language_dict[language])
    else:
        st.error("Please select a valid source type!")
