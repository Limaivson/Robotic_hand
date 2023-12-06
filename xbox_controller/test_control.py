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

# Estados
PARALLEL_MODE = "paralelo"
INDIVIDUAL_MODE = "individual"
FINE_TUNING_MODE = "ajuste_fino"
current_mode = PARALLEL_MODE

# Índice do dedo selecionado
finger_index = 0

# Posições dos dedos de 0 a 180
finger_positions = [0, 0, 0, 0, 0, 90]


def set_finger_positions(positions):
    # Código para enviar os comandos para a mão robótica definindo a posição dos dedos
    positions[-1] = 110  # Mantém o último elemento como 90
    controle.update_angles(positions)
    controle.send_hand_angles(controle.angles)
    print(f"Enviando posições dos dedos: {positions}")


def switch_mode():
    global current_mode
    if current_mode == PARALLEL_MODE:
        current_mode = INDIVIDUAL_MODE
    elif current_mode == INDIVIDUAL_MODE:
        current_mode = FINE_TUNING_MODE
    else:
        current_mode = PARALLEL_MODE
    print(f"Modo alterado para: {current_mode}")


def increase_finger_position(position):
    if position < 170:
        return position + 10
    return position


def decrease_finger_position(position):
    if position > 10:
        return position - 10
    return position


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
                finger_positions = [180, 180, 180, 180, 180, 90]
                set_finger_positions(finger_positions)
                print("Dedos abertos")
            elif event.button == BUTTON_B:
                finger_positions = [0, 0, 0, 0, 0, 90]
                set_finger_positions(finger_positions)
                print("Dedos fechados")
            elif event.button == BUTTON_LB and current_mode == INDIVIDUAL_MODE:
                finger_index = (finger_index - 1) % 6
                print(f"Dedo selecionado: {finger_index}")
            elif event.button == BUTTON_RB and current_mode == INDIVIDUAL_MODE:
                finger_index = (finger_index + 1) % 6
                print(f"Dedo selecionado: {finger_index}")

        elif event.type == pygame.JOYHATMOTION:
            hat_x, _ = event.value
            if hat_x == 1:  # Cetinha direita pressionada
                if current_mode == PARALLEL_MODE:
                    finger_positions = [increase_finger_position(pos) for pos in finger_positions]
                elif current_mode == FINE_TUNING_MODE:
                    finger_positions[finger_index] = increase_finger_position(finger_positions[finger_index])
            elif hat_x == -1:  # Cetinha esquerda pressionada
                if current_mode == PARALLEL_MODE:
                    finger_positions = [decrease_finger_position(pos) for pos in finger_positions]
                elif current_mode == FINE_TUNING_MODE:
                    finger_positions[finger_index] = decrease_finger_position(finger_positions[finger_index])

            set_finger_positions(finger_positions)

    time.sleep(0.1)  # Evita processamento excessivo

# Finaliza o pygame
pygame.quit()
