import cv2
import mediapipe as mp

def is_finger_open(hand_landmarks, finger_tip_id, finger_base_id):
    tip = hand_landmarks.landmark[finger_tip_id]
    base = hand_landmarks.landmark[finger_base_id]
    return tip.y < base.y

def main():
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    # Inicializar o estado anterior dos dedos como fechado
    prev_thumb_state = False
    prev_index_state = False
    prev_middle_state = False
    prev_ring_state = False
    prev_pinky_state = False

    while True:
        success, image = cap.read()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dedão
                thumb_open = is_finger_open(hand_landmarks, 18, 2)
                if thumb_open != prev_thumb_state:
                    print("Dedão:", "Aberto" if thumb_open else "Fechado")
                prev_thumb_state = thumb_open

                # Indicador
                index_finger_open = is_finger_open(hand_landmarks, 8, 6)
                if index_finger_open != prev_index_state:
                    print("Indicador:", "Aberto" if index_finger_open else "Fechado")
                prev_index_state = index_finger_open

                # Médio
                middle_finger_open = is_finger_open(hand_landmarks, 12, 9)
                if middle_finger_open != prev_middle_state:
                    print("Médio:", "Aberto" if middle_finger_open else "Fechado")
                prev_middle_state = middle_finger_open

                # Anelar
                ring_finger_open = is_finger_open(hand_landmarks, 16, 10)
                if ring_finger_open != prev_ring_state:
                    print("Anelar:", "Aberto" if ring_finger_open else "Fechado")
                prev_ring_state = ring_finger_open

                # Mínimo
                pinky_open = is_finger_open(hand_landmarks, 20, 18)
                if pinky_open != prev_pinky_state:
                    print("Mínimo:", "Aberto" if pinky_open else "Fechado")
                prev_pinky_state = pinky_open

                mpDraw.draw_landmarks(image, hand_landmarks, mpHands.HAND_CONNECTIONS)

        cv2.imshow("Video", image)
        if cv2.waitKey(30) == 27:  # Quebra o loop quando a tecla ESC é pressionada.
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
