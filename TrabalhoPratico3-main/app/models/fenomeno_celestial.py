from mongoengine import Document, StringField, ReferenceField, ListField

class FenomenoCelestial(Document):
    nome = StringField(required=True)
    tipo = StringField()
    descricao = StringField()

    observacoes = ListField(ReferenceField('Observacao'))  # Relacionamento N:N