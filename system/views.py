from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from facereco.train.MFaceNet_LoadModel_SVM import pre_train_information, train
from facereco import write_conf, get_conf

@api_view(['GET'])
def train_view(request):
    result = train()
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
