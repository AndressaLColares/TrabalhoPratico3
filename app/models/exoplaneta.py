from mongoengine import Document, StringField, ReferenceField, ListField


class Exoplaneta(Document):
    nome = StringField(required=True)

    estrela = ReferenceField('Estrela')  # Relacionamento N:1
    planetas = ListField(ReferenceField('Planeta'))  # Relacionamento N:N