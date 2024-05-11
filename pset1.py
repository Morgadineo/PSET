# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Arthur Morgado Teixeira
#    Matrícula: 202306343
#    Turma: CC3mB
#    Email: arthurmorgado7751@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from typing import List, Any

from PIL import Image as PILImage


def mudar_forma_kernel1D(kernel):
    """Altera os valores de um Kernel com MATRIZ BIDIMENSIONAL para um com VETOR unidimensional.

    :param kernel: Kernel de formato [<INT>, [<VETOR DE VALORES>]]
    """
    k = kernel[0]  # Kernel[0] é a dimensão da matriz do Kernel. Deve ser sempre um quadrado AxA
    novo_kernel = []  # Variável de suporte
    for i in range(k):  # Percorre a quantidade de linhas da Matriz do Kernel
        for j in range(k):  # Percorre a quantidade de colunas de cada linha da Matriz
            novo_kernel.append(kernel[1][i][j])  # Adiciona no vetor na forma de ROW-ORDER.
    kernel[1] = novo_kernel  # Substitui a Matriz anterior pelo novo Vetor


def mudar_forma_kernel2D(kernel):
    """Altera a forma de um Kernel onde seus valores são passados como VETOR para uma MATRIZ BIDIMENSIONAL.

    :param kernel: Kernel de formato [<INT>, [<VETOR DE VALORES>]]
    """
    k = kernel[0]  # Kernel[0] é a dimensão da matriz do Kernel. Sempre deve ter a forma de um quadrado AxA|A é impar.
    novo_kernel = []  # Variável de suporte
    for i in range(k):  # Percorre a quantidade de linhas
        novo_kernel.append(kernel[1][:k])  # Adiciona uma fatia do tamanho das colunas na variável de suporte.
        del kernel[1][:k]  # Deleta da matriz do kernel original a fatia adicionada na variável suporte.
    kernel[1] = novo_kernel  # Substitui a matriz antiga pela nova 2D.


def calcular_mascara_nao_nitidez(k, vizinhos):
    valor = 0
    for i in range(k[0]):
        for j in range(k[0]):
            valor += round(vizinhos[i][j] * k[1][i][j])

    return (valor * -1) / 256


def calcular_correlacao_desfoque(k, vizinhos, arredondar=1):
    valor = 0  # Total da soma.
    for i in range(k[0]):  # Percorre uma Matriz Bidimensional do tamanho do Kernel
        for j in range(k[0]):
            valor += vizinhos[i][j] * k[1][i][j]  # Adiciona na soma total o valor do número de indíce (x,y)
            # multiplicado pelo seu equivalente na Matriz do Kernel
    if arredondar:
        return round(valor / (k[0] * k[0]))
    else:
        return valor / (k[0] * k[0])


