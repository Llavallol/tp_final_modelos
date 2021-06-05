from notifier import Notifier

fda_tiempo_resolucion = [
    [ 0,  39, 1],
    [40, 69, 2],
    [70, 89, 3],
    [90, 99, 4],
]

class Servidor:
    def __init__(self, notifier:Notifier, numeros_aleatorios):
        super().__init__()
        self.notifier = notifier
        self.preguntas = []
        self.pregunta_en_resolucion = None
        self.notifier.subscribe(self)
        self.numeros_aleatorios = numeros_aleatorios
    
    def receive_event(self, event_name, event_data):
        # Cuando llega una pregunta la meto en la lista de pendientes
        if event_name == 'ENVIO_PREGUNTA':
            self.preguntas.append(event_data)
        # Cuando llama el reloj si no estás atendiendo, atendé una pregunta. Si estás atendiendo y terminaste una pregunta, enviá la respuesta.
        elif event_name == 'RELOJ':
            if not self.pregunta_en_resolucion:
                if self.preguntas:
                    self.pregunta_en_resolucion = self.preguntas.pop(0)
                    self.pregunta_en_resolucion['tiempo_respuesta_inicio'] = event_data['reloj']
                    self.pregunta_en_resolucion['tiempo_respuesta_pregunta'] = event_data['reloj'] + self.get_tiempo_resolucion()
            elif self.pregunta_en_resolucion['tiempo_respuesta_pregunta'] == event_data['reloj']:
                self.notifier.send_event(event_name='PREGUNTA_RESPONDIDA', event_data=self.pregunta_en_resolucion)
                self.pregunta_en_resolucion = None


    def get_tiempo_resolucion(self):
        numero = self.numeros_aleatorios.pop(0)
        for rango in fda_tiempo_resolucion:
            if numero >= rango[0] and numero <= rango[1]:
                return rango[2]