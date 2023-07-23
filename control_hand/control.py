import pyserial


class Controle:
    def __init__(self):
        self.esp8266 = None
        self.dedao = 0
        self.indicador = 0
        self.medio = 0
        self.anelar = 0
        self.minimo = 0

    def conectar(self):
        if self.esp8266.is_open:
            print("Já está conectado")
        else:
            try:
                self.esp8266 = pyserial.Serial('COM5', 9600)
            except pyserial.SerialException as se:
                print(f'{se}\nErro ao conectar')

    def desconectar(self):
        if self.esp8266.is_open:
            self.esp8266.close()
        else:
            print("Você precisa estar conectado para desconectar")

    def move_dedao(self, angulo):
        if angulo != self.dedao:
            self.dedao = angulo
            print("Angulo do dedao: ", angulo)
            # Logica para mover o dedao
        else:
            pass

    def move_indicador(self, angulo):
        if angulo != self.indicador:
            self.indicador = angulo
            print("Angulo do indicador: ", angulo)
            # Logica para mover o indicador
        else:
            pass

    def move_medio(self, angulo):
        if angulo != self.medio:
            self.medio = angulo
            print("Angulo do medio: ", angulo)
            # Logica para mover o medio
        else:
            pass

    def move_anelar(self, angulo):
        if angulo != self.anelar:
            self.anelar = angulo
            print("Angulo do anelar: ", angulo)
            # Logica para mover o anelar
        else:
            pass

    def move_minimo(self, angulo):
        if angulo != self.minimo:
            self.minimo = angulo
            print("Angulo do minimo: ", angulo)
            # Logica para mover o minimo
        else:
            pass