def calcular_correlacao(k, vizinhos):
    """Calcula a correlação de uma matriz de números com a matriz de um Kernel, resultando num único valor.
    Multiplicando cada valor no indíce (x,y) pelo valor (x,y) na matriz do Kernel e somando os 9.

    :param k: Kernel no formato [<INT>, [<MATRIZ>]
    :param vizinhos: Matriz de números a serem.
    """
    valor = 0  # Total da soma.
    for i in range(k[0]):  # Percorre uma Matriz Bidimensional do tamanho do Kernel
        for j in range(k[0]):
            valor += int(
                vizinhos[i][j] * k[1][i][j])  # Adiciona na soma total o valor do número de indíce (x,y) multipli-
            # cado pelo seu equivalente na Matriz do Kernel
    return valor


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def __pegar_vizinhos__(self, x, y, k):
        """Pega os vizinhos (k*k) mais próximos de um valor localizado numa Matriz Bidimensional localizado por (x,y) e
        retorna uma matriz (x*y) com os vizinhos e o número passado, nos seus respetivos índicies.

        :param x: Índice da linha onde o número se encontra.
        :param y: Índice da coluna onde o número se encontra.
        :param k: Tamanho do Kernel / Número de vizinhos

        :return: Matriz com os valores vizinhos, do tamanho k*k, com o valor buscado (x,y) no centro.
        """
        divisao = -(k // 2)
        vizinhos = []
        for i in range(k):
            linha = []
            xp = divisao + i + x
            for j in range(k):
                yp = divisao + j + y
                linha.append(self.get_pixel(xp, yp))
            vizinhos.append(linha)
        return vizinhos

    def __mudar_para_1D__(self):
        """Transforma uma Matriz Bidimensional de píxels de uma imagem para um VETOR em forma de Ordem de Linhas."""
        nova_forma = []  # Variável de suporte
        for i in range(self.altura):  # Percorre a matriz
            for j in range(self.largura):
                nova_forma.append(self.get_pixel(i, j))  # Adiciona na variável de suporte cada valor da Matriz original
                # Em forma de Ordem de Linhas
        self.pixels = nova_forma  # Salva a nova forma no atributo do Objeto.

    def __mudar_para_2D__(self):
        """Função para transformar uma matriz de píxeis unidimensional (VETOR) de uma imagem em uma
        matriz MULTIDIMENSIONAL, para permitir acessar os píxeis buscando um par ordenado [i, j].
        """
        nova_forma = []  # Variável de suporte
        for i in range(self.altura):  # Percorre na quantidade de linhas
            nova_forma.append(self.pixels[:self.largura])  # Adiciona na nova_forma uma fatia do VETOR original do
            # tamanho da LARGURA da imagem
            del self.pixels[:self.largura]  # Deleta a fatia retirada do VETOR de pixeis.
        self.pixels = nova_forma  # Adiciona a MATRIZ MULTIDIMENSIONAL no atributo original da classe.

    def aplicar_kernel(self, k, funcao_correlacao):
        """Função para correlacionar um Kernel com a Matriz de píxels de um objeto do tipo Imagem.

        :param k: Kernel a ser utilizado na correlação. Exemplo: [<INT>, [<MATRIZ INT*INT>]]

        :return: Uma nova imagem proveniente da correlação entre o Kernel e a Imagem.
        """
        nova_imagem = Imagem.nova(self.largura, self.altura)  # Cria uma nova imagem em branco.
        copia_pixels = [pixel for pixel in self.pixels]
        imagem_copia = Imagem(self.largura, self.altura, copia_pixels)
        imagem_copia.__mudar_para_2D__()  # Altera o vetor de pixel da imagem principal para uma Matriz Bidimensional.
        nova_imagem.__mudar_para_2D__()  # Altera o vetor de píxel da nova imagem para uma Matriz Bidimensional.
        mudar_forma_kernel2D(k)  # Muda a forma do Kernel para uma Matriz Bidimensional.
        for i in range(self.altura):  # Percorre uma Matriz com o tamanho da imagem original
            for j in range(self.largura):
                vizinhos = imagem_copia.__pegar_vizinhos__(i, j, k[0])
                nova_imagem.set_pixel(i, funcao_correlacao(k, vizinhos), j)  # Altera o valor do píxel da nova imagem
                # de índice (i, j) para o valor retornado da função calcular_correlação().
        nova_imagem.__mudar_para_1D__()  # Transforma os píxeis da imagem para VETOR novamente.
        mudar_forma_kernel1D(k)  # Transforma a MATRIZ dos valores do Kernel em um VETOR novamente.

        """Essa transformação da matriz de píxeis para VETOR deve ocorrer pois o cálculo é trabalhado com uma MATRIZ
        BIDIMENSIONAL e a função utilizada para mostrar imagens trabalha com píxeis em forma de VETOR, sendo 
        necessário voltar tudo para VETOR, ao final do processamento."""
        return nova_imagem

    def get_pixel(self, x, y=None):
        """Função para pegar o valor de um píxel específico.
        :param x: Indíce do píxel || Indíce da linha
        :param y: Indíce da coluna do píxel.

        Caso y não seja passado, a função buscará um píxel de indíce x representado num VETOR. Caso y seja passado,
        a função irá buscar um píxel representado por um par ordenado (x,y).

        Como a lista de píxels das imagens são passadas por padrão como uma matriz unidimensional (VETOR),
        porém depois precisei transformar numa matriz bidimensional, alterei a função para permitir buscar tanto
        por par ordenado como indíce único.
        """
        if y is None:  # Verifica se y é do tipo None, se for, retorna um píxel representado por um indíce[x]
            return self.pixels[x]
        else:
            if (-1 < x < self.altura) and (-1 < y < self.largura):
                return self.pixels[x][y]  # Caso contrário, busca um píxel representado por um par ordenado.
            else:
                # Canto superior esquerdo
                if x < 0 > y:
                    return self.pixels[0][0]  # Retorna 0,0
                # Canto superior direito
                elif x < 0 and y >= self.largura:
                    return self.pixels[0][self.largura - 1]  # Retorna ultimo da primeira linha
                # Canto inferior esquerdo
                elif x > self.altura - 1 and y < 0:
                    return self.pixels[self.altura - 1][0]  # Retornar primeiro da ultima linha.
                # Canto inferior direito
                elif x >= self.altura and y >= self.largura:
                    return self.pixels[self.altura - 1][self.largura - 1]  # Retornar ultimo da ultima linha
                # Lado superior
                elif x < 0:
                    return self.pixels[0][y]  # Retorna o valor da primeira linha, logo abaixo
                # Lado inferior
                elif x >= self.altura:
                    return self.pixels[self.altura - 1][y]
                # Lado esquerdo
                elif y < 0:
                    return self.pixels[x][0]  # Retorna o primeiro valor da mesma linha
                # Lado direito
                elif y >= self.largura:
                    return self.pixels[x][self.largura - 1]

    def __printar_parametros__(self):
        """Função para printar a lista de píxeis da imagem"""
        print(self)

    def set_pixel(self, x, cor, y=None):
        """Função para alterar o valor de um píxel. Pode ser representado por indície único ou par ordenado.

        :param x: Indíce do píxel/Indíce da linha do píxel
        :param cor: Valor novo
        :param y: Indíce da coluna do píxel.
        """
        if y is None:  # Caso y não seja passado. Busca somente pelo indíce x.
            self.pixels[x] = cor
        else:
            if 0 < cor < 256:
                self.pixels[x][y] = cor
            elif 0 > cor:
                self.pixels[x][y] = 0
            elif cor > 255:
                self.pixels[x][y] = 255

    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura)  # CORRIGIDO: self.altura e self.largura estavam invertidos,
        # fazendo com que a imagem de resultado diferisse em largura e comprimento.

        # Ao invés de um FOR percorrer o "range" da altura e dentro dele outro FOR percorrer o range da largura,
        # Basta fazer um FOR percorrer o produto da altura com largura.
        for x in range(resultado.largura * resultado.altura):
            cor = self.get_pixel(x)  # GET_PIXEL agora só possui um paramêtro.
            nova_cor = func(cor)
            resultado.set_pixel(x, nova_cor)  # set_pixel agora só possui um paramêtro
        return resultado

    def invertida(self):
        """Função para inverter as cores de uma imagem."""
        return self.aplicar_por_pixel(lambda c: 255 - c)  # CORRIGIDO: o valor correto do cálculo é 255, não 256, pois
        # os valores vão 0 a 255, sendo 0 o mais baixo e 255 o mais alto. 256 é o total de cores possíveis.

    def borrada(self, n):
        kernel_borrada = [n, [1 for i in range(n * n)]]
        imagem_borrada = self.aplicar_kernel(kernel_borrada, calcular_correlacao_desfoque)
        return imagem_borrada

    def focada(self, n):
        imagem_borrada = self.borrada(n)
        imagem_focada = Imagem(self.altura, self.largura, [i for i in self.pixels])
        imagem_focada.__mudar_para_2D__()
        imagem_borrada.__mudar_para_2D__()
        for i in range(self.altura):
            for j in range(self.largura):
                valor = round(2 * imagem_focada.get_pixel(i, j) - imagem_borrada.get_pixel(i, j))
                imagem_focada.set_pixel(i, valor, j)
        imagem_focada.__mudar_para_1D__()
        imagem_borrada.__mudar_para_1D__()

        return imagem_focada

    def bordas(self):
        raise NotImplementedError

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    imagem = Imagem.carregar('test_images/mushroom.png')

    gaussian_blur = [3, [1, 2, 1,
                         2, 4, 2,
                         1, 2, 1]]

    imagem_blur = imagem.aplicar_kernel(gaussian_blur, calcular_gaussian)
    imagem.mostrar()
    imagem_blur.mostrar()

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
