import serial
import time


class HandAngles:


    def __init__(self):
        # Suponha que você tenha uma maneira de obter os ângulos dos dedos
        self.angles = [0, 0, 0, 0, 0, 0]
        self.ser = serial.Serial('COM7', 512000, timeout=1)

    # Atualiza o ângulo do dedão
    def update_thumb(self, angle):
        self.angles[0] = angle

    # Atualiza o ângulo do indicador
    def update_index(self, angle):
        self.angles[1] = angle

    # Atualiza o ângulo do médio
    def update_middle(self, angle):
        self.angles[2] = angle

    # Atualiza o ângulo do anelar
    def update_ring(self, angle):
        self.angles[3] = angle

    # Atualiza o ângulo do mínimo
    def update_pinky(self, angle):
        self.angles[4] = angle

    # Atualiza todos os ângulos de uma vez
    def update_angles(self, new_angles):
        self.angles = new_angles

    def send_hand_angles(self, angles):
        angles_str = ",".join(str(a) for a in angles)
        self.ser.write(angles_str.encode())
        self.ser.write(b'\n')  # Envia uma quebra de linha para indicar o fim da mensagem


if __name__ == "__main__":
    angle_servo = HandAngles()
    angle = 60
    # ser = serial.Serial('COM7', 512000, timeout=1)
    angle_servo.update_thumb(angle)
    angle_servo.send_hand_angles(angle_servo.angles)

    try:
        while True:
            # key_press = input("Pressione 's' para acrescentar 10 graus ao ângulo ou 'q' para sair: ")
            time.sleep(4)
            print(angle_servo.angles[0])
            angle_servo.update_index(angle_servo.angles[1] + 10)
            angle_servo.send_hand_angles(angle_servo.angles)
            # if key_press == 's':
            #     # Acrescenta 10 graus ao ângulo do dedo desejado
            #     angle_servo.update_thumb(angle_servo.angles[0] + 10)
            #     angle_servo.send_hand_angles(angle_servo.angles)  # Envia os ângulos para a mão robótica
            #     print("Ângulo acrescentado com sucesso.")
            # elif key_press == 'q':
            #     print("Encerrando o programa.")
            #     break
            # else:
            #     print("Comando inválido. Pressione 's' para acrescentar 10 graus ou 'q' para sair.")

    except KeyboardInterrupt:
        print("\nEncerrando o programa.")
