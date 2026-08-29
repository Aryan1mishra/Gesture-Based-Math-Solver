# import cv2 as cv
# import mediapipe as mp
# import numpy as np
# import time

# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7,
#     min_tracking_confidence=0.7)

# # distance between two points
# def euclidean_distance(p1, p2):
#     return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# #gestures for different operations
# def detectGesture(hand1_data, hand2_data):
#     (hand1, label1), (hand2, label2) = hand1_data, hand2_data
#     f1 = count_fingers(hand1, label1)
#     f2 = count_fingers(hand2, label2)
#     dist = euclidean_distance(hand1.landmark[8], hand2.landmark[8])
#     if f1==1 and f2==1:
#         if dist < 0.06:
#             return "exit"
#         return "+"
#     elif (f1==1 and f2==2) or (f1==2 and f2==1):
#         return "-"
#     elif (f1==1 and f2==3) or (f1==3 and f2==1):
#         return "*"
#     elif (f1==1 and f2==4) or (f1==4 and f2==1):
#         return "/"
#     elif (f1==2 and f2==2):
#         return "del"
#     elif (f1+f2==6):
#         return "6"
#     elif (f1+f2==7):
#         return "7"
#     elif (f1+f2==8):
#         return "8"
#     elif (f1+f2==9):
#         return "9"
#     elif f1==0 and f2==0:
#         return "="
#     elif f1==5 and f2==5:
#         return "clear"
#     return None

# #counting fingers are up
# def count_fingers(hand_landmarks, label):
#     tip_ids = [4,8,12,16,20]
#     fingers = []
#     if label=="Left":
#         fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0]-1].x else 0)
#     else:
#         fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0]-1].x else 0)
#     for ids in range(1,5):
#         if hand_landmarks.landmark[tip_ids[ids]].y < hand_landmarks.landmark[tip_ids[ids]-2].y:
#             fingers.append(1)
#         else:
#             fingers.append(0)
#     return fingers.count(1)

# #Initialising variables
# last_finger_count = None
# last_update_time = 0
# delay = 1.25
# expression=""
# res=""

# # webcam input:
# cap = cv.VideoCapture(0)
# while True:
#     success, image = cap.read()
#     image = cv.flip(image, 1)
#     img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#     result = hands.process(img_rgb)
#     current_time = time.time()
#     hand_data=[]
    
#     #Reading hand data and mapping it on the screen
#     if result.multi_hand_landmarks and result.multi_handedness:
#         for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
#             label = hand_handedness.classification[0].label
#             hand_data.append((hand_landmarks,label))
#             mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
#         #Reading single and multi-hand data   
#         if len(hand_data)==1:
#             hand_landmarks, label = hand_data[0]
#             fingers_up = count_fingers(hand_landmarks, label)
#             if fingers_up in [0, 1, 2, 3, 4, 5] and current_time - last_update_time > delay:
#                 expression += str(fingers_up)
#                 last_update_time = current_time
#                 last_finger_count = fingers_up
        
#         if len(hand_data)==2:
#             gesture = detectGesture(hand_data[0], hand_data[1])
            
#             #Clearing the screen
#             if gesture=="clear":
#                 expression = ""
#                 res = ""
            
#             #Exitting the window after 'x' sign
#             if gesture == "exit":
#                 break 
            
#             #Evaluating the result
#             if gesture and current_time - last_update_time > delay:
                
#                 if gesture == "del":
#                     expression = expression[:-1]
#                     last_update_time = current_time
                    
#                 elif gesture=="=":
#                     try:
#                         res = str(eval(expression))
#                         print("Result:", res)
#                     except:
#                         res = "Error"
#                     last_update_time = current_time
#                 else:
#                     expression+=gesture
#                     last_update_time = current_time
     
#     #Displaying the expression and result   
#     cv.putText(image, f'Expr: {expression}', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
#     cv.putText(image, f'Result: {res}', (10, 100), cv.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 2)
#     cv.imshow("Math Solver", image)
#     key = cv.waitKey(1) & 0xFF
#     if key == ord('q') or key == 27:
#         break
#     elif key == ord('c'):
#         expression=""
#         res=""
        
# #Releasing resources and closing the windows
# cap.release()
# cv.destroyAllWindows()

import streamlit as st
import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import av

from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    WebRtcMode,
    RTCConfiguration,
   
)


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Gesture Based Math Solver",
    page_icon="✋",
    layout="wide"
)

st.title("✋ Gesture Based Math Solver")
st.write("Real-Time Gesture Based Mathematical Expression Solver")


# ---------------- SESSION STATE ----------------

if "expression" not in st.session_state:
    st.session_state.expression = ""

if "result" not in st.session_state:
    st.session_state.result = ""


# ---------------- FUNCTIONS ----------------

def euclidean_distance(p1, p2):
    return np.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


def count_fingers(hand_landmarks, label):

    tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if label == "Left":
        fingers.append(
            1 if hand_landmarks.landmark[4].x >
            hand_landmarks.landmark[3].x
            else 0
        )
    else:
        fingers.append(
            1 if hand_landmarks.landmark[4].x <
            hand_landmarks.landmark[3].x
            else 0
        )

    # Other fingers
    for ids in range(1, 5):

        if hand_landmarks.landmark[tip_ids[ids]].y < \
                hand_landmarks.landmark[tip_ids[ids] - 2].y:

            fingers.append(1)

        else:
            fingers.append(0)

    return fingers.count(1)


