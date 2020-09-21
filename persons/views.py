from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from faceRest.filters import FilterSearch
from .serializers import PersonSerializer, LabelSerializer, TemperatureSerializer, PersonTempSerializer
from .models import Person, Label, Temperature


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.OrderingFilter, FilterSearch]
    search_fields = ['name', 'age']
    filter_fields = ['name', 'age', 'active']
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path="available")
    def available_persons(self, request):
        queryset = Person.objects.filter(available=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    filter_backends = [FilterSearch]
    filter_fields = ['name']


class TemperatureViewSet(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class PersonTempViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonTempSerializer


class PersonDetail(viewsets.generics.GenericAPIView,
                   viewsets.mixins.RetrieveModelMixin,
                   viewsets.mixins.DestroyModelMixin,
                   viewsets.mixins.UpdateModelMixin):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# @api_view(['GET'])
def persons_list(request):
    if request.method == 'GET':
        persons = Person.objects.all()
        persons_serializer = PersonSerializer(persons, many=True)
        return JsonResponse(persons_serializer.data, safe=False)
