import flet as ft
import base64
import cv2
from angle_hand import AngleHandDetector
from time import sleep


class Contador(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.ahd = AngleHandDetector()
        self.ahd.iniciar_camera()

    def did_mount(self):
        self.update_timer()

    def update_timer(self):
        while True:
            frame = self.ahd.obter_frame()  # Corrigido para usar o método obter_frame() para obter o frame
            _, im_arr = cv2.imencode('.jpg', frame)
            im_b64 = base64.b64encode(im_arr)
            self.img.src_base64 = im_b64.decode("utf-8")
            self.lbl_dedao.text = "Dedão: {:.2f}".format(self.ahd.dedao_angulo)
            self.lbl_indicador.text = "Indicador: {:.2f}".format(self.ahd.indicador_angulo)
            self.lbl_medio.text = "Médio: {:.2f}".format(self.ahd.medio_angulo)
            self.lbl_anelar.text = "Anelar: {:.2f}".format(self.ahd.anelar_angulo)
            self.lbl_minimo.text = "Mínimo: {:.2f}".format(self.ahd.minimo_angulo)
            self.update()

    def build(self):
        self.img = ft.Image(
            border_radius=ft.border_radius.all(10),
            width=320,  # Defina a largura para corresponder à largura do quadro da câmera
            height=240,  # Defina a altura para corresponder à altura do quadro da câmera
        )
        self.lbl_dedao = ft.Text(
            f"Dedão: 0.00",
            size=16,
            color=ft.colors.WHITE
        )
        self.lbl_indicador = ft.Text(
            "Indicador: 0.00",
            size=16,
            color=ft.colors.WHITE
        )
        self.lbl_medio = ft.Text(
            "Médio: 0.00",
            size=16,
            color=ft.colors.WHITE
        )
        self.lbl_anelar = ft.Text(
            "Anelar: 0.00",
            size=16,
            color=ft.colors.WHITE
        )
        self.lbl_minimo = ft.Text(
            "Mínimo: 0.00",
            size=16,
            color=ft.colors.WHITE
        )

        return ft.Column([
            self.img,
            self.lbl_dedao,
            self.lbl_indicador,
            self.lbl_medio,
            self.lbl_anelar,
            self.lbl_minimo
        ]
        )


secao = ft.Container(
    margin=ft.margin.only(bottom=40),
    content=ft.Row([
        ft.Card(
            elevation=30,
            content=ft.Container(
                bgcolor=ft.colors.WHITE24,
                padding=10,
                border_radius=ft.border_radius.all(20),
                content=ft.Column([
                    Contador(),
                    ft.Text("Captura dos ângulos das articulações",
                            size=20,
                            color=ft.colors.BLACK),
                ]
                ),
            )
        ),
        # ft.Card(
        #     elevation=30,
        #     content=ft.Container(
        #         bgcolor=ft.colors.WHITE24,
        #         padding=10,
        #         border_radius=ft.border_radius.all(20),
        #         content=ft.Column([
        #             ft.Slider(
        #                 min=500, max=900, on_change=lambda e: print(e.control.value)
        #             ),
        #             ft.Slider(
        #                 min=500, max=900,
        #             )
        #
        #         ]
        #         ),
        #
        #     )
        # )
    ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
)


def principal(pagina: ft.Page):
    pagina.padding = 50
    pagina.window_left = pagina.window_left + 100
    pagina.theme_mode = ft.ThemeMode.DARK
    pagina.add(
        secao,
    )


if __name__ == '__main__':
    ft.app(target=principal)
