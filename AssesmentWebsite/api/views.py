from .models import Demographic
from .serializers import *
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


latest_id = None
question_bank_id = None
code_id = None

@api_view(['GET', 'POST', 'DELETE'])
def demographic(request, pk=None):
 global latest_id
 print(request.user.id)
 if request.method == 'GET': 
  id = pk
  if id is not None:
   stu = Demographic.objects.get(uid=id)
   serializer = DemographicSerializer(stu)
   return Response(serializer.data)

  stu = Demographic.objects.all()
  serializer = DemographicSerializer(stu, many=True)
  return Response(serializer.data)

 if request.method == 'POST':
  serializer = DemographicSerializer(data=request.data)
  if serializer.is_valid():
   serializer.save()
   latest_id = Demographic.objects.order_by('-uid')[0].uid
   return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 if request.method == 'DELETE':
  id = pk
  stu = Demographic.objects.get(uid=id)
  stu.delete()
  return Response({'msg':'Data Deleted'})

@api_view(['GET', 'POST', 'DELETE'])
def expertise(request, pk=None):
 global latest_id
 if request.method == 'GET': 
  id = pk
  if id is not None:
   stu = Expertise.objects.get(eid=id)
   serializer = ExpertiseSerializer(stu)
   return Response(serializer.data)

  stu = Expertise.objects.all()
  serializer = ExpertiseSerializer(stu, many=True)
  return Response(serializer.data)

 if request.method == 'POST':
  print(request.data)
  dic = request.data
  dic['fuid'] = latest_id
  serializer = ExpertiseSerializer(data=dic)
  print(latest_id)
  print(dic)
  if serializer.is_valid():
   serializer.save()
  #  latest_id = Demographic.objects.order_by(by = 'uid')[0].uid
   return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 if request.method == 'DELETE':
  id = pk
  stu = Expertise.objects.get(eid=id)
  stu.delete()
  return Response({'msg':'Data Deleted'})


@api_view(['POST'])
@csrf_exempt
def login1(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        user_name = pythondata.get('username', None)
        user_password = pythondata.get('password', None)
        user = authenticate(request,username=user_name, password=user_password)
        
        if user is not None:
            token,created=Token.objects.get_or_create(user=user)
            login(request, user)
            json_data = json.dumps({"ans":"login is successful",
            "token":token.key,"created":created})
            return HttpResponse(json_data, content_type='application/json')
        else:
            json_data = json.dumps({"ans":"login is unsuccessful"})
            return HttpResponse(json_data, content_type='application/json')

    return HttpResponse(json.dumps({"result":"Please login yourself"}), content_type='application/json')
  
  
@api_view(['GET', 'POST', 'DELETE'])
def questionbank(request, pk=None):
 global question_bank_id
 if request.method == 'GET': 
  id = pk
  if id is not None:
   stu = QuestionBank.objects.get(qbid=id)
   serializer = QuestionBankSerializer(stu)
   return Response(serializer.data)

  stu = QuestionBank.objects.all()
  serializer = QuestionBankSerializer(stu, many=True)
  return Response(serializer.data)

 if request.method == 'POST':
  print("hello post ")
  print(request.data)
  dic = request.data
  dic['aid'] = request.user.id
  serializer = QuestionBankSerializer(data=dic)
  print(latest_id)
  print(dic)
  if serializer.is_valid():
   serializer.save()
   question_bank_id = QuestionBank.objects.order_by('-qbid')[0].qbid
   return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 if request.method == 'DELETE':
  id = pk
  stu = QuestionBank.objects.get(qbid=id)
  stu.delete()
  return Response({'msg':'Data Deleted'})

@api_view(['GET', 'POST', 'DELETE'])
def code(request, pk=None):
 global code_id
 if request.method == 'GET': 
  id = pk
  if id is not None:
   stu = Code.objects.get(cid=id)
   serializer = CodeSerializer(stu)
   return Response(serializer.data)

  stu = Code.objects.all()
  serializer = CodeSerializer(stu, many=True)
  return Response(serializer.data)

 if request.method == 'POST':
  print("hello post ")
  print("request data",request.data)
  dic = request.data
  dic['fqbid'] = question_bank_id
  serializer = CodeSerializer(data=dic)
  print("question bank id",question_bank_id)
  print("code data",dic)
  if serializer.is_valid():
   serializer.save()
   code_id = Code.objects.order_by('-cid')[0].cid
   return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 if request.method == 'DELETE':
  id = pk
  stu = code.objects.get(cid=id)
  stu.delete()
  return Response({'msg':'Data Deleted'})


@api_view(['GET', 'POST', 'DELETE'])
def question(request, pk=None):
 if request.method == 'GET': 
  id = pk
  if id is not None:
   stu = Question.objects.get(qid=id)
   serializer = QuestionSerializer(stu)
   return Response(serializer.data)

  stu = Question.objects.all()
  serializer = QuestionSerializer(stu, many=True)
  return Response(serializer.data)

 if request.method == 'POST':
  print("hello post ")
  print("request data",request.data)
  dic = request.data
  print("code id", code_id)
  dic['fcid'] = code_id
  serializer = QuestionSerializer(data=dic)
  print("question id",code_id)
  print("question data",dic)
  if serializer.is_valid():
   serializer.save()
   return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 if request.method == 'DELETE':
  id = pk
  stu = Question.objects.get(qid=id)
  stu.delete()
  return Response({'msg':'Data Deleted'})