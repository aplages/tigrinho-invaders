import graphics as gf
from random import randint
from time import sleep

largura_janela = 600
altura_janela = 800
win = gf.GraphWin("Teste de Jogo", largura_janela, altura_janela)
pontuacao_tela = gf.Rectangle(gf.Point(450, 10), gf.Point(590, 40))
pontuacao_tela.draw(win).setFill('white')

win.setBackground("gray")

def separa_ranking(lista_rankeada, n=10):
    cont = 0
    ranking_separado = []
    temp = []
    for j in lista_rankeada:
        if cont < 10:
            temp.append(j)
            cont += 1
        else:
            ranking_separado.append(temp)
            temp = []
            temp.append(j)
            cont = 1
    if temp != []:
        ranking_separado.append(temp)
    return ranking_separado

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

def joga(largura_janela=win.getWidth(), altura_janela=win.getHeight()):
    ## JOGO
    gf.Image(gf.Point(largura_janela/2, altura_janela/2 ), "imagens/fundo.png").draw(win) # FUNDO

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
    ciclo = 1
    boss_control = False


    while len(lista_vidas) < 3:
        vida = gf.Image(gf.Point(posi_vida, 30), "imagens/vidas.png") #sprite vida
        vida.draw(win)
        lista_vidas.append(vida)
        posi_vida += 30

    while tecla != 'Escape':
        tecla = win.checkKey()
        clique = win.checkMouse()
        

        if tecla == "Right" or tecla == 'd' or tecla == 'D':
            move_sprite(sprite=p1, x_min=20, y_min=660, x_max=580, y_max=780, dX=vel)

        elif tecla == "Left" or tecla == 'a' or tecla == 'A':
            move_sprite(sprite=p1, x_min=20, y_min=660, x_max=580, y_max=780, dX=-vel)
        
        elif tecla == "Up" or tecla == 'w' or tecla == 'W':
            move_sprite(sprite=p1, x_min=20, y_min=660, x_max=580, y_max=780, dY=-vel)

        elif tecla == "Down" or tecla == 's' or tecla == 'S':
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
                tiro_p1_liberado = False # ativa o delay do tiro

        for i in lista_de_tiros: # loop para mover todos tiros da lista
            i.move(0, -0.5-(0.5*ciclo))
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


        if pontuacao < (30 * ciclo):
            if len(lista_inimigos) < (3 + ciclo):
                inimigo = gf.Image(gf.Point((randint(15, 585)), 0), "imagens/inimigo.png") # sprite inimigo
                inimigo.draw(win)
                lista_inimigos.append(inimigo)
            


            for j in lista_inimigos: # loop para mover todos os inimigos da lista
                j.move(0, 0.2)
                if j.getAnchor().getY() >= 650: # caso o inimigo chegue na base ele é destruido
                    j.undraw()
                    lista_inimigos.remove(j)
                    if len(lista_vidas) > 0:
                        vida_perdida = lista_vidas.pop()
                        vida_perdida.undraw()
                    else:
                        tecla = 'Escape' # se não tiver mais vidas, o jogo termina
                        
        else:
            # Quando a pontuação atingir o alvo
            if pontuacao >= (30 * ciclo):

                # Remove inimigos comuns da tela
                for ini in lista_inimigos:
                    ini.undraw()
                lista_inimigos = []

                # Criar boss 
                if not boss_control:
                    boss_control = True
                    boss_vida = 3
                    boss = gf.Image(gf.Point(randint(50, 550), 100), "imagens/boss.png")
                    boss.draw(win)
                    direcao_boss = 'direita'

                # Mover boss para baixo
                if direcao_boss == 'direita':
                    move_sprite(boss, dX=0.5, x_max=largura_janela-25, x_min=50)
                    if boss.anchor.getX() >= (largura_janela-25):
                        direcao_boss = 'esquerda'
                        move_sprite(boss, dY=10, y_max=altura_janela-25, y_min=100)
                else:
                    move_sprite(boss, dX=-0.5, x_max=largura_janela-25, x_min=50)
                    if boss.anchor.getX() <= (50):
                        direcao_boss = 'direita'
                        move_sprite(boss, dY=10, y_max=altura_janela-25, y_min=100)


                # Verificar colisão dos tiros com o boss
                for tiro in lista_de_tiros[:]:  
                    tiro.move(0, -1)

                    if colisao_do_tiro(tiro, boss):
                        tiro.undraw()
                        lista_de_tiros.remove(tiro)
                        boss_vida -= 1
                        print(f"Vida do boss: {boss_vida}")

                        # Se o boss morrer
                        if boss_vida <= 0:
                            boss.undraw()
                            boss_control = False
                            ciclo += 1
                            if ciclo <= 10:
                                vel = vel + ciclo
        
                            pontuacao += 10

                            # Atualiza pontuação
                            pontuacao_texto.undraw()
                            pontuacao_texto = gf.Text(gf.Point(520, 25), pontuacao).draw(win)
                        break

                # Se o boss passou pela base
                if boss.getAnchor().getY() >= 650:
                    boss.undraw()
                    boss_control = False

                    # Perde vida
                    if len(lista_vidas) > 0:
                        vida_perdida = lista_vidas.pop()
                        vida_perdida.undraw()
                    else:
                        tecla = "Escape"

        sleep(0.0016)     # delay dos quadros do jogo

    return pontuacao
