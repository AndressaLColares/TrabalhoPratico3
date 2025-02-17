from mongoengine import Document, StringField, FloatField, DateTimeField, ReferenceField

class Telescopio(Document):
    nome = StringField(required=True)
    tipo = StringField()
    localizacao = StringField()
    diametro = FloatField()
    data_lancamento = DateTimeField()

    observacao = ReferenceField('Observacao')  # Relacionamento 1:1
