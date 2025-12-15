import cv2
import math
import numpy as np
import streamlit as st
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL, CoInitialize
from comtypes.client import CreateObject
from pycaw.pycaw import IAudioEndpointVolume, IMMDeviceEnumerator


st.set_page_config(layout="wide", page_title="Hand Gesture Mic Control")

# --- Apple-like UI CSS ---
st.markdown(
        """
        <style>
        :root{
            --apple-bg: #F5F7FB;
            --card-bg: rgba(255,255,255,0.85);
            --muted: #6b7280;
            --accent: #007aff;
            --radius: 14px;
            --glass: rgba(255,255,255,0.6);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
        }
        html, body, .stApp {
            background: var(--apple-bg) !important;
            color: #0b1220;
            font-family: inherit !important;
        }
        /* Card-like containers */
        .app-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(250,250,250,0.9));
            border-radius: var(--radius);
            padding: 18px;
            box-shadow: 0 6px 20px rgba(15,23,42,0.06);
            border: 1px solid rgba(15,23,42,0.04);
        }
        /* Sidebar tweaks */
        .css-1d391kg .css-1l02c9k {border-radius: var(--radius);} /* best-effort selectors */
        .stSidebar .stButton>button, .stButton>button{
            border-radius: 10px;
            padding: 10px 14px;
            background: linear-gradient(180deg, rgba(255,255,255,0.6), rgba(245,245,245,0.6));
            border: 1px solid rgba(11,18,32,0.06);
            color: #0b1220;
            box-shadow: 0 3px 8px rgba(11,18,32,0.04);
        }
        .stMetric>div>div>div{font-weight:600}
        h1.apple-title{font-size:34px;margin:0;color:#0b1220}
        p.apple-sub{color:var(--muted);margin:4px 0 12px}
        .status-pill{display:inline-block;padding:6px 10px;border-radius:999px;background:var(--glass);border:1px solid rgba(11,18,32,0.04);color:var(--muted);}
        </style>
        """,
        unsafe_allow_html=True,
)

# --- UPDATED TUNING PARAMETERS ---
# Ratio = (Thumb-Index Distance) / (Wrist-MiddleKnuckle Distance)
PINCH_RATIO_THRESHOLD = 0.15   # MUTE if ratio is below 0.1
MIN_RATIO = 0.15              # 0% Volume starts at ratio 0.1
MAX_RATIO = 1.5               # 100% Volume at ratio 2.0
SMOOTHING = 3                 # Smoothing factor

# Load MediaPipe (Optimized for Speed)
@st.cache_resource
def load_mediapipe():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        model_complexity=0,      # "Lite" model for lowest latency
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    mp_draw = mp.solutions.drawing_utils
    return hands, mp_draw

hands, mp_draw = load_mediapipe()

# --- AUDIO SETUP ---
def get_mic_interface():
    try:
        CoInitialize()
        CLSID_MMDeviceEnumerator = "{BCDE0395-E52F-467C-8E3D-C4579291692E}"
        enumerator = CreateObject(CLSID_MMDeviceEnumerator, interface=IMMDeviceEnumerator)
        device = enumerator.GetDefaultAudioEndpoint(1, 0) # 1=Mic
        interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))
    except:
        return None

# 2. SIDEBAR

with st.sidebar:
    st.header("Settings")
    cam_index = st.selectbox("Select Camera Index", [0, 1, 2], index=0)
    st.header("Manual Controls")
    
    def manual_change(change):
        vc = get_mic_interface()
        if vc:
            try:
                curr = vc.GetMasterVolumeLevelScalar()
                vc.SetMasterVolumeLevelScalar(min(max(curr + change, 0.0), 1.0), None)
            except: pass
            
    col_b1, col_b2 = st.columns(2)
    if col_b1.button("Vol +20%"): manual_change(0.2)
    if col_b2.button("Vol -20%"): manual_change(-0.2)

# 3. HEADER & LAYOUT

