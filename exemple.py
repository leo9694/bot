
from iqoptionapi.stable_api import IQ_Option
import time, json
from datetime import datetime
from dateutil import tz

API = IQ_Option('leop.gabriel8@gmail.com', 'Nossamae123')
API.connect()
API.change_balance('PRACTICE')
while True:
    if API.check_connect() == False:
        print('Erro ao se conectar')
        API.connect()
    else:
        print('Conectado com sucesso')
        break

    time.sleep(1)



def perfil(): # Função para capturar informações do perfil
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))

    return perfil

    '''
        name
        first_name
        last_name
        email
        city
        nickname
        currency
        currency_char 
        address
        created
        postal_index
        gender
        birthdate
        balance
    '''


x = perfil()
banca = API.get_balance()



######################### IMPRESSAO ########################

print(x['name'])
print(banca)


def timestamp_converter(x): # Função para converter timestamp
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]
	

'''
	Para pegar somente a quantia da sua banca utilize: banca = API.get_balance()
'''

print(API.get_balance())

par = 'EURUSD'

vela = API.get_candles(par, 60,1, time.time())  
print (vela)
print(timestamp_converter(vela[0]['from']))

#historico velas
'''total = []
tempo = time.time()

for i in range(2):
    X = API.get_candles(par,60,1000,tempo)
    total=X+total
    tempo = int(X[0]['from'])-1
for velas in total:
    print(timestamp_converter(velas['from']))'''


#tempo real


par= 'EURUSD'
entrada = 2 
direcao ='call'
timeframe = 1

status, id =API.buy(entrada, par, direcao, timeframe)

if status:
    print(API.check_win_v3(id))