import math
from webbrowser import get
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from groups.serializers import GroupsSerializer
from traits.serializers import TraitsSerializer
from groups.models import Groups
from traits.models import Traits
from .models import Genders, Animals



class AnimalsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    age_in_human_years = serializers.SerializerMethodField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Genders.choices, default=Genders.UNDEFINED)
    traits  = TraitsSerializer(many=True)
    groups = GroupsSerializer()
    
    

    def create(self,validate_data: dict):
        group_To_Create = validate_data.pop("groups")
        groupAll = Groups.objects.get_or_create(**group_To_Create)[0]
        traits_to_Create = validate_data.pop('traits')

        createAnimal = Animals.objects.create( **validate_data, groups = groupAll)

        for trait in traits_to_Create:
            traits_to_add = Traits.objects.get_or_create(**trait)[0]
            createAnimal.traits.add(traits_to_add)
        return createAnimal

    def update(self, instance: Animals, validated_data: dict):
        non_editable_keys = ("sex", "groups", "traits")
        errors = {}
         
        for key, value in validated_data.items():
            if key in non_editable_keys:
                errors.update({key: f"You can not update {key} property."})
                continue
            
            setattr(instance, key , value)
        
        if errors:
            raise ValidationError(errors)
        
        instance.save()
        
        return instance

    def get_age_in_human_years(self, obj: Animals):
        animal_age  = obj.age + 31
        round_num = round(math.log(animal_age))
        age_in_human = 16 * round_num
        return age_in_human