st.markdown(
        """
        <div class="app-card">
            <h1 class="apple-title">Microphone</h1>
            <p class="apple-sub">Infosys SpringBoard - Volume Control Using Hand Gestures </p>
            <div style="display:flex;gap:10px;align-items:center">
                <div class="status-pill">TEAM D</div>
                <div style="color:var(--muted);font-size:15px">Mentor:<b> Dr. D. BHANU PRAKASH<b></div>
                 <div style="color:var(--muted);font-size:13px">Team: Anusuya, Prashanti, Shreyas, Siva Sankar</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("Interface")
    if 'run_camera' not in st.session_state:
        st.session_state.run_camera = False

    def toggle_camera_state():
        st.session_state.run_camera = not st.session_state.run_camera

    btn_text = "STOP CAMERA" if st.session_state.run_camera else "START CAMERA"
    st.button(btn_text, on_click=toggle_camera_state, type="primary")

    st.markdown("### Real Time Status")
    vol_metric = st.empty()
    dist_metric = st.empty()
    status_msg = st.empty()

    if not st.session_state.run_camera:
        status_msg.info("Camera is OFF.")

with col2:
    st.subheader("Live Camera Feed")
    video_container = st.empty()


# 4. HIGH-PERFORMANCE LOOP

if st.session_state.run_camera:
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        st.error("Could Not Open Camera.")
        st.session_state.run_camera = False
    else:
        # Get Audio Interface ONCE
        vc = get_mic_interface()
        
        while st.session_state.run_camera:
            ret, frame = cap.read()
            if not ret: break
            
            # Preprocessing
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Inference
            results = hands.process(rgb_frame)
            
            current_ratio = 0.0
            is_pinched = False
            
            if results.multi_hand_landmarks:
                for hand_lms in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)
                    
                    # Landmarks for Scale Invariant Calculation
                    p4 = hand_lms.landmark[4]  # Thumb Tip
                    p8 = hand_lms.landmark[8]  # Index Tip
                    p0 = hand_lms.landmark[0]  # Wrist
                    p9 = hand_lms.landmark[9]  # Middle Finger MCP (Knuckle)

                    # 1. Calculate Pinch Distance (Thumb to Index)
                    pinch_dist = math.hypot(p8.x - p4.x, p8.y - p4.y)
                    
                    # 2. Calculate Reference Scale (Wrist to Middle Knuckle)
                    scale_dist = math.hypot(p9.x - p0.x, p9.y - p0.y)
                    
                    # 3. Calculate Ratio
                    if scale_dist < 0.01: scale_dist = 0.01
                    ratio = pinch_dist / scale_dist
                    current_ratio = ratio

                    # Visuals
                    x1, y1 = int(p4.x * w), int(p4.y * h)
                    x2, y2 = int(p8.x * w), int(p8.y * h)
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    
                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    if vc:
                        try:
                            # --- LOGIC: PINCH (MUTE) vs VOLUME ---
                            if ratio <= PINCH_RATIO_THRESHOLD:
                                # MUTE
                                cv2.circle(frame, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
                                cv2.putText(frame, "MUTE STATE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                                
                                if not vc.GetMute():
                                    vc.SetMute(1, None)
                                is_pinched = True
                            else:
                                # UNMUTE & ADJUST VOLUME
                                if vc.GetMute():
                                    vc.SetMute(0, None)
                                is_pinched = False
                                
                                # Map Ratio to Volume
                                # [0.1, 2.0] -> [0, 100]
                                vol_per = np.interp(ratio, [MIN_RATIO, MAX_RATIO], [0, 100])
                                vol_per = SMOOTHING * round(vol_per / SMOOTHING)
                                vc.SetMasterVolumeLevelScalar(vol_per / 100, None)
                        except: pass

            # Update UI
            if vc:
                try:
                    curr_vol = int(vc.GetMasterVolumeLevelScalar() * 100)
                    vol_metric.metric("Mic Volume:", f"{curr_vol}%")
                except: pass
            
            dist_metric.metric("Gesture Ratio:", f"{current_ratio:.2f}")
            
            if is_pinched:
                status_msg.error("MICROPHONE IN  MUTE  STATE")
            else:
                status_msg.success("MICROPHONE IN UNMUTED STATE")

            # Display Video
            video_container.image(frame, channels="BGR", width=650)

        cap.release()
        cv2.destroyAllWindows()

        st.write("Stopped.")

