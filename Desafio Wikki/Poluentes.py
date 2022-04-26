
from cProfile import label
import this
from time import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
from tkinter.tix import INTEGER
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename
import os
import matplotlib
from matplotlib import figure
from matplotlib.image import FigureImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.express as px
import numpy
import time

class Application:
    def __init__(self,master=None):
        self.file =""
        self.matrizL = 0
        self.matrizC = 0
        self.malhaMatriz = []
        self.malhaPoluente = []
        self.dimensaoX = 0
        self.dimensaoY = 0
        self.barra = DoubleVar()
        self.barra.set(0)
        self.checked =BooleanVar()

#Construção da janela
  

        self.fontePadrao = ('verdana',8,'bold')
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()
        
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 30
        self.segundoContainer["pady"] = 5
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer["pady"] = 5
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["padx"] = 30
        self.quartoContainer["pady"] = 5
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["padx"] = 20
        self.quintoContainer["pady"] = 5
        self.quintoContainer.pack()
        
        self.sextoContainer = Frame(master)
        self.sextoContainer["padx"] = 20
        self.sextoContainer["pady"] = 5
        self.sextoContainer.pack()

        self.setimoContainer = Frame(master)
        self.setimoContainer["padx"] = 20
        self.setimoContainer["pady"] = 8
        self.setimoContainer.pack()

        self.oitavoContainer = Frame(master)
        self.oitavoContainer["padx"] = 20
        self.oitavoContainer["pady"] = 20
        self.oitavoContainer.pack()

        self.nonoContainer = Frame(master)
        self.nonoContainer["padx"] = 20
        self.nonoContainer["pady"] = 20
        self.nonoContainer.pack()

        self.decimoContainer = Frame(master)
        self.decimoContainer["padx"] = 20
        self.decimoContainer["pady"] = 20
        self.decimoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Dados",font=('verdana',10,'bold'))
        self.titulo.pack()

        self.malhaLabel = Label(self.segundoContainer,text="Malha da ilha: ", font=self.fontePadrao)
        self.malhaLabel.pack(side=LEFT)

        self.malha = Entry(self.segundoContainer)
        self.malha["width"] = 20
        self.malha["font"] = self.fontePadrao
        self.malha.pack(side=LEFT)

        self.carregar = Button(self.segundoContainer,text="Carregar",bd=2,bg='#9c3337',fg='white',font=('verdana',8,'bold'))
        self.carregar["width"] = 10
        self.carregar["command"] = self.carregaMalha
        self.carregar.pack(side=RIGHT)

        self.intesidadeLabel = Label(self.terceiroContainer, text="Intesidade da fonte: ", font=self.fontePadrao)
        self.intesidadeLabel.pack(side=LEFT)

        self.intensidade = Spinbox(self.terceiroContainer,from_=0, to=1000)
        self.intensidade["width"] = 20
        self.intensidade.pack(side=LEFT)

        self.coordenadasLabel1 = Label(self.quartoContainer,text = "Coordenadas (x,y): ")
        self.coordenadasLabel1["font"] = self.fontePadrao
        self.coordenadasLabel1.pack(side=LEFT)

        self.coordenadas = Entry(self.quartoContainer)
        self.coordenadas["width"] = 30
        self.coordenadas.pack(side=RIGHT)

        self.gravarLabel1 = Label(self.quintoContainer,text = "Gravar resultado por: ")
        self.gravarLabel1["font"] = self.fontePadrao
        self.gravarLabel1.pack(side=LEFT)

        self.gravar = ttk.Combobox(self.quintoContainer,values =["Dia","Semana","Mes"])
        self.gravar["width"] = 30
        self.gravar.pack(side=RIGHT)

        self.limiteLabel1 = Label(self.sextoContainer,text = "Limite máximo de iterações: ")
        self.limiteLabel1["font"] = self.fontePadrao
        self.limiteLabel1.pack(side=LEFT)

        self.limite = Spinbox(self.sextoContainer,from_=0, to=1000)
        self.limite["width"] = 20
        self.limite.pack(side=RIGHT)

        self.nomePoluenteLabel1 = Label(self.setimoContainer,text="Nome poluente: ")
        self.nomePoluenteLabel1["font"] = self.fontePadrao
        self.nomePoluenteLabel1.pack(side=LEFT)

        self.nomePoluente = Entry(self.setimoContainer)
        self.nomePoluente["width"] = 30
        self.nomePoluente.pack(side=RIGHT)

        self.check = Checkbutton(self.oitavoContainer,variable=self.checked,text='Exibir mapas de disperção para cada iteração',font=('verdana',8,'bold'), onvalue=True, offvalue=False)
        self.check.pack()

        self.iniciar = Button(self.nonoContainer,text="Iniciar simulação",bd=2,bg='#9c3337',fg='white',font=('verdana',8,'bold'))
        self.iniciar["command"] = self.geradorIteracao
        self.iniciar.pack(side=LEFT)

        self.nova = Button(self.nonoContainer,text="Nova simulação",bd=2,bg='#9c3337',fg='white',font=('verdana',8,'bold'))
        self.nova["command"] = self.novaSimulacao
        self.nova.pack(side=RIGHT)

        self.progressoLabel1 = Label(self.decimoContainer,text="Progresso (%) ")
        self.progressoLabel1["font"] = self.fontePadrao
        self.progressoLabel1.pack(side=LEFT)

        self.progresso = Progressbar(self.decimoContainer,length=280,mode='determinate',variable=self.barra,maximum=100)
        self.progresso.pack(side=RIGHT)

        self.canvas = tkinter.Canvas(bg="white", height=500, width=500)
        

        
