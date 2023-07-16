# Mão robótica 
Foi utilizado o YOLOv8 para detectar objetos e estimar a posição entre a mão e o objeto detectado, 
será utilizado o robô nyrio para levar a mão ao objeto.

# Dataset
- Foi utilizado o roboflow para fazer as anotações nas imagens além de usar tecnicas como girar em 90°,
- crop, rotacionar em -15° e +15°, shear, saturação, exposição, blur e noise.

# Treinamento
- Foi usado o YOLOv8 para treinar o modelo.
- Foi feito o treinamento com 100 épocas.

# Detecção 
- Para detectar os objetos foi usado a própria câmera do notebook, mas os resultados seriam melhores,
caso fosse usado a câmera do celular cujo foi tirado as fotos.
- Para utilizar a câmera do celular é necessário usar a GPU para ter um melhor desempenho.
- O modelo foi nomeado como train_v(versão do modelo treinado).pt

# Resultados
- Os resultados obtidos foram satisfatórios, mas ainda é possível melhorar tanto no dataset como no
algoritmo de treinamento e no de detecção.
