from rest_framework.views import Request, Response, APIView, status
from django.shortcuts import get_object_or_404


from .models import Animals
from .serializers import AnimalsSerializer


class AnimalsView(APIView):
    def get(self, request: Request) -> Response:
        animals_query_set = Animals.objects.all()
        animals_serializer = AnimalsSerializer(animals_query_set, many=True)
        return Response(animals_serializer.data, status.HTTP_200_OK)

    
    def post(self, request: Request)-> Response:
        animals_serializer = AnimalsSerializer(data=request.data)
        animals_serializer.is_valid(raise_exception=True)
        animals_serializer.save()

        return Response(animals_serializer.data, status.HTTP_201_CREATED)

class AnimalDetailsView(APIView):
    def patch(self, request: Request, animal_id: int):
        animals_obj = get_object_or_404(Animals, id=animal_id)

        animals_serializer = AnimalsSerializer(animals_obj, data=request.data, partial=True)
        animals_serializer.is_valid(raise_exception=True)
        animals_serializer.save()

        return Response(animals_serializer.data, status.HTTP_200_OK)

    def get(self, request: Request, animal_id: int):
        animals_obj = get_object_or_404(Animals, id=animal_id)
        animals_serializer = AnimalsSerializer(animals_obj)
        
        return Response(animals_serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, animal_id: int) -> Response:
        animals_obj = get_object_or_404(Animals, id=animal_id)

        animals_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    


