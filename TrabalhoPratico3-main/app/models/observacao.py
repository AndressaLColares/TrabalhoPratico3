from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField

class Observacao(Document):
    datahora = DateTimeField(required=True)
    objeto_id = StringField()
    observador = StringField()
    localizacao = StringField()
    propriedades_observadas = StringField()

    telescopio = ReferenceField('Telescopio')  # Relacionamento 1:N
    astronomo = ReferenceField('Astronomo')   # Relacionamento 1:N
    fenomenos = ListField(ReferenceField('FenomenoCelestial'))  # Relacionamento N:N