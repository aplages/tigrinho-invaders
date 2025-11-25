import graphics as gf
import random as rd
from time import sleep

largura_janela = 600
altura_janela = 800
win = gf.GraphWin("Teste de Jogo", largura_janela, altura_janela)
pontuaçao_tela = gf.Rectangle(gf.Point(450, 10), gf.Point(590, 40))
pontuaçao_tela.draw(win).setFill('white')



win.setBackground("gray")

def move_sprite(sprite, anchor, x_min=0, y_min=0, x_max=largura_janela, y_max=altura_janela, dX=0, dY=0):
    # função usada para mover o sprite e a ancora juntos
    # é possivel dar um limite usando (x_min, y_min, x_max, y_max)
        # x_min # limite mínimo para o eixo X, o padrão é 0
        # y_min # limite mínimo para o eixo y, o padrão é 0
        # x_max # limite máximo para o eixo X, o padrão é a largura da janela
        # y_max # limite máximo para o eixo Y, o padrão é a altura da janela
    # dx: velocidade para direçao do vetor X; o padrão é 0
    # dY: velocidade para direçao do vetor Y; o padrão é 0
    if dX != 0:
        if dX > 0:
            if anchor.getX() < x_max:
                anchor.move(dX, 0)
                sprite.move(dX, 0)
        elif dX < 0:
            if anchor.getX() > x_min:
                anchor.move(dX, 0)
                sprite.move(dX, 0)
    elif dY != 0:
        if dY > 0:
            if anchor.getY() < y_max:
                anchor.move(0, dY)
                sprite.move(0, dY)
        elif dY < 0:
            if anchor.getY() > y_min:
                anchor.move(0, dY)
                sprite.move(0, dY)

def colisao_do_tiro(tiro_anchor, sprite_anchor): # compara as coordenadas do tiro e da sprite escolhida para determinar se estão se colidindo (retorna True ou False)
    tiro_y = tiro_anchor.getY()
    tiro_x = tiro_anchor.getX()
    sprite_y = sprite_anchor.getY()
    sprite_x = sprite_anchor.getX()
    if -20 <= (int(tiro_x) - int(sprite_x)) <= 20:
        if -20 <= (int(tiro_y) - int(sprite_y)) <= 20:
            return True
    return False

## MENU INICIAL
fundo = gf.Image(gf.Point(largura_janela/2, altura_janela/2 ), "tigrinho_fundo.png")
fundo.draw(win)

botao_play = gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)-20), gf.Point((largura_janela/2)+80, (altura_janela/2)+20))
botao_play.draw(win).setFill('white')
texto_play = gf.Text(gf.Point(largura_janela/2, altura_janela/2), 'Jogar').draw(win)

teste = win.getMouse()

while True:
    if ((largura_janela/2)-80) <= teste.getX() <= ((largura_janela/2)+80) and ((altura_janela/2)-20) <= teste.getY() <= ((altura_janela/2)+20):
        break # sai da tela inicial e inicia o jogo
    teste = win.getMouse()
##



## JOGO
fundo = gf.Image(gf.Point(largura_janela/2, altura_janela/2 ), "fundo.png")
fundo.draw(win)
pontuaçao_tela = gf.Rectangle(gf.Point(450, 10), gf.Point(590, 40)) #Visor da pontuação
pontuaçao_tela.draw(win).setFill('gray')
pontuaçao = 0
pontuaçao_texto = gf.Text(gf.Point(520, 25), pontuaçao).draw(win) # mostra a pontuação
##

bolinha = gf.Point(300, 725) # Referência Player
p1 = gf.Image(gf.Point(300, 725), "mineiro.png") # Player sprite
p1.draw(win)
##

##
base = gf.Rectangle(gf.Point(5, 650), gf.Point(595, 795)) # Area limite para se mexer
base.draw(win)
##

vel = 5 # velocidade do jogador
tecla = ''
lista_de_tiros = []
tiro_p1_liberado = True # essa variável será usada para impedir que o jogador spamme tiros
delay_de_tiro = 0 # usado para "recarregar" o tiro antes de poder atirar novamente
lista_inimigos = []
lista_vidas = []
posi_vida = 40


