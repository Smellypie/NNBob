from mlxtend.data import loadlocal_mnist
from skimage.transform import resize
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import os

def Sigmoid(x):
    np.seterr(all='ignore')

    x[x<-500] = -500

    return 1/(1 + np.exp(-x))

def SigmoidDerivative(x):
    np.seterr(all='ignore')

    if x < -500:
        x = -500

    return np.exp(-x)/(np.square(1 + np.exp(-x)))

class DataSet:
    def __init__(self):
        pass
    
    def LoadData(self):
        X, y = loadlocal_mnist(
            images_path='/home/luis/Documents/NN/train-images.idx3-ubyte', 
            labels_path='/home/luis/Documents/NN/train-labels.idx1-ubyte')
        
        self.images = X
        self.labels = y

class NeuralNetwork:
    def __init__(self):
        self.data = DataSet()
        self.data.LoadData()

        self.dWeights1 = np.zeros((16,784))
        self.dWeights2 = np.zeros((16,16))
        self.dWeights3 = np.zeros((10,16))
        
        self.dBiases1 = np.zeros(16)
        self.dBiases2 = np.zeros(16)
        self.dBiases3 = np.zeros(10)
        
    def CreateWeights(self):
        self.TestCounter = 0
        
        self.weights1 = (2*np.random.rand(16,784)-1)/np.sqrt(784)
        self.weights2 = (2*np.random.rand(16,16)-1)/np.sqrt(16)
        self.weights3 = (2*np.random.rand(10,16)-1)/np.sqrt(16)
        
        self.biases1 = np.zeros(16)
        self.biases2 = np.zeros(16)
        self.biases3 = np.zeros(10)
    
    def LoadWeights(self):
        NetData = open("/home/luis/Documents/NN/NetData.txt", "r")
        
        self.TestCounter = np.loadtxt(NetData, comments="#", max_rows = 1)
        self.weights1 = np.loadtxt(NetData, comments="#", max_rows = 16)
        self.weights2 = np.loadtxt(NetData, comments="#", max_rows = 16)
        self.weights3 = np.loadtxt(NetData, comments="#", max_rows = 10)
        self.biases1 = np.loadtxt(NetData, comments="#", max_rows = 16)
        self.biases2 = np.loadtxt(NetData, comments="#", max_rows = 16)
        self.biases3 = np.loadtxt(NetData, comments="#", max_rows = 10)

    def SaveWeights(self):
        if os.path.exists("NetData.txt"):
            os.remove("NetData.txt")

        NetData = open("NetData.txt", "a")
        
        NetData.write("#TestCounter\n")
        NetData.write(str(self.TestCounter))
        NetData = open("NetData.txt", "ab")
        NetData.write(b"\n\n#W1\n")
        np.savetxt(NetData, self.weights1, fmt='%.5f')
        NetData.write(b"\n#W2\n")
        np.savetxt(NetData, self.weights2, fmt='%.5f')
        NetData.write(b"\n#W3\n")
        np.savetxt(NetData, self.weights3, fmt='%.5f')
        NetData.write(b"\n#b1\n")
        np.savetxt(NetData, self.biases1, fmt='%.5f')
        NetData.write(b"\n#b2\n")
        np.savetxt(NetData, self.biases2, fmt='%.5f')
        NetData.write(b"\n#b3\n")
        np.savetxt(NetData, self.biases3, fmt='%.5f')
        
        NetData.close()
    
    def FeedForward(self):
        self.layer1 = Sigmoid(np.matmul(self.weights1, self.input) + self.biases1)
        self.layer2 = Sigmoid(np.matmul(self.weights2, self.layer1) + self.biases2)
        self.output = Sigmoid(np.matmul(self.weights3, self.layer2) + self.biases3)
    
    def BackPropagate(self):
        dWeights1 = np.zeros((16,784))
        dWeights2 = np.zeros((16,16))
        dWeights3 = np.zeros((10,16))
        
        dBiases1 = np.zeros(16)
        dBiases2 = np.zeros(16)
        dBiases3 = np.zeros(10)
        
        p = 0.1
        
        for i in range(16):
            for j in range(784):
                for k in range(10):
                    for l in range(16):
                        dWeights1[i][j] += 2*(self.expectedOutput[k] - self.output[k])*SigmoidDerivative(np.dot(self.weights3[k,:], self.layer2) + self.biases3[k])*self.weights3[k,l]*SigmoidDerivative(np.dot(self.weights2[l,:], self.layer1) + self.biases2[l])*self.weights2[l,i]*SigmoidDerivative(np.dot(self.weights1[i,:], self.input) + self.biases1[i])*self.input[j]
                        if j == 1:
                            dBiases1[i] += 2*(self.expectedOutput[k] - self.output[k])*SigmoidDerivative(np.dot(self.weights3[k,:], self.layer2) + self.biases3[k])*self.weights3[k,l]*SigmoidDerivative(np.dot(self.weights2[l,:], self.layer1) + self.biases2[l])*self.weights2[l,i]*SigmoidDerivative(np.dot(self.weights1[i,:], self.input) + self.biases1[i])
        
        for i in range(16):
            for j in range(16):
                for k in range(10):
                    dWeights2[i][j] += 2*(self.expectedOutput[k] - self.output[k])*SigmoidDerivative(np.dot(self.weights3[k,:], self.layer2) + self.biases3[k])*self.weights3[k,i]*SigmoidDerivative(np.dot(self.weights2[i,:], self.layer1) + self.biases2[i])*self.layer1[j]
                    if j == 1:
                        dBiases2[i] += 2*(self.expectedOutput[k] - self.output[k])*SigmoidDerivative(np.dot(self.weights3[k,:], self.layer2) + self.biases3[k])*self.weights3[k,i]*SigmoidDerivative(np.dot(self.weights2[i,:], self.layer1) + self.biases2[i])
        
        for i in range(10):
            for j in range(16):
                dWeights3[i][j] += 2*(self.expectedOutput[i] - self.output[i])*SigmoidDerivative(np.dot(self.weights3[i,:], self.layer2) + self.biases3[i])*self.layer2[j]
            dBiases3[i] += 2*(self.expectedOutput[i] - self.output[i])*SigmoidDerivative(np.dot(self.weights3[i,:], self.layer2) + self.biases3[i])
        
        self.dWeights1 += p*dWeights1
        self.dWeights2 += p*dWeights2
        self.dWeights3 += p*dWeights3
        
        self.dBiases1 += p*dBiases1
        self.dBiases2 += p*dBiases2
        self.dBiases3 += p*dBiases3
    
    def Test(self, n):
        self.input = self.data.images[n].reshape(-1)
        self.expectedOutput = np.zeros(10)
        self.expectedOutput[self.data.labels[n]] = 1
        
        self.FeedForward()
        self.BackPropagate()
    
    def Learn(self, n):
        for i in range(n):
            for j in range(10):
                self.Test(10*i + int(self.TestCounter) + j)
                
            self.weights1 += self.dWeights1
            self.weights2 += self.dWeights2
            self.weights3 += self.dWeights3
            
            self.biases1 += self.dBiases1
            self.biases2 += self.dBiases2
            self.biases3 += self.dBiases3
            
            self.dWeights1 = np.zeros((16,784))
            self.dWeights2 = np.zeros((16,16))
            self.dWeights3 = np.zeros((10,16))

            self.dBiases1 = np.zeros(16)
            self.dBiases2 = np.zeros(16)
            self.dBiases3 = np.zeros(10)
            
            self.TestCounter += 10
            
            self.SaveWeights()
            
            print("Teste", i+1, "de", n, "completo")
        
    def Guess(self, n):
        self.input = self.data.images[n].reshape(-1)
        expectedOutput = self.data.labels[n]
        
        self.FeedForward()
        
        output = np.argmax(self.output)
        
        print("Ao analizar uma imagem do número", expectedOutput, "o Bob viu um", output)

    def CarregarImagem(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        fileName = input("Inserir nome da imagem\n")

        if fileName == "":
            StartMenu()
        else:
            if os.path.exists(fileName):
                imagem = rgb2gray(img.imread(fileName))

                imagem = resize(imagem, (28, 28))
                
                self.input = imagem.reshape(-1)

                plt.imshow(imagem, cmap='gray', vmin=0, vmax=255)
            else:
                os.system('cls' if os.name == 'nt' else 'clear')

                print("Esta imagem não existe")
                input("\nENTER para continuar")

                self.CarregarImagem()

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def OpcaoCriar():
    os.system('cls' if os.name == 'nt' else 'clear')

    Bob = NeuralNetwork()

    print("Criar uma nova rede vai eliminar a rede actual")
    print("Tens a certeza que é o que pretendes?(y/n)")
    option = input()
    if option == 'y' or option == 'yes':
        Bob.CreateWeights()
        Bob.SaveWeights()

        os.system('cls' if os.name == 'nt' else 'clear')

        print("Rede criada")
        input("\nENTER para continuar")

        StartMenu()
    elif option == 'n' or option == 'no':
        StartMenu()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("Opção indisponível")
        input("\nENTER para continuar")

        OpcaoCriar()

def OpcaoTreinar():
    os.system('cls' if os.name == 'nt' else 'clear')

    Bob = NeuralNetwork()
    Bob.LoadWeights()

    print("Quantos grupos de imagens vamos analizar?")
    print("(cada conjunto são 10 imagens e demora 7-10 minutos)")

    n = int(input())

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Treinando...")
    Bob.Learn(n)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Treino completo")
    input("\nENTER para continuar")

    StartMenu()

def OpcaoAdivinhar():
    os.system('cls' if os.name == 'nt' else 'clear')

    Bob = NeuralNetwork()
    Bob.LoadWeights()

    print("1 - Imagem aleatória")
    print("2 - Carregar imagem")
    print("3 - Voltar")

    option = int(input())

    if option == 1:
        os.system('cls' if os.name == 'nt' else 'clear')

        Bob.Guess(np.random.randint(50000, 60000))

        print(Bob.output)
        input("\nENTER para continuar")

        OpcaoAdivinhar()
    elif option == 2:
        os.system('cls' if os.name == 'nt' else 'clear')

        Bob.CarregarImagem()

        Bob.FeedForward()
        
        output = np.argmax(Bob.output)
        
        print("Ao analizar a imagem, o Bob viu um", output)
        print(Bob.output)
        plt.show()
        input("\nENTER para continuar")

        OpcaoAdivinhar()
    elif option == 3:
        StartMenu()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Opção indisponível")
        input("\nENTER para continuar")

        OpcaoAdivinhar()

def OpcaoBackup():
    os.system('cls' if os.name == 'nt' else 'clear')

    if os.path.exists("NetData.txt"):
        Bob = NeuralNetwork()
        Bob.LoadWeights()

        if os.path.exists("NetDataBackup.txt"):
            os.remove("NetDataBackup.txt")

        NetData = open("NetDataBackup.txt", "a")
        
        NetData.write("#TestCounter\n")
        NetData.write(str(Bob.TestCounter))
        NetData = open("NetData.txt", "ab")
        NetData.write(b"\n\n#W1\n")
        np.savetxt(NetData, Bob.weights1, fmt='%.5f')
        NetData.write(b"\n#W2\n")
        np.savetxt(NetData, Bob.weights2, fmt='%.5f')
        NetData.write(b"\n#W3\n")
        np.savetxt(NetData, Bob.weights3, fmt='%.5f')
        NetData.write(b"\n#b1\n")
        np.savetxt(NetData, Bob.biases1, fmt='%.5f')
        NetData.write(b"\n#b2\n")
        np.savetxt(NetData, Bob.biases2, fmt='%.5f')
        NetData.write(b"\n#b3\n")
        np.savetxt(NetData, Bob.biases3, fmt='%.5f')
        
        NetData.close()

        print("Backup criado")
        input("\nENTER para continuar")

        StartMenu()
    else:
        print("Tens que criar uma rede")
        input("\nENTER para continuar")

        StartMenu()

def StartMenu():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("1 - Nova Rede")
    print("2 - Treinar")
    print("3 - Adivinhar")
    print("4 - Backup Data")
    print("5 - Sair")

    option = int(input())
    
    if option == 1:
        OpcaoCriar()
    elif option == 2:
        OpcaoTreinar()
    elif option == 3:
        OpcaoAdivinhar()
    elif option == 4:
        OpcaoBackup()
    elif option == 5:
        os.system('cls' if os.name == 'nt' else 'clear')

        return 0
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Opção indisponível")
        input("\nENTER para continuar")

        StartMenu()

StartMenu()