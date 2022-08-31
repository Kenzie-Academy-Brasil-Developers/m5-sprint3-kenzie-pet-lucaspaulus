from django.db import models

# Create your models here.
class Genders(models.TextChoices):
    MALE = 'Macho'
    FEMALE = 'Femea'
    UNDEFINED = "Não Informado"


class Animals(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=15, choices=Genders.choices, default=Genders.UNDEFINED)
    # FK 1:N
    groups = models.ForeignKey('groups.Groups', on_delete=models.CASCADE, related_name='animals')
    traits = models.ManyToManyField('traits.Traits', related_name='traits')

    def __repr__(self) -> str:
        return f"<Animals {self.name} - {self.age}>"