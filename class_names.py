class Names:
    def __init__(self):
        self.class_names = {
            0: "caixa_fone",
            1: "controle_xbox",
            2: "garrafa",
            3: "mouse",
            4: "talco",
            5: "dedo_1",
            6: "dedo_2",
            7: "dedo_3",
            8: "dedo_4",
            9: "dedo_5",
            10: "2_dedos",
            11: "3_dedos",
            12: "4_dedos",
            13: "5_dedos",
            14: "mao_fechada",
        }

    def get_class_names(self):
        return self.class_names

    def get_class_name(self, class_id):
        return self.class_names[class_id]

    def get_class_id(self, class_name):
        for key, value in self.class_names.items():
            if value == class_name:
                return key
        return None

# class_names = {
#         0: "caixa_fone",
#         1: "controle_xbox",
#         2: "garrafa",
#         3: "mouse",
#         4: "talco",
#         5: "dedo_1",
#         6: "dedo_2",
#         7: "dedo_3",
#         8: "dedo_4",
#         9: "dedo_5",
#         10: "2_dedos",
#         11: "3_dedos",
#         12: "4_dedos",
#         13: "5_dedos",
#         14: "mao_fechada",
# }