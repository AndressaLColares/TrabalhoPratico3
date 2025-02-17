from mongoengine import Document, StringField, FloatField, DateTimeField, ReferenceField, ListField

class Estrela(Document):
    nome = StringField(required=True)
    tipo_espectral = StringField()
    magnitude = FloatField()
    distancia = FloatField()
    luminosidade = FloatField()
    temperatura = FloatField()
    idade = FloatField()

    planetas = ListField(ReferenceField('Planeta'))  # Relacionamento 1:N
    exoplanetas = ListField(ReferenceField('Exoplaneta'))  # Relacionamento 1:N