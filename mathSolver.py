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

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Gesture Based Math Solver",
    page_icon="✋",
    layout="wide"
)

st.title("✋ Gesture Based Math Solver")
st.write("Use your hand gestures to create mathematical expressions.")

# ---------------- MEDIAPIPE ----------------
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


@st.cache_resource
def get_hands():
    return mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )


hands = get_hands()


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
            1 if hand_landmarks.landmark[tip_ids[0]].x >
            hand_landmarks.landmark[tip_ids[0] - 1].x
            else 0
        )
    else:
        fingers.append(
            1 if hand_landmarks.landmark[tip_ids[0]].x <
            hand_landmarks.landmark[tip_ids[0] - 1].x
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


def detectGesture(hand1_data, hand2_data):

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


# ---------------- SESSION STATE ----------------

if "expression" not in st.session_state:
    st.session_state.expression = ""

if "result" not in st.session_state:
    st.session_state.result = ""


# ---------------- UI ----------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Expression")
    st.info(st.session_state.expression)

with col2:
    st.subheader("Result")
    st.success(st.session_state.result)


# ---------------- BUTTONS ----------------

button_col1, button_col2 = st.columns(2)

with button_col1:
    if st.button("🗑 Clear Expression"):
        st.session_state.expression = ""
        st.session_state.result = ""
        st.rerun()

with button_col2:
    if st.button("🧮 Calculate"):
        try:
            st.session_state.result = str(
                eval(st.session_state.expression)
            )
        except:
            st.session_state.result = "Error"

        st.rerun()


st.divider()

st.subheader("📷 Camera")

camera_image = st.camera_input(
    "Show your hand gesture to the camera"
)


# ---------------- PROCESS IMAGE ----------------

if camera_image is not None:

    file_bytes = np.asarray(
        bytearray(camera_image.read()),
        dtype=np.uint8
    )

    image = cv.imdecode(
        file_bytes,
        cv.IMREAD_COLOR
    )

    image = cv.flip(image, 1)

    img_rgb = cv.cvtColor(
        image,
        cv.COLOR_BGR2RGB
    )

    result = hands.process(img_rgb)

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

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


        # -------- ONE HAND --------

        if len(hand_data) == 1:

            hand_landmarks, label = hand_data[0]

            fingers_up = count_fingers(
                hand_landmarks,
                label
            )

            if fingers_up in [0, 1, 2, 3, 4, 5]:

                st.session_state.expression += str(
                    fingers_up
                )

                st.success(
                    f"Detected Number: {fingers_up}"
                )


        # -------- TWO HANDS --------

        elif len(hand_data) == 2:

            gesture = detectGesture(
                hand_data[0],
                hand_data[1]
            )

            if gesture == "clear":

                st.session_state.expression = ""
                st.session_state.result = ""

                st.success("Expression Cleared")


            elif gesture == "del":

                st.session_state.expression = \
                    st.session_state.expression[:-1]

                st.success("Last Character Deleted")


            elif gesture == "=":

                try:
                    st.session_state.result = str(
                        eval(
                            st.session_state.expression
                        )
                    )

                except:
                    st.session_state.result = "Error"

                st.success(
                    f"Result: {st.session_state.result}"
                )


            elif gesture == "exit":

                st.warning("Gesture session stopped")


            elif gesture:

                st.session_state.expression += gesture

                st.success(
                    f"Detected: {gesture}"
                )


    else:

        st.warning("No hands detected")


    # Display processed image

    image_rgb = cv.cvtColor(
        image,
        cv.COLOR_BGR2RGB
    )

    st.image(
        image_rgb,
        caption="Processed Image",
        use_container_width=True
    )


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
