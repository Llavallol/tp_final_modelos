from notifier import Notifier
import time

class Logger:
    def __init__(self, notifier:Notifier):
        super().__init__()
        self.notifier = notifier
        self.notifier.subscribe(self)
        self.filename = f"{int(time.time())}.csv"
        with open(self.filename, "w+") as f:
            f.write('CLIENTE,ESPERA_TOTAL_CLIENTE,REVIEW,ENVIA_PREGUNTA,SERVIDOR_PREPARA_RESPUESTA,SERVIDOR_RESPONDE,ESPERA_CLIENTE,SERVIDOR_OCUPADO\n')
    
    def receive_event(self, event_name, event_data):
        if event_name == 'PREGUNTA_RESPONDIDA':
            envia_pregunta = event_data['tiempo_llegada_pregunta']
            servidor_prepara = event_data['tiempo_respuesta_inicio']
            servidor_responde = event_data['tiempo_respuesta_pregunta']
            espera_cliente = servidor_responde - envia_pregunta
            servidor_ocupado = servidor_responde - servidor_prepara + 1
            with open(self.filename, "a+") as f:
                f.write(f"{event_data['id_cliente']},,,{envia_pregunta},{servidor_prepara},{servidor_responde},{espera_cliente},{servidor_ocupado}\n")
        elif event_name == 'CLIENTE_ATENDIDO':
             with open(self.filename, "a+") as f:
                f.write(f"{event_data['id_cliente']},{event_data['espera']},{event_data['review']},,,,,,\n")