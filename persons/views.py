from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from faceRest.filters import FilterSearch
from .serializers import PersonSerializer, LabelSerializer
from .models import Person, Label


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, FilterSearch]
    search_fields = ['name', 'age']
    filter_fields = ['name', 'age', 'active']
    # permission_classes = [IsAuthenticated]


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    filter_backends = [FilterSearch]
    filter_fields = ['name']


class PersonDetail(viewsets.generics.GenericAPIView,
                   viewsets.mixins.RetrieveModelMixin
    , viewsets.mixins.DestroyModelMixin,
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