#Carrega a matriz recebida 
    def carregaMalha(self):
        self.OpenFile()
        
        malha = open(self.file,'r')
        texto = []
        matrizMalha = []
        texto = malha.readlines()

        for i in range(len(texto)):  
            matrizMalha.append(texto[i].split())  

        for i in range(len(matrizMalha)):
            for z in range(len(matrizMalha[i])):
                matrizMalha[i][z] = int(matrizMalha[i][z])

        self.dimensaoX = matrizMalha[0][0]
        self.dimensaoY = matrizMalha[1][0]

        matrizMalha.pop(0)
        matrizMalha.pop(0)

        self.malhaMatriz = matrizMalha
        print(self.malhaMatriz)

        self.malhaMatriz.pop()
        
        
        self.plotaMapaTerreno(self.malhaMatriz)
        malha.close()


#Limpa o formulário
    def novaSimulacao(self):
        self.file =""
        self.matrizL = 0
        self.matrizC = 0
        self.malhaMatriz = []
        self.malhaPoluente = []
        self.dimensaoX = 0
        self.dimensaoY = 0
        self.malha.delete(0,'end')
        self.intensidade.delete(0,'end')
        self.coordenadas.delete(0,'end')
        self.gravar.delete(0,'end')
        self.limite.delete(0,'end')
        self.canvas.get_tk_widget().destroy()
 
        

#Carrega matriz de disperção do poluente
    def carregaMalhaPoluente(self,i,x,y):
        self.malhaPoluente = numpy.zeros((i,x,y),dtype=float)
        

#Abre o arquivo e o define como o atributo "file"
    def OpenFile(self):
        arquivo = askopenfilename()
        self.file = arquivo 
        self.malha.insert(0,os.path.basename(arquivo))

#Acha e carrega o foco do poluente
    def achaCoordenadaCentral(self):
        aux = self.coordenadas.get()
        coordenadas= []
        coordenadas.append(aux.split(","))

        print(coordenadas)
        
        try:
            self.matrizL = int(coordenadas[0][0])
            self.matrizC = int(coordenadas[0][1])
            print(self.matrizL,self.matrizC)
            self.malhaPoluente[0][self.matrizL][self.matrizC] = self.intensidade.get()
        except:
            messagebox.showinfo("coordenada","as coordenadas devem estar no formato (x,y)")
            return False
            
        return True

        
       

