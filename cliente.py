from notifier import Notifier

fda_tiempo_pregunta = [
    [ 0, 29, 1],
    [30, 79, 2],
    [80, 89, 3],
    [90, 94, 4],
    [95, 99, 6],
]

fda_cantidad_preguntas = [
    [ 0, 10, 1],
    [10, 19, 2],
    [20, 49, 3],
    [50, 79, 4],
    [80, 99, 6],
]

puntaje_review = [
    [ 0, 5, 5],
    [ 6, 10, 4],
    [ 11,15, 3],
    [ 16,22, 2],
    [ 23,99, 1],
]

class Cliente:
    def __init__(self, notifier:Notifier, nombre:str, numeros_aleatorios):
        super().__init__()
        self.notifier = notifier        
        self.pregunta_actual = None
        self.pregunta_enviada = False
        self.tiempo_llegada_pregunta = 0
        self.espera = 0
        self.iteraciones = 0
        self.nombre_base = nombre
        self.id = self.get_id()
        self.numeros_aleatorios = numeros_aleatorios
        self.cantidad_preguntas = self.get_cantidad_preguntas()
        self.notifier.subscribe(self)
    
    def receive_event(self, event_name, event_data):
        if event_name == 'RELOJ':
            if not self.pregunta_actual:
                self.programar_pregunta(event_data['reloj'])
            elif self.pregunta_actual['tiempo_llegada_pregunta'] == event_data['reloj']:
                self.pregunta_enviada = True
                self.notifier.send_event('ENVIO_PREGUNTA', self.pregunta_actual)

        if event_name == 'PREGUNTA_RESPONDIDA':
            if event_data['id_pregunta'] == self.pregunta_actual['id_pregunta']:
                self.cantidad_preguntas -= 1
                self.pregunta_enviada = False            
                self.espera += event_data['tiempo_respuesta_pregunta'] - self.tiempo_llegada_pregunta
                if self.cantidad_preguntas == 0:
                    data = {
                        'id_cliente': self.id,
                        'espera': self.espera,
                        'review': self.get_review()
                    }
                    self.notifier.send_event(event_name='CLIENTE_ATENDIDO', event_data=data)
                    self.reset_client()
                else:
                    self.pregunta_actual = None
    
    def programar_pregunta(self, tiempo_actual):
        self.pregunta_id = f"ID:{self.id}-PREG{self.cantidad_preguntas}"
        self.tiempo_llegada_pregunta = tiempo_actual + self.get_tiempo_pregunta()
        data = {
            'id_pregunta': self.pregunta_id,
            'id_cliente': self.id,
            'tiempo_llegada_pregunta': self.tiempo_llegada_pregunta,
        }
        self.pregunta_actual = data
    
    def get_tiempo_pregunta(self):
        numero = self.numeros_aleatorios.pop(0)
        for rango in fda_tiempo_pregunta:
            if numero >= rango[0] and numero <= rango[1]:
                return rango[2]
    
    def get_cantidad_preguntas(self):
        numero = self.numeros_aleatorios.pop(0)
        for rango in fda_cantidad_preguntas:
            if numero >= rango[0] and numero <= rango[1]:
                return rango[2]

    def get_id(self):
        return f"{self.nombre_base}:ITER{self.iteraciones}"

    def get_review(self):
        for rango in puntaje_review:
            if self.espera >= rango[0] and self.espera <= rango[1]:
                return rango[2]
    
    def reset_client(self):
        self.iteraciones += 1
        self.pregunta_actual = None
        self.pregunta_enviada = False
        self.tiempo_llegada_pregunta = 0
        self.espera = 0
        self.id = self.get_id()
        self.cantidad_preguntas = self.get_cantidad_preguntas()