import pygame
import time
from control_hand.servo_control import HandAngles

# Inicialização do pygame e do controle
pygame.init()
pygame.joystick.init()
controle = HandAngles()

# Verifica se há algum controle conectado
if pygame.joystick.get_count() == 0:
    print("Nenhum controle encontrado.")
    quit()

# Pega o primeiro controle disponível
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Configuração de botões
BUTTON_START = 7
BUTTON_BACK = 6
BUTTON_A = 0
BUTTON_B = 1
BUTTON_LB = 4
BUTTON_RB = 5

# Configuração de eixos
AXIS_LEFT_X = 0
AXIS_LEFT_Y = 1
AXIS_LT = 2

# Estado inicial
current_mode = "parallel"
finger_index = 0
finger_positions = [0, 0, 0, 0, 0, 0]  # Posições dos dedos de 0 a 180


def set_finger_positions(positions):
    # Código para enviar os comandos para a mão robótica definindo a posição dos dedos
    controle.update_angles(positions)
    controle.send_hand_angles(controle.angles)
    print(f"Enviando posições dos dedos: {positions}")


def switch_mode():
    global current_mode
    if current_mode == "parallel":
        current_mode = "individual"
    else:
        current_mode = "parallel"
    print(f"Modo alterado para: {current_mode}")


# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == BUTTON_START:
                switch_mode()
            elif event.button == BUTTON_BACK:
                running = False
            elif event.button == BUTTON_A:
                finger_positions = [180, 180, 180, 180, 180, 0]
                set_finger_positions(finger_positions)
                print("Dedos abertos")
            elif event.button == BUTTON_B:
                finger_positions = [0, 0, 0, 0, 0, 0]
                set_finger_positions(finger_positions)
                print("Dedos fechados")
            elif event.button == BUTTON_LB and current_mode == "individual":
                finger_index = (finger_index - 1) % 5
                print(f"Dedo selecionado: {finger_index}")
            elif event.button == BUTTON_RB and current_mode == "individual":
                finger_index = (finger_index + 1) % 5
                print(f"Dedo selecionado: {finger_index}")
        elif event.type == pygame.JOYAXISMOTION:
            if current_mode == "parallel":
                if event.axis == AXIS_LEFT_Y:
                    analog_value = event.value
                    finger_positions = [int((analog_value + 1) * 90) for _ in range(5)]
                    finger_positions.append(0)
                    set_finger_positions(finger_positions)
                    print(f"Posições dos dedos em paralelo: {finger_positions}")
            elif current_mode == "individual" and event.axis == AXIS_LT:
                analog_value = event.value
                finger_positions[finger_index] = int(analog_value * 180)
                set_finger_positions(finger_positions)
                print(f"Posição do dedo {finger_index}: {finger_positions[finger_index]}")

    # Coloque aqui a lógica para enviar os comandos para a mão robótica de acordo com finger_positions

    time.sleep(0.1)  # Evita processamento excessivo

# Finaliza o pygame
pygame.quit()
