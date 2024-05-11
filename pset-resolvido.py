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


# Documentada
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


# Documentada
def mudar_forma_kernel2D(kernel):
    """Altera a forma de um Kernel onde seus valores são passados como vetor para uma MATRIZ BIDIMENSIONAL.

    :param kernel: Kernel de formato [<INT>, [<VETOR DE VALORES>]]
    """
    k = kernel[0]  # Kernel[0] é a dimensão da matriz do Kernel. Sempre deve ter a forma de um quadrado AxA|A é impar.
    novo_kernel = []  # Variável de suporte
    for i in range(k):  # Percorre a quantidade de linhas
        novo_kernel.append(kernel[1][:k])  # Adiciona uma fatia do tamanho das colunas na variável de suporte.
        del kernel[1][:k]  # Deleta da matriz do kernel original a fatia adicionada na variável suporte.
    kernel[1] = novo_kernel  # Substitui a matriz antiga pela nova 2D.


def calcular_correlacao_desfoque_2(k, vizinhos):
    return calcular_correlacao(k, vizinhos) / (k[0] * k[0])


def calcular_correlacao_desfoque(k, vizinhos):
    return round(calcular_correlacao(k, vizinhos) / (k[0] * k[0]))  # Retorna o valor arrendodado com 0 casas decimais.


# Documentada
def calcular_correlacao(k, vizinhos):
    """Calcula a correlação de uma matriz de números com a matriz de um Kernel, resultando num único valor.
    Multiplicando cada valor no indíce (x,y) pelo valor (x,y) na matriz do Kernel e somando os {k} valores.

    :param k: Kernel no formato [<INT>, [<MATRIZ>]
    :param vizinhos: Matriz de números vizinhos.

    :return: Valor do píxel.
    """
    valor = 0  # Total da soma.
    for i in range(k[0]):  # Percorre uma Matriz Bidimensional do tamanho do Kernel
        for j in range(k[0]):
            valor += vizinhos[i][j] * k[1][i][j]  # Soma a multiplicação do valor na lista vizinhos com seu respectivo
            # peso na matriz do kernel.

    return valor