# fim da funcao joga()

def menu_inicial(largura_janela=win.getWidth(), altura_janela=win.getHeight()):
    ## MENU INICIAL
    gf.Image(gf.Point(largura_janela/2, altura_janela/2 ), "imagens/tigrinho_fundo.png").draw(win) # FUNDO

    gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)-20), gf.Point((largura_janela/2)+80, (altura_janela/2)+20)).draw(win).setFill('white') # botao PLAY
    gf.Text(gf.Point(largura_janela/2, altura_janela/2), 'Jogar').draw(win) # texto PLAY

    while True:
        tecla = win.checkKey()
        mouse = win.checkMouse()
        if tecla == 'Escape':
            return 'Sair'
        if mouse != None:
            #print(mouse, type(mouse))
            if ((largura_janela/2)-80) <= mouse.x <= ((largura_janela/2)+80) and ((altura_janela/2)-20) <= mouse.y <= ((altura_janela/2)+20):
                return 'Joga'

def tela_final(pontuacao, salvou, largura_janela=win.getWidth(), altura_janela=win.getHeight()):
    fim_tela = gf.Rectangle(gf.Point(0, 0), gf.Point(largura_janela, altura_janela))
    fim_tela.draw(win).setFill('white')
    salvou_pont = salvou # variável pra testar se JÁ salvou a pontuação
    gf.Text(gf.Point(largura_janela/2, (altura_janela/2)-175), f"FIM DE JOGO\n\nSua pontuação foi {pontuacao}").draw(win)

    if not salvou_pont:
        gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)-70), gf.Point((largura_janela/2)+80, (altura_janela/2)-30)).draw(win) # BOTAO SALVAR PONTUACAO
        gf.Text(gf.Point(largura_janela/2, (altura_janela/2)-50), 'Salvar Pontuação').draw(win) # TEXTO DO BOTAO SALVAR PONTUACAO
    else:
        gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)-70), gf.Point((largura_janela/2)+80, (altura_janela/2)-30)).draw(win) # BOTAO SALVAR PONTUACAO (já salvou)
        gf.Text(gf.Point(largura_janela/2, (altura_janela/2)-50), 'Salvo✅').draw(win) # TEXTO DO BOTAO SALVAR PONTUACAO (já salvou)


    gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)-20), gf.Point((largura_janela/2)+80, (altura_janela/2)+20)).draw(win) # BOTAO JOGAR NOVAMENTE
    gf.Text(gf.Point(largura_janela/2, (altura_janela/2)), 'Jogar Novamente').draw(win) # TEXTO DO BOTAO JOGAR NOVAMENTE

    gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)+30), gf.Point((largura_janela/2)+80, (altura_janela/2)+70)).draw(win) # BOTAO MENU
    gf.Text(gf.Point(largura_janela/2, (altura_janela/2)+50), 'Menu Principal').draw(win) # TEXTO DO BOTAO MENU

    gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)+80), gf.Point((largura_janela/2)+80, (altura_janela/2)+120)).draw(win) # BOTAO RANKING
    gf.Text(gf.Point(largura_janela/2, (altura_janela/2)+100), 'Ranking Local').draw(win) # TEXTO DO BOTAO RANKING

    gf.Text(gf.Point(largura_janela/2, (altura_janela/2)+175), 'Pressione "Esc" para fechar o jogo.').draw(win) # TEXTO DE SAIDA

    #with open('ranking_local.txt', 'a') as ranking:
        #ranking.write(f'{str(pontuacao)};')
        #ranking.close()
        # futuramente irá aceitar um input para o nome do jogador
        # terá opção de olhar o ranking
    
    if not salvou_pont:
        salvando_pont = True # variável pra testar se ESTÁ SALVANDO a pontuação (serve pra salvar a pontualção DEPOIS do jogador escrever o nome dele)
    else:
        salvando_pont = False
    
    while True:
        tecla = win.checkKey()
        mouse = win.checkMouse()
        if tecla == 'Escape':
            return ('Sair', salvou_pont)
        if mouse != None:
            if ((largura_janela/2)-80) <= mouse.x <= ((largura_janela/2)+80):
                if ((altura_janela/2)-70) <= mouse.y <= ((altura_janela/2)-30) and not salvou_pont: # salvar pontuacao
                    #print('salvar pontuacao')
                    gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)-70), gf.Point((largura_janela/2)+80, (altura_janela/2)-30)).draw(win).setFill('white') # BOTAO SALVAR PONTUACAO
                    gf.Text(gf.Point(largura_janela/2, (altura_janela/2)-50), '>SALVAR<').draw(win) # TEXTO DO BOTAO SALVAR PONTUACAO
                    
                    gf.Text(gf.Point(largura_janela/2, (altura_janela/2)-120), 'Nickname:').draw(win)
                    nick_input = gf.Entry(gf.Point(largura_janela/2, (altura_janela/2)-100), 10).draw(win)
                    salvando_pont = True
                    salvou_pont = True
                    
                elif ((altura_janela/2)-70) <= mouse.y <= ((altura_janela/2)-30) and salvando_pont:
                    with open('ranking_local.csv', 'a') as ranking:
                        nick = nick_input.getText()
                        ranking.write(f'\n{str(pontuacao)};{nick}')
                        nick_input.undraw()
                        salvando_pont = False
                        gf.Rectangle(gf.Point((largura_janela/2)-80, (altura_janela/2)-70), gf.Point((largura_janela/2)+80, (altura_janela/2)-30)).draw(win).setFill('white') # BOTAO SALVAR PONTUACAO
                        gf.Text(gf.Point(largura_janela/2, (altura_janela/2)-50), 'Salvo✅').draw(win) # TEXTO DO BOTAO SALVAR PONTUACAO
                elif ((altura_janela/2)-20) <= mouse.y <= ((altura_janela/2)+20): # jogar novamente
                    return ('Joga', salvou_pont)
                elif ((altura_janela/2)+30) <= mouse.y <= ((altura_janela/2)+70): # menu principal
                    return ('Menu', salvou_pont)
                elif ((altura_janela/2)+80) <= mouse.y <= ((altura_janela/2)+120): # ver ranking
                    return ('Local', salvou_pont)

