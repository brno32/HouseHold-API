from django.db.models import (
    BooleanField,
    CharField,
    Model,
)


# Create your models here.
class Items(Model):

    name = CharField(max_length=30)
    category = CharField(max_length=30)
    isChecked = BooleanField(default=False)
    # group