while len(lista_vidas) < 3:
    vida_sprite = gf.Image(gf.Point(posi_vida, 30), "vidas.png") #sprite vida
    vida_anchor = gf.Point(posi_vida, 40) #ancora vida
    vida_sprite.draw(win)
    lista_vidas.append([vida_sprite, vida_anchor])
    posi_vida += 30

while tecla != 'Escape':


    if len(lista_vidas) == 0:
        fim_tela = gf.Rectangle(gf.Point(0, 0), gf.Point(largura_janela, altura_janela))
        fim_tela.draw(win).setFill('white')
        fim_text = gf.Text(gf.Point(largura_janela/2, altura_janela/2), "FIM DE JOGO").draw(win)
        sleep(3)
        break

    tecla = win.checkKey()
    clique = win.checkMouse()
    temp = []


    if tecla == "Right":
        print("Pra direita")
        move_sprite(sprite=p1, anchor=bolinha, x_min=20, y_min=660, x_max=580, y_max=780, dX=vel)

    elif tecla == "Left":
        print("Pra Esquerda")
        move_sprite(sprite=p1, anchor=bolinha, x_min=20, y_min=660, x_max=580, y_max=780, dX=-vel)
    
    elif tecla == "Up":
        print("Pra Cima")
        move_sprite(sprite=p1, anchor=bolinha, x_min=20, y_min=660, x_max=580, y_max=780, dY=-vel)

    elif tecla == "Down":
        print("Pra Baixo")
        move_sprite(sprite=p1, anchor=bolinha, x_min=20, y_min=660, x_max=580, y_max=780, dY=vel)
    
    if not tiro_p1_liberado:
        delay_de_tiro += 1 # se o tiro está carregando, ele aumenta o numero
        if delay_de_tiro == 500: # se o numero chega em 500, o delay termina
            tiro_p1_liberado = True
            delay_de_tiro = 0
    
    if clique != '' and clique != None:
        tiro_p1_sprite = gf.Image(gf.Point(bolinha.getX(), bolinha.getY()), "tiro.png") # sprite do tiro
        tiro_p1_anchor = gf.Point(bolinha.getX(), bolinha.getY()) # ancora do tiro
        
        if tiro_p1_liberado:
            tiro_p1_sprite.draw(win)
            temp.append(tiro_p1_sprite) # vai ser o indice [0]
            temp.append(tiro_p1_anchor) # vai ser o indice [1]
            lista_de_tiros.append(temp) # cada tiro faz parte de uma lista
            tiro_p1_liberado = False


    
    for i in lista_de_tiros: # loop para mover todos tiros da lista
        i[0].move(0, -1)
        i[1].move(0, -1)
        for ini in lista_inimigos:
            if colisao_do_tiro(i[1], ini[1]): # usa a funçao de colisao de tiro, se True, ele destrói o inimigo e o tiro
                i[0].undraw()
                lista_de_tiros.remove(i)
                ini[0].undraw()
                lista_inimigos.remove(ini)
                pontuaçao_texto.undraw()
                pontuaçao += 1
                pontuaçao_texto = gf.Text(gf.Point(520, 25), pontuaçao).draw(win)
                break
        if i[1].getY() <= 0: # caso o tiro ultrapasse o limite da janela, ele é "destruido"
           i[0].undraw()
           lista_de_tiros.pop(0) # remove o tiro da lista, o índice teoricamente é sempre 0 por que o mais antigo sempre estará o mais longe e será o primeiro da lista



    if len(lista_inimigos) < 4:
        posix_ini = rd.randint(15, 585)
        ini_sprite = gf.Image(gf.Point(posix_ini, 0), "inimigo.png") #sprite inimigo
        ini_anchor = gf.Point(posix_ini, 0) # ancora inimigo
        ini_sprite.draw(win)
        lista_inimigos.append([ini_sprite, ini_anchor])
    


    for j in lista_inimigos: # loop para mover todos os inimigos da lista
        j[0].move(0, 0.2)
        j[1].move(0, 0.2)
        if j[1].getY() >= 650: # caso o inimigo chegue na base ele é destruido
            j[0].undraw()
            lista_inimigos.remove(j)
            if len(lista_vidas) > 0:
                vida_perdida = lista_vidas.pop()
                vida_perdida[0].undraw()
            else:
                tecla = 'Escape' # se não tiver mais vidas, o jogo termina


    sleep(0.0016) # delay dos quadros do jogo