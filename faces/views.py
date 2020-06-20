from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from faceRest.filters import FilterSearch
from faceRest.utils import StandardResultsSetPagination
from faces.models import FaceDetected, FaceDataSet
from faces.serializers import FaceDetectedSerializer, FaceDataSetSerializer, MoveFaceSerializer


class FaceDetectedViewSet(viewsets.ModelViewSet):
    queryset = FaceDetected.objects.all()
    serializer_class = FaceDetectedSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [FilterSearch, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['label__name', ]
    # filter_fields = ['label', 'label__isnull', 'instate']

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        # self.queryset.
        if self.queryset.delete():
            return Response({"message": "Got some data!", "data": request.data})
        else:
            return Response("delete error", status=status.HTTP_400_BAD_REQUEST)


class FaceDataSetViewSet(viewsets.ModelViewSet):
    queryset = FaceDataSet.objects.all()
    serializer_class = FaceDataSetSerializer
    filter_backends = [FilterSearch, filters.SearchFilter, filters.OrderingFilter]

    # @api_view(['GET', 'POST'])
    @action(detail=False, methods=['post'])
    def move(self, request):
        serializer = MoveFaceSerializer(data = request.data)
        if serializer.is_valid():
            print("Serializer valid")
            serializer.save()
            return Response({"message": "Got some data!", "data": request.data})
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)