def desenha_ranking(ranking_separado, len_ranking, n=0, largura_janela=win.getWidth(), altura_janela=win.getHeight()):
        #fim_tela = gf.Rectangle(gf.Point(0, 0), gf.Point(largura_janela, altura_janela))
        #fim_tela.draw(win).setFill('white')
        gf.Rectangle(gf.Point(0, 0), gf.Point(largura_janela, altura_janela)).draw(win).setFill('white')
        gf.Text(gf.Point(largura_janela/2, 25), f"Ranking Local:").draw(win)
        
        altura = 50
        for jogador in ranking_separado[n]:
            gf.Rectangle(gf.Point((largura_janela/2)-80, (altura)), gf.Point((largura_janela/2)+80, altura+30)).draw(win) # Quadrado do playerX
            gf.Text(gf.Point(largura_janela/2, altura+15), f'{jogador[1].strip()} - {jogador[0]}').draw(win) # Nome do playerX
            altura += 65
        
        altura = 725
        gf.Rectangle(gf.Point(50, (altura)), gf.Point(150, altura+50)).draw(win) # Quadrado do botao MENU
        gf.Text(gf.Point(100, altura+25), 'Menu').draw(win) # Texto botao MENU
        
        gf.Rectangle(gf.Point(largura_janela-150, (altura)), gf.Point(largura_janela-50, altura+50)).draw(win) # Quadrado do botao VOLTAR
        gf.Text(gf.Point(largura_janela-100, altura+25), 'Voltar').draw(win) # Texto botao VOLTAR

        gf.Rectangle(gf.Point((largura_janela/2)+50, (altura)), gf.Point((largura_janela/2)+75, altura+25)).draw(win) # Quadrado do botao BAIXO
        gf.Text(gf.Point((largura_janela/2)+62.5, altura+12.5), '⬇').draw(win) # Texto botao BAIXO

        gf.Rectangle(gf.Point((largura_janela/2)-75, (altura)), gf.Point((largura_janela/2)-50, altura+25)).draw(win) # Quadrado do botao CIMA
        gf.Text(gf.Point((largura_janela/2)-62.5, altura+12.5), '⬆').draw(win) # Texto botao CIMA

        gf.Text(gf.Point((largura_janela/2), altura+12.5), f'{n+1}/{len_ranking+1}').draw(win) # Texto PAGINA ATUAL