# Documentada
def __verificar_valor__(valor):
    """Faz o tratamento do valor de um píxel. Se valor < 0 retorna 0, se valor > 255 retorna 255

    :param valor: Valor/Cor

    :return: 255 se o valor for maior que 255 || 0 se o valor for menor que 0.
    """
    if valor > 255:
        return 255
    elif valor < 0:
        return 0
    return valor


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura  # Largura em píxel da imagem.
        self.altura = altura  # Altura em píxel da imagem
        self.pixels = pixels  # Lista com a cor correspondente a cada píxel.

    # Documentada
    def __criar_imagem_borda_x__(self):
        """Calcula e retorna uma versão da imagem com filtro de detecção de borda vertical.

        :return: Nova imagem com filtro de borda vertical.
        """
        kx = [3, [-1, 0, 1,
                  -2, 0, 2,
                  -1, 0, 1]]  # Kernel de detecção de borda vertical
        imagem_x = self.aplicar_kernel(kx, calcular_correlacao)  # Gera uma nova imagem proveniente da aplicação do
        # kernel de detecção vertical com a imagem.
        return imagem_x

    # Documentada
    def __criar_imagem_borda_y__(self):
        """Calcula e retorna uma versão da imagem com filtro de detecção de borda horizontal.

        :return: Nova imagem com filtro de borda horizontal.
        """
        ky = [3, [-1, -2, -1,
                  0, 0, 0,
                  1, 2, 1]]  # Kernel de detecção de borda horizontal.
        imagem_y = self.aplicar_kernel(ky, calcular_correlacao)  # Gera uma nova imagem proveniente da aplicação do
        # kernel de detecção horizontal com a imagem.
        return imagem_y

    # Documentada
    def calcular_mascara_nao_nitidez(self, imagem_borrada):
        """Aplica um filtro de nitidez na imagem, utilizando a mesma imagem com filtro borrado.

        :param imagem_borrada: Versão da imagem borrada. De prefêrencia, a imagem borrada deve ser gerada pelo método
        self.borrada(n)

        :return: Cópia da imagem com filtro de nitidez.
        """
        imagem_nova = Imagem.nova(self.largura, self.altura)  # Cria uma cópia da imagem toda branca.
        for i in range(self.altura * self.largura):  # Percorre o vetor de píxel da imagem.
            novo_valor = round(2 * self.get_pixel(i) - imagem_borrada.get_pixel(i))  # Calcula o novo valor do píxel.

            imagem_nova.set_pixel(i, __verificar_valor__(novo_valor))  # Altera o valor do píxel da cópia da
            # imagem pelo valor recordado [valor < 0 = 0 || valor > 255 = 255]

        return imagem_nova

    # Precisa escrever a explicação da lógica ainda.
    def __pegar_vizinhos__(self, x, y, k):
        """Pega os vizinhos (k*k) mais próximos de um valor localizado numa matriz bidimensional localizado por (x,y) e
        retorna uma matriz (x*y) com os vizinhos e o número passado, nos seus respetivos índicies.

        Explicação da fórmula -(k // 2): '//' é o operador de divisão exata. O resultado proveniente da divisão exata
        de uma das dimensões do kernel por 2, resultada na distância diagonal do valor no centro (valor buscado)
        do ponto inicial da matriz de números vizinhos. Exemplo: Imagine aplicar um kernel 3x3 em uma matriz de píxel.
        Para cada píxel será necessário encontrar os 3 * 3 - 1 = 8 píxeis mais próximos dele e adicionar em uma matriz,
        onde o valor no centro, é o valor buscado, para assim, realizar a correlação do vetor de vizinhos com os valores
        do kernel. O ponto (1,1) representa o valor central da matriz de vizinhos, que é o número buscado. A posição do
        primeiro valor vizinho, (0,0) com relação a posição na matriz de vizinhos e não com seu valor na matriz de píxel
        da imagem... Talvez esteja confuso.



        :param x: Índice da linha do píxel.
        :param y: Índice da coluna do píxel.
        :param k: Tamanho do Kernel / Número de vizinhos.

        :return: Matriz com os valores vizinhos, do tamanho k*k, com o valor buscado (x,y) no centro.
        """
        divisao = -(k // 2)  # Distância do primeiro valor vizinho do ponto central buscado.
        vizinhos = []  # Variável suporte
        for i in range(k):  # Percore as linhas do kernel
            linha = []  # Variável de suporte representando as linhas
            xp = divisao + i + x  # Indíce (x) do vizinho (xp, yp) do píxel buscado na matriz de píxel original.
            for j in range(k):  # Percorre as colunas
                yp = divisao + j + y  # Indíce (y) do vizinho (xp, yp) do píxel buscado na matriz original.
                linha.append(self.get_pixel(xp, yp))  # Adiciona na linha o valor do píxel (xp, yp) na matriz de píxel
                # da imagem. Não precisa ser um valor com indíce real.
            vizinhos.append(linha)  # Após adicionar os k valores, adiciona a linha na lista de vizinhos.
        return vizinhos  # Retorna a lista.

    # Documentada
    def __mudar_para_1D__(self):
        """Transforma a lista de píxeis em forma bidimensional (matriz) para um vetor unidimensional.
        Permitindo que os seus valores sejam acessados atráves da busca de um indíce único.
        """
        nova_forma = []  # Variável de suporte
        for i in range(self.altura):  # Percorre a matriz
            for j in range(self.largura):
                nova_forma.append(self.get_pixel(i, j))  # Adiciona na variável de suporte cada valor da Matriz original
                # Em forma de Ordem de Linhas
        self.pixels = nova_forma  # Salva a nova forma no atributo do Objeto.

    # Documentada
    def __mudar_para_2D__(self):
        """Transforma a lista de píxeis em forma unidimensional (vetor) para uma matriz bidimensional (matriz).
        Permitindo que os seus valores sejam acessados atráves da busca por um par ordenado.
        """
        nova_forma = []  # Variável de suporte
        for i in range(self.altura):  # Percorre na quantidade de linhas
            nova_forma.append(self.pixels[:self.largura])  # Adiciona na nova_forma uma fatia do VETOR original do
            # tamanho da LARGURA da imagem
            del self.pixels[:self.largura]  # Deleta a fatia retirada do VETOR de pixeis.
        self.pixels = nova_forma  # Adiciona a MATRIZ MULTIDIMENSIONAL no atributo original da classe.

    # Documentada
    def aplicar_kernel(self, k, funcao):
        """Correlaciona um Kernel k com a matriz de píxels de uma imagem, aplicando uma função funcao para cada píxel.

        :param k: Kernel a ser utilizado na correlação. Exemplo: [<INT>, [<MATRIZ INT*INT>]]
        :param funcao: Função de correlação a ser realizada para cada píxel da imagem.

        :return: Uma nova imagem proveniente da correlação entre o kernel e a imagem.
        """
        nova_imagem = Imagem.nova(self.largura, self.altura)  # Cria uma cópia da nova imagem em branco.
        copia_pixels = [pixel for pixel in self.pixels]  # Copia os píxeis da imagem
        imagem_copia = Imagem(self.largura, self.altura, copia_pixels)  # Altera os píxeis da imagem cópia para os reais
        imagem_copia.__mudar_para_2D__()  # Altera o vetor de píxel da imagem principal para uma matriz bidimensional.
        nova_imagem.__mudar_para_2D__()  # Altera o vetor de píxel da nova imagem para uma matriz bidimensional.
        mudar_forma_kernel2D(k)  # Muda a forma do Kernel para uma matriz bidimensisonal.
        for i in range(self.altura):  # Percorre uma matriz com o tamanho da imagem original
            for j in range(self.largura):
                vizinhos = imagem_copia.__pegar_vizinhos__(i, j, k[0])  # Para cada píxel, pega uma lista com os valores
                # vizinhos
                nova_imagem.set_pixel(i, funcao(k, vizinhos), j)  # Altera o valor do píxel da nova imagem de índice
                # (i, j) para o valor retornado de uma função de correlação.
        nova_imagem.__mudar_para_1D__()  # Transforma os píxeis da imagem para VETOR novamente.
        mudar_forma_kernel1D(k)  # Transforma a matriz dos valores do Kernel em um VETOR novamente.

        """Essa transformação da matriz de píxeis para um vetor deve ocorrer pois o cálculo é trabalhado com os píxeis
         representados em uma MATRIZ BIDIMENSIONAL e a função utilizada para mostrar imagens trabalha com píxeis em 
         forma de VETOR, sendo necessário voltar tudo para VETOR, ao final do processamento."""
        return nova_imagem

    # Documentada
    def get_pixel(self, x, y=None):
        """Função para pegar o valor de um píxel específico.
        Caso y não seja passado, a função buscará um píxel de indíce x representado num VETOR. Caso y seja passado,
        a função irá buscar um píxel representado por um par ordenado (x,y).

        Como a lista de píxels das imagens são passadas por padrão como uma matriz unidimensional (VETOR),
        porém depois precisei transformar numa matriz bidimensional, alterei a função para permitir buscar tanto
        por par ordenado como indíce único.

        Caso um valor fora da matriz de píxel seja buscado, a função retorna um píxel simulando um versão extendida da
        imagem original.

        :param x: Indíce do píxel || Indíce da linha
        :param y: Indíce da coluna do píxel. None por padrão.

        :return: Valor do píxel.
        """
        if y is None:  # Verifica se y é do tipo None, se for, retorna um píxel representado por um indíce[x]
            return self.pixels[x]
        else:  # Caso contrário, trabalha com um píxel representado por par ordenado[x][y]
            if (-1 < x < self.altura) and (-1 < y < self.largura):  # Verifica se o indíce está presente na matriz
                return self.pixels[x][y]
            else:
                if x < 0 > y:  # Tratamento para o canto superior esquerdo
                    return self.pixels[0][0]  # Retorna o primeiro da primeira linha
                elif x < 0 and y >= self.largura:  # Tratamento para o canto superior direito
                    return self.pixels[0][self.largura - 1]  # Retorna ultimo da primeira linha
                elif x > self.altura - 1 and y < 0:  # Tratamento para o canto inferior esquerdo
                    return self.pixels[self.altura - 1][0]  # Retornar primeiro da última linha.
                elif x >= self.altura and y >= self.largura:  # Tratamento para o canto inferior direito
                    return self.pixels[self.altura - 1][self.largura - 1]  # Retornar ultimo da última linha
                elif x < 0:  # Tratamento para o lado superior
                    return self.pixels[0][y]  # Retorna o valor da primeira linha, logo abaixo
                elif x >= self.altura:  # Tratamento para o lado inferior
                    return self.pixels[self.altura - 1][y]  # Retorna o valor da mesma coluna, logo acima.
                elif y < 0:  # Tratamento para o lado esquerdo
                    return self.pixels[x][0]  # Retorna o primeiro valor da mesma linha
                elif y >= self.largura:  # Tratamento para o lado direito
                    return self.pixels[x][self.largura - 1]  # Retorna o último valor, da mesma linha

    # Documentada
    def __printar_atributos__(self):
        """Printa os atributos do objeto"""
        print(self)

    # Documentada
    def set_pixel(self, x, cor, y=None):
        """Função para alterar o valor de um píxel. Pode ser representado por indície único ou par ordenado.

        :param x: Indíce do píxel/Indíce da linha do píxel.
        :param cor: Valor novo.
        :param y: Indíce da coluna do píxel. None por padrão.
        """
        if y is None:  # Caso y não seja passado. Busca somente pelo indíce x.
            self.pixels[x] = cor  # Altera o valor do píxel.

        else:  # Caso contrário, busca por um par ordenado.
            self.pixels[x][y] = cor  # Altera o valor do píxel.

    # Documentada
    def aplicar_por_pixel(self, func):
        """Percorre a imagem e calcula um novo valor para cada píxel, baseado na função passada.

        :return: Uma cópia da imagem com os píxeis recalculados.
        """
        resultado = Imagem.nova(self.largura, self.altura)  # Cria uma cópia da imagem com todos os píxeis sendo 0.

        for x in range(resultado.largura * resultado.altura):  # Percorre um vetor do tamanho da matriz de píxeis.
            cor = self.get_pixel(x)  # Pega a cor do pixel.
            nova_cor = func(cor)  # Aplica uma função para gerar um novo valor.
            resultado.set_pixel(x, nova_cor)  # Muda a cor do pixel para o valor calculado.
        return resultado

    # Documentada
    def invertida(self):
        """Inverter as cores de uma imagem.

        :return: Cópia da imagem com filtro de inversão.
        """
        return self.aplicar_por_pixel(lambda c: 255 - c)  # CORRIGIDO: o valor correto do cálculo é 255, não 256, pois
        # os valores vão 0 a 255, sendo 0 o mais baixo e 255 o mais alto.

    # Documentada
    def borrada(self, n, arredondar=True):
        """Aplica o efeito de borrada.

        :param n: Tamanho do Kernel.
        :param arredondar: Arredondar resultado final? default=True.

        :return: Imagem atual com filtro de 'blur'(borrão)
        """
        kernel_borrada = [n, [1 for _ in range(n * n)]]  # Gera um kernel de tamanho n*n prenchido por 1
        if arredondar:
            imagem_borrada = self.aplicar_kernel(kernel_borrada, calcular_correlacao_desfoque)  # Aplica o kernel de
            # desfoque utilizando a função de correlação com arredondamento
            return imagem_borrada
        else:
            imagem_borrada = self.aplicar_kernel(kernel_borrada, calcular_correlacao_desfoque_2)  # Aplica o kernel
            # de desfoque utilizando a função de correlação sem arredondamento
            return imagem_borrada

    # Documentada
    def focada(self, n):
        """Aplica o efeito de filtro de nitidez.

        :param n: Tamanho do Kernel.

        :return: Imagem atual com filtro de foco.
        """
        imagem_borrada = self.borrada(n, False)  # Gera uma cópia da imagem atual com filtro borrado
        return self.calcular_mascara_nao_nitidez(imagem_borrada)

    # Documentada
    def bordas(self):
        """Implementa um operador Sobel para aplicar o efeito de detecção de borda na imagem. A função junta duas
        versões da imagem com filtro, uma com as bordas horizontais destacadas e outra com as bordas verticais
        destacadas, depois, junta as duas em uma única imagem com filtro de borda.

        :return: Copia da imagem com filtro de detecção de borda.
        """
        imagem_borda_x = self.__criar_imagem_borda_x__()  # Calcula uma imagem com bordas horizontais destacadas
        imagem_borda_y = self.__criar_imagem_borda_y__()  # Calcula uma imagem com bordas verticais destacadas
        imagem_borda = Imagem.nova(self.largura, self.altura)  # Cria uma nova imagem vazia

        for i in range(self.altura * self.largura):  # Percorre o vetor de píxeis da imagem
            valor = round(((imagem_borda_x.get_pixel(i) ** 2) + (imagem_borda_y.get_pixel(i) ** 2)) ** 0.5)  # Calcula
            # o valor de cada píxel da nova imagem como sendo (pixelX^2 + pixelY^2)^0.5,arredonda o valor para um
            # inteiro, juntando os dois píxeis de cada imagem.

            imagem_borda.set_pixel(i, __verificar_valor__(valor))  # Altera o pixel da nova imagem para o resultado
            # verificado da fórmula e recortado [valor < 0 = 0 || valor > 255 = 255].

        return imagem_borda  # Retorna uma versão da imagem com efeito de detecção de borda.

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

    imagem_borrada = imagem.bordas()
    imagem_borrada.mostrar()

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
