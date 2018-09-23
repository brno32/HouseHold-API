from django.contrib.auth.models import Group
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    ForeignKey,
    Model,
)

Group.add_to_class('password', CharField(max_length=180, default='password'))


class Item(Model):

    name = CharField(max_length=30)
    category = CharField(max_length=30)
    isChecked = BooleanField(default=False)
    group = ForeignKey(Group, null=True, on_delete=CASCADE)

    def __str__(self):
        return self.name
