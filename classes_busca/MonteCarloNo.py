# MIT License
#
# Copyright (c) 2018 Luiz Felipe de Melo (lffloyd), Vítor Costa (vitorhardoim), Renato Bastos (RenatoBastos33)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################################################


#Define a classe MonteCarloNo, responsável por descrever o um nó no algoritmo de busca 'Monte-Carlo tree search'.

#Escrito por: Vítor Costa, Renato Bastos.

import copy
# import numpy as np #Substituí as funções do numpy pelas funções normais do Python, pois não consigo instalar o numpy aqui.
import math

class MonteCarloNo:
    def __init__(self, estado, pai = None):
        self.estado = estado
        self.pai = pai
        self.filhos = []
        self.vitorias = 1
        self.visitas = 1
        self.UCT = 0

    def __str__(self):
        x = 0
        for i in self.filhos:
            print("\n\nFilho" + str(x))
            print(i.estado.mesa)
            x+=1
        return "\nQtd de Filhos:" + str(len(self.filhos))

    def expandir(self):
        #print("AQUIII" + str(len(self.estado.jogador.pegaPecasJogaveis())))
        for peca in self.estado.jogador.pegaPecasJogaveis():
            for i in range(0,2):
                novoEstado = copy.deepcopy(self.estado)
                adicionou = novoEstado.mesa.adicionarNaMesa(peca, i)
                novoNo = MonteCarloNo(novoEstado, self)
                novoEstado.jogador.setaVez(False)
                novoEstado.oponente.setaVez(True)
                if (adicionou):
                    novoNo.simular()
                    novoNo.estado.onde = i
                    novoNo.estado.ultimaPecaJogada = peca
                    self.filhos.append(novoNo)



    #funcao para escolher o melhor filho usando o valor do UCT
    def melhorFilho(self):
        melhor=None
        for i in self.filhos:
            i.UCT = (i.vitorias / i.visitas) + (1.4 * (math.sqrt(math.log(self.visitas) / i.visitas)))
            if melhor!=None:
                if i.UCT>melhor.UCT:
                    melhor=i
            else:
                melhor=i
        #print("Melhor filho:" + str(melhor))
        return melhor

    def escolheMelhor(self):
        melhor=None
        txvitorias=0
        for i in self.filhos:
            novatx=i.vitorias/i.visitas
            if melhor!=None:
                if txvitorias<novatx:
                    melhor=i
                    txvitorias=novatx
            else:
                txvitorias=novatx
                melhor=i
        return melhor



    def foiTotalmenteExpandido(self):
        if(self.estado.jogador.ehSuaVez() == True): return len(self.filhos) == len(self.estado.jogador.pegaPecasJogaveis())
        else: return len(self.filhos) == len(self.estado.oponente.pegaPecasJogaveis())

    #funcao de backpropagation para aumentar o numero de simulacoes e vitorias das simulacoes
    def backPropagation(self, no, vitoria, visita):
        if(no != None):
            no.vitorias += vitoria
            no.visitas += visita
            self.backPropagation(no.pai, vitoria, visita)
        else: return

    def gerarJogo(self,no,difSimulacao): #difSimulacao variavel para saber se uma simulacao diferente foi gerada
        #print(no.estado)
        #print(no.estado.ehEstadoFinal())

        #Se o estado e final então o backpropagation sera chamado.
        if no.estado.ehEstadoFinal():
            if difSimulacao:
                #se ganhou adiciona 1 nas vitorias
                if no.estado.jogador.jaGanhou():
                    self.backPropagation(no,1,1)
                    return
            self.backPropagation(no,0,1)
            return

        novoEstado=copy.deepcopy(no.estado)
        #Escolhe o jogador da vez e simula uma jogada
        if novoEstado.jogador.ehSuaVez():
            novoEstado.jogador.jogarRandom(novoEstado.mesa,novoEstado.oponente)
        else:
            novoEstado.oponente.jogarRandom(novoEstado.mesa, novoEstado.jogador)
        achouFilho=False
        #achou uma outra simulação de jogada que levou pro mesmo no?
        for filho in no.filhos:
            if novoEstado.comparar(filho.estado):
                achouFilho=True
                self.gerarJogo(filho,difSimulacao)
        #se não achou, um novo no filho sera criado e sera chamada a funcao novamente para este novo no
        if achouFilho==False:
            novoNo=MonteCarloNo(novoEstado,no)
            no.filhos.append(novoNo)
            self.gerarJogo(novoNo,True)

    def simular(self):
        self.gerarJogo(self,False)
        return