def ver_ranking(largura_janela=win.getWidth(), altura_janela=win.getHeight()):
    #fim_tela = gf.Rectangle(gf.Point(0, 0), gf.Point(largura_janela, altura_janela))
    #fim_tela.draw(win).setFill('white')
    #gf.Text(gf.Point(largura_janela/2, 25), f"Ranking Local:").draw(win)
    
    with open('ranking_local.csv', 'r') as arq:
        ranking_temp = arq.readlines()
        ranking = []
        for i in ranking_temp: # cria sub-listas contendo: [0] = pontuacao // [1] = nome do jogador
            ranking.append(i.split(';'))
        for n in range(len(ranking)): # faz a pontuação do jogador virar int() -- sem isso, o sorted() dá errado
            ranking[n][0] = int(ranking[n][0])
        ranking = sorted(ranking, reverse=True) # organiza o ranking por ordem de pontuação decrescente


        ranking_separado = separa_ranking(ranking) # ranking separado cria um ranking separado por páginas de len(10)
        arq.close()
    max = len(ranking_separado)-1

    desenha_ranking(ranking_separado, len_ranking=max)
    
    print(max)
    pag = 0
    while True:
        tecla = win.checkKey()
        mouse = win.checkMouse()
        if tecla == 'Escape':
            return 'Menu'
        elif tecla == 'Backspace':
            return 'Fim'
        elif tecla == 'Down':
            if pag < max:
                pag += 1
            desenha_ranking(ranking_separado, len_ranking=max, n=pag)
        elif tecla == 'Up':
            if pag > 0:
                pag -= 1
            desenha_ranking(ranking_separado, len_ranking=max, n=pag)
        elif mouse != None:
            print(mouse, type(mouse))
            #if ((largura_janela/2)-80) <= mouse.x <= ((largura_janela/2)+80) and ((altura_janela/2)-20) <= mouse.y <= ((altura_janela/2)+20):
                #return 'Joga'
            if mouse.y > 725:
                if 50 <= mouse.x <= 150 and mouse.y <= 775:
                    return 'Menu'
                elif (largura_janela-150) <= mouse.x <= (largura_janela-50) and mouse.y <= 775:
                    return 'Fim'
                elif ((largura_janela/2)+50) <= mouse.x <= ((largura_janela/2)+75) and mouse.y <= 750:
                    if pag < max:
                        pag += 1
                    desenha_ranking(ranking_separado, len_ranking=max, n=pag)
                elif ((largura_janela/2)-75) <= mouse.x <= ((largura_janela/2)-50) and mouse.y <= 750:
                    if pag > 0:
                        pag -= 1
                    desenha_ranking(ranking_separado, len_ranking=max, n=pag)
                



opcao = 'Menu'
salvou = False
while True:
    if opcao == 'Menu':
        opcao = menu_inicial(largura_janela, altura_janela)
        #if ((largura_janela/2)-80) <= teste.getX() <= ((largura_janela/2)+80) and ((altura_janela/2)-20) <= teste.getY() <= ((altura_janela/2)+20):
            #opcao = 'Joga'
    
    if opcao == 'Joga':
        salvou = False # caso o jogador já tenha salvo a sua pontuação e esteja jogando novamente, ele pode salvar sua nova pontuação depois
        pontuacao = joga(largura_janela, altura_janela)
        opcao = 'Fim'
    
    if opcao == 'Fim':
        retornos = tela_final(pontuacao, salvou) # Essa tela retorna uma tupla pq o jogador pode ter salvo (ou nao) a pontuação dele. **Nao queremos q ele salve a mesma pontuação dnv =)
        opcao = retornos[0]
        salvou = retornos[1]
    
    if opcao == 'Sair':
        break
    
    if opcao == 'Local':
        opcao = ver_ranking()
