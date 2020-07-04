from datetime import timedelta

from django.shortcuts import render
import dateutil.parser
# Create your views here.
from rest_framework import viewsets, filters, status, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.utils import timezone
from faceRest.filters import FilterSearch
from faceRest.utils import StandardResultsSetPagination
from faces.models import FaceDetected, FaceDataSet, Pointage
from faces.serializers import FaceDetectedSerializer, FaceDataSetSerializer, MoveFaceSerializer, PointageSerializer


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


class PointageViewSet(viewsets.ModelViewSet):
    queryset = Pointage.objects.all()
    serializer_class = PointageSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [FilterSearch, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['person__name', ]

    # filter_fields = ['label', 'label__isnull', 'instate']

    @action(detail=False, methods=['get'])
    def filter_date(self, request):
        # dateutil.parser.parse
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        date = request.GET.get('date')
        if date1:
            try:
                date1 = dateutil.parser.parse(date1)
                date2 = dateutil.parser.parse(date2)
            except ValueError:
                return Response("delete error", status=status.HTTP_400_BAD_REQUEST)
            else:
                queryset = Pointage.objects.filter(date_entree__range=[date1, date2])
        elif date:
            if date == 'today':
                queryset = Pointage.objects.filter(date_entree__gte=today)
            elif date == 'week':
                queryset = Pointage.objects.filter(date_entree__gte=today - timedelta(today.weekday()))
            elif date == 'month':
                queryset = Pointage.objects.filter(today.replace(day=1))
            elif date == 'year':
                queryset = Pointage.objects.filter(date_entree__gte=today.replace(day=1, month=1))
            else:
                return Response("delete error", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("delete error", status=status.HTTP_400_BAD_REQUEST)
        ser = PointageSerializer()

        return Response({"Nothing!"})


class FaceDataSetViewSet(viewsets.ModelViewSet):
    queryset = FaceDataSet.objects.all()
    serializer_class = FaceDataSetSerializer
    filter_backends = [FilterSearch, filters.SearchFilter, filters.OrderingFilter]

    # @api_view(['GET', 'POST'])
    @action(detail=False, methods=['post'])
    def move(self, request):
        serializer = MoveFaceSerializer(data=request.data)
        if serializer.is_valid():
            print("Serializer valid")
            serializer.save()
            return Response({"message": "Got some data!", "data": request.data})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
