from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from facereco.train.MFaceNet_LoadModel_SVM import pre_train_information, total_train
from facereco import write_conf, get_conf
from psutil import process_iter
from persons.models import Person
from faces.models import FaceDetected, FaceDataSet, Pointage


def facereco_is_running():
    for p in process_iter(["name"]):
        if p.info["name"] == "maincapture":
            return True
    return False


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def dashboard_view(request):
    result = {}
    result["persons"] = Person.objects.count()
    result["pointage"] = Pointage.objects.count()
    result["detected"] = FaceDetected.objects.count()
    result["train"] = FaceDataSet.objects.filter(dataset_type='Train').count()
    result["test"] = FaceDataSet.objects.filter(dataset_type='Test').count()
    return Response(result)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def running_view(request):
    result = facereco_is_running()
    # json_result = JSONParser().parse(result)
    # snippets = Snippet.objects.all()
    # serializer = SnippetSerializer(snippets, many=True)
    return Response(result)


@api_view(['GET'])
def train_view(request):
    result = total_train()
    return Response(result)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def train_info_view(request):
    result = pre_train_information()
    # json_result = JSONParser().parse(result)
    # snippets = Snippet.objects.all()
    # serializer = SnippetSerializer(snippets, many=True)
    return Response(result)

@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
def conf_view(request):
    if request.method == 'POST':
        print('POST')
        try :
            write_conf(**request.data)
            return Response({'method': 'POST'})
        except Exception as e:
            print(e)
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(get_conf())
    write_conf(request.data)
    # json_result = JSONParser().parse(result)
    # snippets = Snippet.objects.all()
    # serializer = SnippetSerializer(snippets, many=True)
