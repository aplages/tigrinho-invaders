import graphics as gf
from random import randint
from time import sleep

largura_janela = 600
altura_janela = 800
win = gf.GraphWin("Teste de Jogo", largura_janela, altura_janela)
pontuacao_tela = gf.Rectangle(gf.Point(450, 10), gf.Point(590, 40))
pontuacao_tela.draw(win).setFill('white')



win.setBackground("gray")

def move_sprite(sprite, x_min=0, y_min=0, x_max=largura_janela, y_max=altura_janela, dX=0, dY=0):
    # é possivel dar um limite usando (x_min, y_min, x_max, y_max)
        # x_min # limite mínimo para o eixo X, o padrão é 0
        # y_min # limite mínimo para o eixo y, o padrão é 0
        # x_max # limite máximo para o eixo X, o padrão é a largura da janela
        # y_max # limite máximo para o eixo Y, o padrão é a altura da janela
    # dx: velocidade para direçao do vetor X; o padrão é 0
    # dY: velocidade para direçao do vetor Y; o padrão é 0
    if dX != 0:
        if dX > 0:
            if sprite.getAnchor().getX() < x_max:
                sprite.move(dX, 0)
        elif dX < 0:
            if sprite.getAnchor().getX() > x_min:
                sprite.move(dX, 0)
    elif dY != 0:
        if dY > 0:
            if sprite.getAnchor().getY() < y_max:
                sprite.move(0, dY)
        elif dY < 0:
            if sprite.getAnchor().getY() > y_min:
                sprite.move(0, dY)

def colisao_do_tiro(tiro, sprite): # compara as coordenadas do tiro e da sprite escolhida para determinar se estão se colidindo (retorna True ou False)
    tiro_y = tiro.getAnchor().getY()
    tiro_x = tiro.getAnchor().getX()
    sprite_y = sprite.getAnchor().getY()
    sprite_x = sprite.getAnchor().getX()
    if -20 <= (int(tiro_x) - int(sprite_x)) <= 20:
        if -20 <= (int(tiro_y) - int(sprite_y)) <= 20:
            return True
    return False

## MENU INICIAL
fundo = gf.Image(gf.Point(largura_janela/2, altura_janela/2 ), "imagens/tigrinho_fundo.png")
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
fundo = gf.Image(gf.Point(largura_janela/2, altura_janela/2 ), "imagens/fundo.png")
fundo.draw(win)
pontuacao_tela = gf.Rectangle(gf.Point(450, 10), gf.Point(590, 40)) #Visor da pontuação
pontuacao_tela.draw(win).setFill('gray')
pontuacao = 0
pontuacao_texto = gf.Text(gf.Point(520, 25), pontuacao).draw(win) # mostra a pontuação
##

p1 = gf.Image(gf.Point(300, 725), "imagens/mineiro.png") # Player sprite
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
    vida = gf.Image(gf.Point(posi_vida, 30), "imagens/vidas.png") #sprite vida
    vida.draw(win)
    lista_vidas.append(vida)
    posi_vida += 30

while tecla != 'Escape':
    tecla = win.checkKey()
    clique = win.checkMouse()
    temp = []


    if tecla == "Right" or tecla == 'd':
        move_sprite(sprite=p1, x_min=20, y_min=660, x_max=580, y_max=780, dX=vel)

    elif tecla == "Left" or tecla == 'a':
        move_sprite(sprite=p1, x_min=20, y_min=660, x_max=580, y_max=780, dX=-vel)
    
    elif tecla == "Up" or tecla == 'w':
        move_sprite(sprite=p1, x_min=20, y_min=660, x_max=580, y_max=780, dY=-vel)

    elif tecla == "Down" or tecla == 's':
        move_sprite(sprite=p1, x_min=20, y_min=660, x_max=580, y_max=780, dY=vel)
    
    if not tiro_p1_liberado:
        delay_de_tiro += 1 # se o tiro está carregando, ele aumenta o numero
        if delay_de_tiro == 250: # se o numero chega em 500, o delay termina
            tiro_p1_liberado = True
            delay_de_tiro = 0
    
    if clique != '' and clique != None:
        tiro_p1 = gf.Image(gf.Point(p1.getAnchor().getX(), p1.getAnchor().getY()), "imagens/tiro.png") # sprite do tiro
        
        if tiro_p1_liberado:
            tiro_p1.draw(win)
            lista_de_tiros.append(tiro_p1) # cada tiro faz parte de uma lista
            tiro_p1_liberado = False


    
    for i in lista_de_tiros: # loop para mover todos tiros da lista
        i.move(0, -1)
        for ini in lista_inimigos:
            if colisao_do_tiro(i, ini): # usa a funçao de colisao de tiro, se True, ele destrói o inimigo e o tiro
                i.undraw()
                lista_de_tiros.remove(i)
                ini.undraw()
                lista_inimigos.remove(ini)
                pontuacao_texto.undraw()
                pontuacao += 1
                pontuacao_texto = gf.Text(gf.Point(520, 25), pontuacao).draw(win)
                break
        if i.getAnchor().getY() <= 0: # caso o tiro ultrapasse o limite da janela, ele é "destruido"
           i.undraw()
           lista_de_tiros.pop(0) # remove o tiro da lista, o índice teoricamente é sempre 0 por que o mais antigo sempre estará o mais longe e será o primeiro da lista



    if len(lista_inimigos) < 4:
        inimigo = gf.Image(gf.Point((randint(15, 585)), 0), "imagens/inimigo.png") # sprite inimigo
        inimigo.draw(win)
        lista_inimigos.append(inimigo)
    


    for j in lista_inimigos: # loop para mover todos os inimigos da lista
        j.move(0, 0.2)
        if j.getAnchor().getY() >= 650: # caso o inimigo chegue na base ele é destruido
            j.undraw()
            lista_inimigos.remove(j)
            if len(lista_vidas) > 1:
                vida_perdida = lista_vidas.pop()
                vida_perdida.undraw()
            else:
                tecla = 'Escape' # se não tiver mais vidas, o jogo termina


    sleep(0.0016) # delay dos quadros do jogo


fim_tela = gf.Rectangle(gf.Point(0, 0), gf.Point(largura_janela, altura_janela))
fim_tela.draw(win).setFill('white')
fim_text = gf.Text(gf.Point(largura_janela/2, (altura_janela/2)-20), f"FIM DE JOGO\n\nSua pontuação foi {pontuacao}").draw(win)
gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)+30), gf.Point((largura_janela/2)+80, (altura_janela/2)+70)).draw(win) # BOTAO MENU
gf.Text(gf.Point(largura_janela/2, (altura_janela/2)+50), 'Menu Principal').draw(win) # TEXTO DO BOTAO MENU

gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)+80), gf.Point((largura_janela/2)+80, (altura_janela/2)+120)).draw(win) # BOTAO RANKING
gf.Text(gf.Point(largura_janela/2, (altura_janela/2)+100), 'Ranking Local').draw(win) # TEXTO DO BOTAO RANKING

gf.Text(gf.Point(largura_janela/2, (altura_janela/2)+175), 'Pressione "Esc" para fechar o jogo.').draw(win) # TEXTO DE SAIDA

with open('ranking_local.txt', 'a') as ranking:
    ranking.write(f'{str(pontuacao)};')
    ranking.close()
    # futuramente irá aceitar um input para o nome do jogador
    # terá opção de olhar o ranking


win.getMouse()