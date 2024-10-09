from math import log
import sys
from random import randint
from time import time
from Enderecos.importante import importante

def Abrir_arquivo(entrada,lista):
	"""
	Abre os Arquivos e guarda os endereços
	"""
	try:
		with open(entrada, 'rb') as arquivo:
			while True:
				conteudo = arquivo.read(4)  # Lê o conteúdo completo do arquivo
				if(not conteudo):
					break
				else:
					inteiro = int.from_bytes(conteudo, byteorder='big', signed=False)
					lista.append(inteiro)

	except FileNotFoundError:
		print('Arquivo não encontrado!')
	


def Com_flag():
	pass

def Sem_flag():
	pass



class Cache:
	def __init__(self, nsets, bsize, assoc, repl):
		self.nsets=nsets
		self.bsize=bsize
		self.assoc=assoc
		self.repl=repl.upper()
		self.tamanho= nsets*bsize*assoc
		self.blocos=nsets*assoc
		self.blocos_ocupados=0
		self.bits_offset = int(log(bsize,2))
		self.bits_indice = int(log(nsets,2))
		self.bits_tag = 32 - self.bits_offset - self.bits_indice
		self.validade = [[0 for c in range(0, self.assoc)] for l in range(0, self.nsets)] # list compreension
		self.tag = [[-1 for c in range(0, self.assoc)] for l in range(0, self.nsets)] # list compreension
		self.fila_acessos = [[] for l in range(0, self.nsets)]  # list compreension
	
	def Printf(self, lst: list[list[int]])->None:
		for c in lst:
			print(c)
		print('\n\n\n')

	def PegarDoRandom(self):
		return randint(0, self.assoc-1)
	
	def PegarDaFila(self, indice: int, tag: int) -> int:
		try:
			entrada = self.tag[indice].index(self.fila_acessos[indice][0])
			self.fila_acessos[indice].pop(0)
			self.fila_acessos[indice].append(tag)
			return entrada
		except ValueError:
			return 0 # Nunca acontece...


	def Acessar_Endereco(self, endereco:int) -> None:
		teve_miss = True

		# Pega o tag e o indice do endereço
		tag = endereco >> (self.bits_indice + self.bits_offset)
		indice = (endereco >> self.bits_offset) & (2**self.bits_indice -1)
		#print('indice: {}'.format(indice))
		#print('tag: {}'.format(tag))

		# Permite o acesso as variáveis globais
		global hits
		global misses_compulsorio
		global misses_capacidade
		global misses_conflito
		
		#print('capacidade {}/{}'.format(self.blocos_ocupados, self.blocos))

		# Testa se os bits válidos geram um hit
		for c in range(0, self.assoc):
			if(self.validade[indice][c] == 1 and tag == self.tag[indice][c]):
				teve_miss = False
				hits += 1
				#print('hit')

				# Atualiza o tag na fila caso usando "L"
				if self.repl == 'L':
					self.fila_acessos[indice].remove(tag)
					self.fila_acessos[indice].append(tag)
		
		# Se não teve hit, verifica o tipo de miss
		if teve_miss:
			# Se há entrada livre => miss compulsório
			if 0 in self.validade[indice]:
				#print("miss compulsório")
				misses_compulsorio+=1
				self.blocos_ocupados+=1

				# Insere o tag na fila se usando "L" ou "R"
				if self.repl == "F" or self.repl == "L":
					self.fila_acessos[indice].append(tag)
					#print(self.fila_acessos[indice])

				# Coloca o end na primeira posição disponível
				for i in range(0, self.assoc):
					if self.validade[indice][i] == 0:
						self.validade[indice][i] = 1
						self.tag[indice][i] = tag
						break

			# Se a cache está cheia => miss capacidade
			elif self.blocos_ocupados == self.blocos:
				#print("miss de capacidade")
				misses_capacidade += 1
				if(self.assoc == 1):
					self.validade[indice][0] = 1
					self.tag[indice][0] = tag
				elif self.repl == "R":
					entrada = self.PegarDoRandom()
					self.validade[indice][entrada] = 1
					self.tag[indice][entrada] = tag
				elif self.repl == "F" or self.repl == "L":
					entrada = self.PegarDaFila(indice, tag)
					self.validade[indice][entrada] = 1
					self.tag[indice][entrada] = tag
					#print(self.fila_acessos[indice])
				
			# Senão => miss conflito
			else:
				#print("miss de conflito")
				misses_conflito += 1
				if(self.assoc == 1):
					self.validade[indice][0] = 1
					self.tag[indice][0] = tag
				elif self.repl == "R":
					entrada = self.PegarDoRandom()
					self.validade[indice][entrada] = 1
					self.tag[indice][entrada] = tag
				elif self.repl == "F" or self.repl == "L":
					entrada = self.PegarDaFila(indice, tag)
					self.validade[indice][entrada] = 1
					self.tag[indice][entrada] = tag
					#print(self.fila_acessos[indice])



