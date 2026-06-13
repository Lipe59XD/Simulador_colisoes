#Use   "pyhton -m venv <nome_do_seu_venv>""   para criar seu ambiente virtual
#Ative o seu venv com "<nome_do_seu_venv>/Scripts/activate" no windows e "source <nome_do_seu_venv>/bin/activate" no linux
#instale as depedencias com "pip install -r dependencias.txt"


import pygame as pg
import random


class Bola():
    def __init__(self, pos_x, pos_y): #velocidades e posições aleatórias
        self.velocity = pg.math.Vector2(random.randint(-1000, 1000), random.randint(-1000, 1000))
        self.pos = pg.math.Vector2(pos_x, pos_y)
    def update(self, dt): 
        #Atualiza a posição 
        self.pos += self.velocity * dt
        
        #Verifica colisão com a Borda 
        if self.pos.x < radius:
            self.pos.x = radius
            if self.velocity.x < 0:  # Só rebate se ela estiver se movendo para a esquerda
                self.velocity.x *= -1
                
        elif self.pos.x > screen_x - radius:
            self.pos.x = screen_x - radius 
            if self.velocity.x > 0:  # Só rebate se ela estiver se movendo para a direita
                self.velocity.x *= -1
            
        #Verifica colisão com a Borda Superior / Inferior
        if self.pos.y < radius:
            self.pos.y = radius 
            if self.velocity.y < 0:  # Só rebate se estiver subindo
                self.velocity.y *= -1
                
        elif self.pos.y > screen_y - radius:
            self.pos.y = screen_y - radius
            if self.velocity.y > 0:  # Só rebate se estiver descendo
                self.velocity.y *= -1

def is_colliding(obj1, obj2, radius=20):
    distance = obj1.pos.distance_to(obj2.pos)
    return distance < radius * 2

def collide(obj1, obj2, c_restitution=1):
    #Vetor direção entre os centros
    p = obj1.pos - obj2.pos
    distance = p.length()
    #Evita normalizacao de vetor de tamanho nulo
    if distance == 0:
        return
    
    #Normaliza o vetor in place
    p.normalize_ip()

    # Calcula o quanto elas entraram uma na outra (overlap)
    overlap = (2 * radius) - distance
    if overlap > 0:
        # Empurra cada uma para o lado oposto pela metade do valor sobreposto
        obj1.pos += p * (overlap / 2)
        obj2.pos -= p * (overlap / 2)

    #separa a velocidade original na componente da colisão
    v1_n = obj1.velocity.project(p)
    v2_n = obj2.velocity.project(p)

    #guarda a velocidade perpendicular que nn muda na batida
    v1_t = obj1.velocity - v1_n
    v2_t = obj2.velocity - v2_n

    #v do centro de massa
    v_cm_n = (v1_n + v2_n) / 2

    #Aplica a fórmula apenas na componente da colisão
    v1_n_final = (1 + c_restitution) * v_cm_n - c_restitution * v1_n
    v2_n_final = (1 + c_restitution) * v_cm_n - c_restitution * v2_n

    #A velocidade final
    obj1.velocity = v1_n_final + v1_t
    obj2.velocity = v2_n_final + v2_t

#dimnesões da tela
screen_x = 1900
screen_y = 1060

#raio das bolas
radius = 30

#coeficiente de restituicao
c_restituition = 0.5

#quantidade de bolas
n_objects = 70
objects = []
for i in range(n_objects):
    posicao_valida = False
    tentativas = 0
    max_tentativas = 1000  #tentativas maximas para n travar o jogo
    
    while not posicao_valida and tentativas < max_tentativas:
        tentativas += 1
        
        # posição X e Y 
        x_sorteado = random.randint(radius, screen_x - radius)
        y_sorteado = random.randint(radius, screen_y - radius)
        colidiu = False
        novo_ponto = pg.math.Vector2(x_sorteado, y_sorteado)
        
        # varre lista 'objects' procurando colisões
        for obj in objects:
            distancia = novo_ponto.distance_to(obj.pos)
            
            # se a distância entre os centros for menor que a soma dos raios
            if distancia < (radius + radius):
                colidiu = True
                break 
                
        if not colidiu:
            posicao_valida = True
            
    # achou uma posição livre
    if posicao_valida:
        objects.append(Bola(x_sorteado, y_sorteado))
    else:
        print(f"Aviso: A tela ficou cheia. Foram criados apenas {len(objects)} objetos.")
        break

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((screen_x, screen_y))
run = True
while run:
    dt = clock.tick(180)/1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    for i in range(len(objects)):
        for j in range(i+1, len(objects)):
            if is_colliding(objects[i], objects[j], radius):
                collide(objects[i], objects[j], c_restituition)
        objects[i].update(dt)
        pg.draw.circle(screen, (255, 255, 255), (float(objects[i].pos.x), float(objects[i].pos.y)), radius)
    pg.display.flip()
    screen.fill((0, 0, 0))


pg.quit()
