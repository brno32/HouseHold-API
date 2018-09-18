from django.contrib.auth.models import Group
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    ForeignKey,
    Model,
)


class Item(Model):

    name = CharField(max_length=30)
    category = CharField(max_length=30)
    isChecked = BooleanField(default=False)
    group = ForeignKey(Group, null=True, on_delete=CASCADE)

    def __str__(self):
        return self.name
