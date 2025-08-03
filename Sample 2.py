import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# screen size
screen_w, screen_h = pyautogui.size()

mouse_held = False
last_click_time = 0
click_interval = 0.25  # seconds

#previous position to compare movement
prev_x, prev_y = 0, 0
movement_threshold = 100  #movement pixel

def is_closed(landmarks):
    fingers = [8,12,16,20]
    knuckle = [5,9,13,17]
    for tips, base in zip(fingers, knuckle):
        if landmarks[tips].y < landmarks[base].y:
            return False
    return True

def is_open(landmarks):
    fingers = [8,12,16,20]
    knuckle = [5,9,13,17]
    for tips, base in zip(fingers, knuckle):
        if landmarks[tips].y > landmarks[base].y:
            return False
    return True

# smooth_x, smooth_y = 0, 0
# smoothing_factor = 0.2

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    now = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            x = int(lm[8].x * w)
            y = int(lm[8].y * h)
            screen_x = int(lm[8].x * screen_w)
            screen_y = int(lm[8].y * screen_h)

            pyautogui.moveTo(screen_x, screen_y)

            # smooth_x = smooth_x + (screen_x - smooth_x) * smoothing_factor
            # smooth_y = smooth_y + (screen_y - smooth_y) * smoothing_factor
            # pyautogui.moveTo(int(smooth_x), int(smooth_y))

            cv2.circle(img, (x, y), 10, (255, 0, 255), -1)

            if is_closed(lm):
                cv2.putText(img, "Fist", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                if not mouse_held and (now - last_click_time > click_interval):
                    pyautogui.mouseDown(button='right')
                    mouse_held = True
                    last_click_time = now
            elif is_open(lm):
                cv2.putText(img, "Open Palm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                if mouse_held:
                    pyautogui.mouseUp(button='right')
                    mouse_held = False

            #for Keyboard
            dx = x - prev_x
            dy = y - prev_y

            # if abs(dx) > abs(dy):
            #     if dx > movement_threshold:
            #         pyautogui.press('right')
            #         cv2.putText(img, "Right", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
            #     elif dx < -movement_threshold:
            #         pyautogui.press('left')
            #         cv2.putText(img, "Left", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
            # else:
            #     if dy > movement_threshold:
            #         pyautogui.press('down')
            #         cv2.putText(img, "Down", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
            #     elif dy < -movement_threshold:
            #         pyautogui.press('up')
            #         cv2.putText(img, "Up", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

            #update previous coordinates
            prev_x, prev_y = x, y

    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
