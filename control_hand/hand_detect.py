import cv2
import mediapipe as mp


class HandGestureDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.prev_thumb_state = False
        self.prev_index_state = False
        self.prev_middle_state = False
        self.prev_ring_state = False
        self.prev_pinky_state = False

    def is_thumb_open(self, hand_landmarks, thumb_tip_id, thumb_base_id, thumb_additional_id):
        tip = hand_landmarks.landmark[thumb_tip_id]
        base = hand_landmarks.landmark[thumb_base_id]
        additional = hand_landmarks.landmark[thumb_additional_id]
        print(tip, base, additional)

        return tip.y < base.y and additional.x < base.x

    def is_finger_open(self, hand_landmarks, finger_tip_id, finger_base_id):
        tip = hand_landmarks.landmark[finger_tip_id]
        base = hand_landmarks.landmark[finger_base_id]
        return tip.y < base.y

    def detect_gestures(self):
        while True:
            self.success, self.image = self.cap.read()
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    thumb_open = self.is_thumb_open(hand_landmarks, 4, 1, 1)
                    if thumb_open != self.prev_thumb_state:
                        print("Dedão:", "Aberto" if thumb_open else "Fechado")
                    self.prev_thumb_state = thumb_open

                    index_finger_open = self.is_finger_open(hand_landmarks, 8, 6)
                    if index_finger_open != self.prev_index_state:
                        print("Indicador:", "Aberto" if index_finger_open else "Fechado")
                    self.prev_index_state = index_finger_open

                    middle_finger_open = self.is_finger_open(hand_landmarks, 12, 9)
                    if middle_finger_open != self.prev_middle_state:
                        print("Médio:", "Aberto" if middle_finger_open else "Fechado")
                    self.prev_middle_state = middle_finger_open

                    ring_finger_open = self.is_finger_open(hand_landmarks, 16, 10)
                    if ring_finger_open != self.prev_ring_state:
                        print("Anelar:", "Aberto" if ring_finger_open else "Fechado")
                    self.prev_ring_state = ring_finger_open

                    pinky_open = self.is_finger_open(hand_landmarks, 20, 18)
                    if pinky_open != self.prev_pinky_state:
                        print("Mínimo:", "Aberto" if pinky_open else "Fechado")
                    self.prev_pinky_state = pinky_open

                    self.mpDraw.draw_landmarks(self.image, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

            cv2.imshow("Video", self.image)
            if cv2.waitKey(30) == 27:  # Break the loop when the ESC key is pressed.
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = HandGestureDetector()
    detector.detect_gestures()