#Gera as iterações
    def iteracao(self,array,iteracoes,linhas,colunas):
        
        contador = 0
        parcela = 100/iteracoes
        self.progresso.start()
        contador += parcela

        for i in range(1,iteracoes):
            contador += parcela
            self.barra.set(contador)
            poluente.update()
            
            for l in range(linhas):
                for c in range(colunas):
                    arredores = 0
                    if(l > 0):
                        arredores += array[i-1,l-1,c]
                    if (l < linhas -1): 
                        arredores += array[i-1,l+1,c]
                    if(c < colunas -1):
                        arredores += array[i-1,l,c+1]
                    if(c > 0):
                        arredores += array[i-1,l,c-1]
                    print(arredores)
                    media = arredores/4
                    if(media >= array[i-1,l,c]):
                        array[i,l,c] = round(media,2)
                    else:
                        array[i,l,c] = round(array[i-1,l,c],2)
        
        poluente.update()
        if(self.checked.get()):
            self.plotarMapa()
        self.progresso.stop()


    def confereCampos(self):
        if(self.malha.get() and self.coordenadas.get()):
            return True 
        else:
            return False


    

#Ativa os processo de disperção do poluente/ analisa se alguma malha foi carregada     
    def geradorIteracao(self):
        if(self.confereCampos()):
            self.carregaMalhaPoluente(int(self.limite.get()),self.dimensaoX,self.dimensaoY)
            if(self.achaCoordenadaCentral()):
                self.iteracao(self.malhaPoluente,int(self.limite.get()),self.dimensaoX,self.dimensaoY)
                self.saveFile(self.malhaPoluente)
                self.canvas.get_tk_widget().destroy()
                self.malhaMatriz = self.malhaPoluente[int(self.limite.get())-1]
                self.plotaMapaTerreno(self.malhaMatriz)
        else:
            messagebox.showinfo("Campos vazios","Preencha todos os campos")

#Gera um heatmap para observação da dispersão do poluente
    def plotarMapa(self):
        for i in range(int(self.limite.get())):
            fig = px.imshow(self.malhaPoluente[i],text_auto=True)
            fig.show()
            time.sleep(0.5)

#Gera o mapa do terreno recipiente
    def plotaMapaTerreno(self,matriz):
        fig = plt.Figure(figsize=(8,4),dpi=100)
        ax =fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig,poluente)
        self.canvas.get_tk_widget().pack()

        ax.imshow(matriz)
        ax.set_title("Terreno recipiente")
        fig.tight_layout()
        self.canvas.get_tk_widget().update()
        

#Salva as iterações: dia/semana/mes    
    def saveFile(self,array):
        nome = "Poluente" if not self.nomePoluente.get() else self.nomePoluente.get()
        if(self.gravar.get() == "Dia"):
          

            for i in range(int(self.limite.get())):
                arquivo = f"dia/{nome}_00{i}.txt"
                geradorArquivo = open(arquivo,"w")
                for l in range(self.dimensaoX):
                    geradorArquivo.write("\n")
                    for c in range(self.dimensaoY):
                        geradorArquivo.write("  "+str(array[i][l][c]).replace(".",","))

            geradorArquivo.close()
            
        elif(self.gravar.get() == "Semana"):
            for i in range(int(self.limite.get())):
                arquivo = f"semana/{nome}_00{i*7}.txt"
                geradorArquivo = open(arquivo,"w")
                for l in range(self.dimensaoX):
                    geradorArquivo.write("\n")
                    for c in range(self.dimensaoY):
                        geradorArquivo.write("  "+str(array[i][l][c]).replace(".",","))

        elif(self.gravar.get() == "Mes"):
            for i in range(int(self.limite.get())):
                arquivo = f"mes/{nome}_00{i*30}.txt"
                geradorArquivo = open(arquivo,"w")
                for l in range(self.dimensaoX):
                    geradorArquivo.write("\n")
                    for c in range(self.dimensaoY):
                        geradorArquivo.write("  "+str(array[i][l][c]).replace(".",","))

            geradorArquivo.close()

        else:
            pass
   

poluente = Tk()
poluente.title("Poluentes")
poluente.iconbitmap(r'images/wikki.ico')
poluente.resizable(True,True)
poluente.minsize(width = 500, height = 400) 
poluente.maxsize(width = 1000, height = 1000) 
Application(poluente)
poluente.mainloop()



