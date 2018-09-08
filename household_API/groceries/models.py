from django.db.models import (
    BooleanField,
    CharField,
    Model,
)


class Item(Model):

    name = CharField(max_length=30)
    category = CharField(max_length=30)
    isChecked = BooleanField(default=False)
    # group

    def __str__(self):
        return self.name
