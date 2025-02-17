from mongoengine import Document, StringField, FloatField, DateTimeField, ReferenceField, ListField

class Planeta(Document):
    nome = StringField(required=True)
    tipo = StringField()
    periodo_orbital = FloatField()
    distancia_da_estrela = FloatField()
    raio = FloatField()
    massa = FloatField()
    composicao_atmosferica = StringField()
    data_descoberta = DateTimeField()

    estrela = ReferenceField('Estrela')  # Relacionamento 1:N
    exoplanetas = ListField(ReferenceField('Exoplaneta'))  # Relacionamento N:N