def detect_gesture(hand1_data, hand2_data):

    (hand1, label1), (hand2, label2) = hand1_data, hand2_data

    f1 = count_fingers(hand1, label1)
    f2 = count_fingers(hand2, label2)

    dist = euclidean_distance(
        hand1.landmark[8],
        hand2.landmark[8]
    )

    if f1 == 1 and f2 == 1:

        if dist < 0.06:
            return "exit"

        return "+"

    elif (f1 == 1 and f2 == 2) or (f1 == 2 and f2 == 1):
        return "-"

    elif (f1 == 1 and f2 == 3) or (f1 == 3 and f2 == 1):
        return "*"

    elif (f1 == 1 and f2 == 4) or (f1 == 4 and f2 == 1):
        return "/"

    elif f1 == 2 and f2 == 2:
        return "del"

    elif f1 + f2 == 6:
        return "6"

    elif f1 + f2 == 7:
        return "7"

    elif f1 + f2 == 8:
        return "8"

    elif f1 + f2 == 9:
        return "9"

    elif f1 == 0 and f2 == 0:
        return "="

    elif f1 == 5 and f2 == 5:
        return "clear"

    return None


# ---------------- VIDEO PROCESSOR ----------------

class GestureProcessor(VideoProcessorBase):

    def __init__(self):

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.expression = ""
        self.result_text = ""

        self.last_update_time = 0
        self.delay = 1.25


    def recv(self, frame):

        image = frame.to_ndarray(format="bgr24")

        # Mirror image
        image = cv.flip(image, 1)

        img_rgb = cv.cvtColor(
            image,
            cv.COLOR_BGR2RGB
        )

        result = self.hands.process(img_rgb)

        current_time = time.time()

        hand_data = []

        if (
            result.multi_hand_landmarks
            and result.multi_handedness
        ):

            for hand_landmarks, hand_handedness in zip(
                result.multi_hand_landmarks,
                result.multi_handedness
            ):

                label = hand_handedness.classification[0].label

                hand_data.append(
                    (hand_landmarks, label)
                )

                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )


            # -------- ONE HAND --------

            if len(hand_data) == 1:

                hand_landmarks, label = hand_data[0]

                fingers_up = count_fingers(
                    hand_landmarks,
                    label
                )

                if (
                    fingers_up in [0, 1, 2, 3, 4, 5]
                    and current_time - self.last_update_time > self.delay
                ):

                    self.expression += str(fingers_up)

                    self.last_update_time = current_time


            # -------- TWO HANDS --------

            elif len(hand_data) == 2:

                gesture = detect_gesture(
                    hand_data[0],
                    hand_data[1]
                )

                if (
                    gesture
                    and current_time - self.last_update_time > self.delay
                ):

                    if gesture == "clear":

                        self.expression = ""
                        self.result_text = ""


                    elif gesture == "del":

                        self.expression = self.expression[:-1]


                    elif gesture == "=":

                        try:
                            self.result_text = str(
                                eval(self.expression)
                            )

                        except Exception:
                            self.result_text = "Error"


                    elif gesture == "exit":

                        pass


                    else:

                        self.expression += gesture


                    self.last_update_time = current_time


        # -------- DISPLAY TEXT --------

        cv.putText(
            image,
            f"Expr: {self.expression}",
            (20, 50),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

        cv.putText(
            image,
            f"Result: {self.result_text}",
            (20, 100),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )
#--------------------------------------------------------------
#                Configuration + streamer       

RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": [
                    "stun:stun.l.google.com:19302"
                ]
            }
        ]
    }
)

st.subheader("📷 Live Camera")

ctx = webrtc_streamer(
    key="gesture-math-solver",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=GestureProcessor,
    media_stream_constraints={
        "video": {
            "width": {"ideal": 640},
            "height": {"ideal": 480},
            "frameRate": {"ideal": 15}
        },
        "audio": False,
    },
    async_processing=True,
)

# ---------------- CONTROLS ----------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button("🗑 Clear Expression"):

        if ctx.video_processor:

            ctx.video_processor.expression = ""
            ctx.video_processor.result_text = ""


with col2:

    if st.button("🧮 Calculate"):

        if ctx.video_processor:

            try:

                ctx.video_processor.result_text = str(
                    eval(ctx.video_processor.expression)
                )

            except Exception:

                ctx.video_processor.result_text = "Error"


# ---------------- INSTRUCTIONS ----------------

st.divider()

st.subheader("Gesture Instructions")

st.markdown("""
### Single Hand

| Fingers | Input |
|---|---|
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 5 |

### Two Hands

| Gesture | Operation |
|---|---|
| 1 + 1 | Addition (+) |
| 1 + 2 | Subtraction (-) |
| 1 + 3 | Multiplication (*) |
| 1 + 4 | Division (/) |
| 2 + 2 | Delete |
| Both Closed | Calculate (=) |
| Both Open | Clear |
""")
