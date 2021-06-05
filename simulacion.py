from reloj import Reloj
from notifier import Notifier
from cliente import Cliente
from servidor import Servidor
from logger import Logger
import random as r
r.seed(a=12345)
# Turno de 6 horas = 360 minutos
iteraciones_reloj = 360
cantidad_clientes = 1

numeros_aleatorios_servidor = [ r.randint(0,99) for _ in range(iteraciones_reloj) ]
numeros_aleatorios_cliente = [ r.randint(0,99) for _ in range(iteraciones_reloj * cantidad_clientes) ]

reloj = Reloj()
notifier = Notifier()
logger = Logger(notifier)
#inicializo clientes
clientes = [Cliente(notifier, f"CLI{int(n)}", numeros_aleatorios_cliente[n*iteraciones_reloj:n*iteraciones_reloj+iteraciones_reloj]) for n in range(0,cantidad_clientes)]
servidor = Servidor(notifier, numeros_aleatorios_servidor)

while reloj.get_time() < iteraciones_reloj:
    notifier.send_event(event_name='RELOJ', event_data={'reloj': reloj.get_time()})
    reloj.advance()