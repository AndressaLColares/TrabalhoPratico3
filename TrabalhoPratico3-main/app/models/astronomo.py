from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField

class Astronomo(Document):
    nome = StringField(required=True)
    area_estudo = StringField()
    data_nascimento = DateTimeField()

    observacoes = ListField(ReferenceField('Observacao'))  # Relacionamento 1:N