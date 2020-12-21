#MARTIN GALE SERÁ SEMPRE O DOBRO

from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time
import sys

def stop(lucro, gain, loss):
	if lucro <= float('-' + str(abs(loss))):
		print('Stop Loss batido!')
		sys.exit()
		
	if lucro >= float(abs(gain)):
		print('Stop Gain Batido!')
		sys.exit()

def Martingale(valor):
	return valor * 2

#TESTE
#VERIFICANDO SE EXISTEM 5 VELAS IDENTICAS
def PossoOperar():
	velas = API.get_candles(par, 60, 5, time.time())
	velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
	velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
	velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
	velas[3] = 'g' if velas[3]['open'] < velas[3]['close'] else 'r' if velas[3]['open'] > velas[3]['close'] else 'd'
	velas[4] = 'g' if velas[4]['open'] < velas[4]['close'] else 'r' if velas[4]['open'] > velas[4]['close'] else 'd'

	cores = velas[0] + ' ' + velas[1] + ' ' + velas[2] + ' ' + velas[3] + ' ' + velas[4]	

	#Checando se existem uma sequeencia de 5 velas iguais
	if(cores.count('g') == 5) or (cores.count('r') == 5) or (cores.count('d') == 5):
		return False
	else:
		return True

#Função que deixa o Martin Gale pausado até surgir uma oportunidade de retornar
def PausarMg():
	print('\n5 velas iguais foram indentificadas... pausando o MartinGale')
	while True:
		time.sleep(60) 
		if (PossoOperar()):
			print('\nNova sequencia MHI identificada... retornando o MartinGale...')
			break
		else:
			print('\nAguardando nova sequencia MHI...')

while True:
	login = input('Informe o seu login: ')
	senha = input('Informe sua senha: ')
	API = IQ_Option(login, senha)
	API.connect()
	if API.check_connect():
		print('Conectado com sucesso!')
		break
	else:
		print(' Erro ao conectar... Digite novamente...')

API.change_balance('PRACTICE') # PRACTICE / REAL

while True:
	try:
		operacao = int(input('\n Deseja operar na\n  1 - Digital\n  2 - Binaria\n  :: '))
		
		if operacao > 0 and operacao < 3 : break
	except:
		print('\n Opção invalida')

while True:
	try:
		tipo_mhi = int(input(' Deseja operar a favor da\n  1 - Minoria\n  2 - Maioria\n  :: '))
		
		if tipo_mhi > 0 and tipo_mhi < 3 : break
	except:
		print('\n Opção invalida')

par = input(' Indique uma paridade para operar: ').upper()
valor_entrada = float(input(' Indique um valor para entrar: '))
valor_entrada_b = float(valor_entrada)

martingale = int(input(' Indique a quantia de martingales: '))
martingale += 1

stop_loss = float(input(' Indique o valor de Stop Loss: '))
stop_gain = float(input(' Indique o valor de Stop Gain: '))

lucro = 0
max_mg = 0 #Variavel responsavel por guardar a quantidade máxima de Martin Gales ocorridos
qtd_mg = 0

while True:
	minutos = float(((datetime.now()).strftime('%M.%S'))[2:])
	entrar = True if (minutos >= 0.58) else False
	
	#Teste
	#VErificar se existe muita sequencia de velas identicas antes de fazer a operacao
	if entrar:
		entrar = PossoOperar()

	print('Hora de entrar?',entrar,'/ Minutos:',minutos, '/ Lucro:', round(lucro, 2), '/ Max MG:', max_mg, ':',qtd_mg,'x')

	if entrar:
		print('\n\nIniciando operação!')
		dir = False
		print('Verificando cores..', end='')
		velas = API.get_candles(par, 60, 3, time.time())
		
		velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
		velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
		velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
		
		cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]		
		print(cores)
	
		if cores.count('g') > cores.count('r') and cores.count('d') == 0 : dir = ('put' if tipo_mhi == 1 else 'call')
		if cores.count('r') > cores.count('g') and cores.count('d') == 0 : dir = ('call' if tipo_mhi == 1 else 'put')

		if dir:
			print('Direção:',dir)
			valor_entrada = valor_entrada_b
			for i in range(martingale):

				if i != 0 and i > max_mg: 
					max_mg = i
					qtd_mg = 0
				if i != 0 and i == max_mg: qtd_mg += 1
					
				operar = PossoOperar() #Verificando se ainda esta dentro das regras da estrategia MHI...
				if operar == False: #Verifico se existe ou não uma sequencia de velas iguais
					PausarMg()
							
				status,id = API.buy_digital_spot(par, valor_entrada, dir, 1) if operacao == 1 else API.buy(valor_entrada, par, dir, 1)
				
				if status:
					while True:
						try:
							status,valor = API.check_win_digital_v2(id) if operacao == 1 else True, API.check_win_v3(id)
						except:
							status = True
							valor = 0
						
						if status:
							valor = valor if valor > 0 else float('-' + str(abs(valor_entrada)))
							lucro += round(valor, 2)
							
							print('Resultado operação: ', end='')
							print('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2) ,'/', round(lucro, 2),('/ '+str(i)+ ' GALE' if i > 0 else '' ))
							
							valor_entrada = Martingale(valor_entrada)
							
							stop(lucro, stop_gain, stop_loss)
							
							break

					if valor > 0: 
						break
					
				else:
					print('\nERRO AO REALIZAR OPERAÇÃO\n\n')

	time.sleep(0.5)