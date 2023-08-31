import cv2
import mediapipe as mp
import math


class AngleHandDetector:
    def __init__(self):
        self.mpDraw = None
        self.results = None
        self.image_rgb = None
        self.image = None
        self.success = None
        self.cap = None
        self.hands = None
        self.prev_thumb_state = False
        self.prev_index_state = False
        self.prev_middle_state = False
        self.prev_ring_state = False
        self.prev_pinky_state = False
        self.dedao_angulo = 0
        self.indicador_angulo = 0
        self.medio_angulo = 0
        self.anelar_angulo = 0
        self.minimo_angulo = 0

    def obter_centro_imagem(self, largura, altura):
        self.centro_x = largura // 2
        self.centro_y = altura // 2
        return self.centro_x, self.centro_y

    # Tamanho da região de interesse (ROI) no centro da imagem

    def iniciar_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands()

    def obter_frame(self):
        self.success, self.image = self.cap.read()
        altura, largura, _ = self.image.shape
        centro_x, centro_y = self.obter_centro_imagem(largura, altura)
        roi_width = 320
        roi_height = 240
        x1 = centro_x - roi_width // 2
        y1 = centro_y - roi_height // 2
        x2 = x1 + roi_width
        y2 = y1 + roi_height
        self.image = self.image[y1:y2, x1:x2]
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(self.image_rgb)
        self.mpDraw = mp.solutions.drawing_utils

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Dedão (passando o índice adicional 1 para o ponto do dedão)
                thumb_open = self.is_thumb_open(hand_landmarks, 4, 1, 1)
                # if thumb_open != self.prev_thumb_state:
                #     print("Dedão:", "Aberto" if thumb_open else "Fechado")
                # prev_thumb_state = thumb_open

                # Indicador
                index_finger_open = self.is_finger_open(hand_landmarks, 8, 6)
                # if index_finger_open != self.prev_index_state:
                #     print("Indicador:", "Aberto" if index_finger_open else "Fechado")
                # prev_index_state = index_finger_open

                # Médio
                middle_finger_open = self.is_finger_open(hand_landmarks, 12, 9)
                # if middle_finger_open != self.prev_middle_state:
                #     print("Médio:", "Aberto" if middle_finger_open else "Fechado")
                # prev_middle_state = middle_finger_open

                # Anelar
                ring_finger_open = self.is_finger_open(hand_landmarks, 16, 10)
                # if ring_finger_open != self.prev_ring_state:
                #     print("Anelar:", "Aberto" if ring_finger_open else "Fechado")
                # prev_ring_state = ring_finger_open

                # Mínimo
                pinky_open = self.is_finger_open(hand_landmarks, 20, 18)
                # if pinky_open != self.prev_pinky_state:
                #     print("Mínimo:", "Aberto" if pinky_open else "Fechado")
                # prev_pinky_state = pinky_open

                self.mpDraw.draw_landmarks(self.image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                # Calcular e exibir os ângulos de fechamento dos dedos
                if len(hand_landmarks.landmark) >= 21:
                    # Dedão
                    self.dedao_angulo = self.calculate_angle(hand_landmarks.landmark[3], hand_landmarks.landmark[4])

                    # Indicador
                    self.indicador_angulo = self.calculate_angle(hand_landmarks.landmark[7], hand_landmarks.landmark[8])

                    # Médio
                    self.medio_angulo = self.calculate_angle(hand_landmarks.landmark[11], hand_landmarks.landmark[12])

                    # Anelar
                    self.anelar_angulo = self.calculate_angle(hand_landmarks.landmark[15], hand_landmarks.landmark[16])

                    # Mínimo
                    self.minimo_angulo = self.calculate_angle(hand_landmarks.landmark[19], hand_landmarks.landmark[20])

        return self.image

    @staticmethod
    def is_thumb_open(hand_landmarks, thumb_tip_id, thumb_base_id, thumb_additional_id):
        tip = hand_landmarks.landmark[thumb_tip_id]
        base = hand_landmarks.landmark[thumb_base_id]
        additional = hand_landmarks.landmark[thumb_additional_id]

        # Comparar a posição vertical (eixo y) do dedão em relação à base
        # e também a posição horizontal (eixo x) do ponto adicional em relação à base
        return tip.y < base.y and additional.x < base.x

    @staticmethod
    def is_finger_open(hand_landmarks, finger_tip_id, finger_base_id):
        tip = hand_landmarks.landmark[finger_tip_id]
        base = hand_landmarks.landmark[finger_base_id]
        return tip.y < base.y

    @staticmethod
    def calculate_angle_yz(landmark1, landmark2):
        # Converte as coordenadas normalizadas para coordenadas na imagem
        x1, y1, z1 = landmark1.x, landmark1.y, landmark1.z
        x2, y2, z2 = landmark2.x, landmark2.y, landmark2.z

        # Calcular o ângulo entre os dois pontos em relação ao eixo y e z
        angle_y_rad = math.atan2(z2 - z1, y2 - y1)
        angle_z_rad = math.atan2(y2 - y1, x2 - x1)

        angle_y_deg = math.degrees(angle_y_rad)
        angle_z_deg = math.degrees(angle_z_rad)

        return angle_y_deg, angle_z_deg

    def parar_camera(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