def main():
	if (len(sys.argv) != 7):
		print("Numero de argumentos incorreto. Utilize:")
		print("python cache_simulator.py <nsets> <bsize> <assoc> <repl> <flag_saida> arquivo_de_entrada")
		exit(1)

	# Guarda a flag de saída
	flag = int(sys.argv[5])

	# Lê o arquivo de entrada e guarda os endereços
	arquivoEntrada = sys.argv[6]
	enderecos=[]
	Abrir_arquivo('Enderecos/' + arquivoEntrada, enderecos)
	
	# Cria um objeto cache com os parâmetros da cache
	cache = Cache(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])

															#<--------------
	# Acessas os endereços um a um
	inicio = time()
	global acessos
	for i in range(0,len(enderecos)):
		acessos += 1
		#print('endereço: {}'.format(enderecos[i]))
		cache.Acessar_Endereco(enderecos[i])
		#print('='*10)

	fim = time()
	
	# Saída

	print('tempo de execução: {:.2f}'.format(fim-inicio))
	print(acessos, end=" ")
	print('{:.4f}'.format(hits/acessos), end=" ")
	misses = misses_compulsorio+misses_capacidade+misses_conflito ## <== Aqui tava errado miss de capacidade 2x
	print('{:.4f}'.format(misses/acessos), end=" ")
	print(f"{misses_compulsorio/misses:.2f}", end=" ")		
	print('{:.2f}'.format(misses_capacidade/misses), end=" ")		
	print(f"{misses_conflito/misses:.2f}", end="\n")
	#importante()				
															 
															#<--------------

acessos=0
hits=0
misses_compulsorio = 0
misses_conflito=0
misses_capacidade=0

if __name__ == '__main__':
	main()



# python cache_simulator.py <nsets> <bsize> <assoc> <repl> <flag_saida> arquivo_de_entrada

# Exemplo 1
# python cache_simulator.py 256 4 1 R 1 bin_100.bin

# Exemplo 2
# python cache_simulator.py 128 2 4 R 1 bin_1000.bin

# Exemplo 3
# python cache_simulator.py 16 2 8 R 1 bin_10000.bin

# Exemplo 4
# python cache_simulator.py 512 8 2 R 1 vortex.in.sem.persons.bin

# Exemplo 5
# python cache_simulator.py 1 4 32 R 1 vortex.in.sem.persons.bin

# Exemplo 6
# python cache_simulator.py 2 1 8 R 1 bin_100.bin

# Exemplo 7
# python cache_simulator.py 2 1 8 L 1 bin_100.bin

# Exemplo 8
# python cache_simulator.py 2 1 8 F 1 bin_100.bin

# Exemplo 9
# python cache_simulator.py 1 4 32 R 1 vortex.in.sem.persons.bin

# Exemplo 10
# python cache_simulator.py 1 4 32 L 1 vortex.in.sem.persons.bin

# Exemplo 11
# python cache_simulator.py 1 4 32 F 1 vortex.in.sem.persons.bin