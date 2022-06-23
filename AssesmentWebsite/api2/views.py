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
import collections
import csv
import pandas as pd


latest_id = None
question_bank_id = None
question_bank_level_id = None
code_id = None
evaluation_id = None
questionbankevaluation_id = None



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

@api_view(['GET', 'POST','PUT', 'DELETE'])
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
  
 if request.method == 'PUT':
    id = pk
    # print("id",id)
    stu = Expertise.objects.get(eid=id)
    serializer = ExpertiseSerializer(stu, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response({'msg':'Data Updated'})
    return Response(serializer.errors)


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
  # dic['aid'] = request.user.id
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
def questionbanklevel(request, pk=None):
 global question_bank_level_id
 if request.method == 'GET': 
  id = pk
  if id is not None:
   stu = QuestionBankLevel.objects.get(qblid=id)
   serializer = QuestionBankLevelSerializer(stu)
   return Response(serializer.data)

  stu = QuestionBankLevel.objects.all()
  serializer = QuestionBankLevelSerializer(stu, many=True)
  return Response(serializer.data)

 if request.method == 'POST':
  print("hello post ")
  print(request.data)
  dic = request.data
  dic['fqbid'] = question_bank_id
  serializer = QuestionBankLevelSerializer(data=dic)
  print(latest_id)
  print(dic)
  if serializer.is_valid():
   serializer.save()
   question_bank_level_id = QuestionBankLevel.objects.order_by('-qblid')[0].qblid
   return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 if request.method == 'DELETE':
  id = pk
  stu = QuestionBankLevel.objects.get(qblid=id)
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
  dic['fqblid'] = question_bank_level_id
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

@api_view(['GET', 'POST', 'DELETE'])
def evaluation(request, pk=None):
 global evaluation_id
 if request.method == 'GET': 
  id = pk
  if id is not None:
   stu = Evaluation.objects.get(evid=id)
   serializer = EvaluationSerializer(stu)
   return Response(serializer.data)

  stu = Evaluation.objects.all()
  serializer = EvaluationSerializer(stu, many=True)
  return Response(serializer.data)

 if request.method == 'POST':
  print("hello post ")
  print("request data",request.data)
  dic = request.data
  print("user id", latest_id)
  dic['ffuid'] = latest_id
  questionbanklang = Expertise.objects.get(fuid=latest_id).programming_language
  dic['ffqbid'] = QuestionBank.objects.get(admin_programming_language = questionbanklang).qbid
  serializer = EvaluationSerializer(data=dic)
  print("user id",latest_id)
  print("evaluation data",dic)
  if serializer.is_valid():
   serializer.save()
   evaluation_id = Evaluation.objects.order_by('-evid')[0].evid
   return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 if request.method == 'DELETE':
  id = pk
  stu = Evaluation.objects.get(evid=id)
  stu.delete()
  return Response({'msg':'Data Deleted'})

# @api_view(['GET', 'POST', 'DELETE'])
# def questionbankevaluation(request, pk=None):
#  global questionbankevaluation_id
#  if request.method == 'GET': 
#   id = pk
#   if id is not None:
#    stu = QuestionBankEvaluation.objects.get(evqbid=id)
#    serializer = QuestionBankEvaluationSerializer(stu)
#    return Response(serializer.data)

#   stu = QuestionBankEvaluation.objects.all()
#   serializer = QuestionBankEvaluationSerializer(stu, many=True)
#   return Response(serializer.data)

#  if request.method == 'POST':
#   print("hello post ")
#   print("request data",request.data)
#   dic = request.data
#   print("evaluaton id", evaluation_id)
#   dic['fevid'] = evaluation_id 
#   queries = request.query_params
#   dic['ffqbid'] = QuestionBank.objects.filter(level = queries['level'][0], admin_programming_language = queries['language'][0])[0].qbid
#   serializer = QuestionBankEvaluationSerializer(data=dic)
#   print("evaluation id id",evaluation_id)
#   print("question bank evaluation data",dic)
#   if serializer.is_valid():
#    serializer.save()
#    questionbankevaluation_id = QuestionBankEvaluation.objects.order_by('-evqbid')[0].evqbid
#    return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
#   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  if request.method == 'DELETE':
#   id = pk
#   stu = QuestionBankEvaluation.objects.get(evqbid=id)
#   stu.delete()
#   return Response({'msg':'Data Deleted'})

@api_view(['GET', 'POST', 'DELETE'])
def score(request, pk=None):
 print("quesry params",request.query_params)
 if request.method == 'GET': 
  id = pk
  if id is not None:
   stu = Score.objects.get(sid=id)
   serializer = ScoreSerializer(stu)
   return Response(serializer.data)

  stu = Score.objects.all()
  serializer = ScoreSerializer(stu, many=True)
  return Response(serializer.data)

 if request.method == 'POST':
  
  print("hello post ")
  print("request data",request.data)
  dic = request.data
  # print("questionbankevaluation_id id", questionbankevaluation_id)
  dic['fevid'] = evaluation_id
#   questionbankevaluation_id = 6 
  language = Expertise.objects.get(fuid=latest_id).programming_language
  temp_questionbank_id = QuestionBank.objects.get(admin_programming_language = language).qbid
  queries = request.query_params
  temp_questionbanklevel_id = QuestionBankLevel.objects.get(fqbid = temp_questionbank_id, qlevel =queries['level'][0] )
#   temp_questionbank_id = QuestionBankEvaluation.objects.get(evqbid =questionbankevaluation_id).ffqbid
#   queries = request.query_params
  temp_code_id = Code.objects.filter(fqblid = temp_questionbanklevel_id)[int(queries['code_no'][0])].cid
  temp_question_id = Question.objects.filter(fcid = temp_code_id)[int(queries['question_no'][0])].qid
  dic['fqid'] = temp_question_id
  if dic['selected_answer'] == Question.objects.get(qid = temp_question_id).correct_option:
    dic['marks'] =  Question.objects.get(qid = temp_question_id).marks
  serializer = ScoreSerializer(data=dic)
  print("questionbankevaluation_id id",questionbankevaluation_id)
  print("question bank evaluation data",dic)
  if serializer.is_valid():
   serializer.save()
   return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 if request.method == 'DELETE':
  id = pk
  stu = Score.objects.get(sid=id)
  stu.delete()
  return Response({'msg':'Data Deleted'})  

def download(request):
    # global response_id
    # print("============", response_id)
    question_ids = []
    correct_answers = []
    selected_answers = []
    marks = []
    decisions = []
    code_ids = []
    dic = collections.defaultdict(list)
    user_id = 1
    program_language = Expertise.objects.get(fuid = user_id).programming_language
    levels = ["1", "2"]
    question_bank_id = QuestionBank.objects.get(admin_programming_language = program_language).qbid
    question_bank_level_ids = []
    print("user id", user_id, "programming language",program_language,"question_bank_id",question_bank_id, "levels", levels,  "code_ids", code_ids, "question_ids", question_ids,"correct_answers",correct_answers,"selected_answers",selected_answers,"marks",marks,"decisions",decisions)
    # print(QuestionBankLevel.objects.filter(fqbid = question_bank_id, qlevel = "1"))
    for index, level in enumerate(levels):
        question_bank_level_ids.append(QuestionBankLevel.objects.filter(fqbid = question_bank_id, qlevel = level)[0].qblid)
        
    # code_ids = []
    
    for id in question_bank_level_ids:
        code_ids.append(Code.objects.filter(fqblid = id)[0].cid)
        code_ids.append(Code.objects.filter(fqblid = id)[1].cid)
        
    # question_ids = []
    # correct_answers = []
    # selected_answers = []
    # marks = []
    # decisions = []
    for id in code_ids:
        question_ids.append(Question.objects.filter(fcid = id)[0].qid)
        question_ids.append(Question.objects.filter(fcid = id)[1].qid)
        question_ids.append(Question.objects.filter(fcid = id)[2].qid)
        # question_ids.append(Question.objects.filter(fcid = id)[3].qid)
        # question_ids.append(Question.objects.filter(fcid = id)[4].qid)
    
    evaluation_id = Evaluation.objects.get(ffuid = user_id, ffqbid = question_bank_id).evid
    for id in question_ids:
        correct_answers.append(Question.objects.get(qid = id).correct_option)
        selected_answers.append(Score.objects.get(fevid = evaluation_id, fqid = id).selected_answer)
        marks.append(Score.objects.get(fevid = evaluation_id, fqid = id).marks)
        decisions.append(Score.objects.get(fevid = evaluation_id, fqid = id).decision)
        
    print("user id", user_id, "programming language",program_language, "levels", levels,  "code_ids", code_ids, "question_ids", question_ids,"correct_answers",correct_answers,"selected_answers",selected_answers,"marks",marks,"decisions",decisions)
        
    # code1 = Code.objects.filter(fqblid = question_bank_level_id)[0].cid
    # print("question_bank_level_id", question_bank_level_id1, "code", code1)
    # question1 = Question.objects.filter(fcid = code1)[0].qid
    # question1 = Question.objects.get(qid = question1).correct_option
    
    n = len(question_ids)
    # responses = Apply.objects.filter(internship=response_id)
    dic['User'] = [user_id]*n
    dic['Programming language'] = [program_language]*n
    dic['Level'] = ([levels[0]]*int(n/2)) + ([levels[1]]*int(n/2))
    dic['Code']  = ([code_ids[0]]*int(n/4)) +  ([code_ids[1]]*int(n/4)) +  ([code_ids[2]]*int(n/4)) +  ([code_ids[3]]*int(n/4))
    dic['Question'] = question_ids
    dic['Selected answer'] = selected_answers
    dic['Correct answer'] = correct_answers
    dic['Decision'] = decisions
    dic['Marks'] = marks
    # print(([levels[0]]*int(n/2)) + (([levels[1]]*int(n/2))))
    print(dic)
    # for i in range(len(responses)):
    #     dic['user'].append(responses[i].user.username)
    #     dic['user_name'].append(responses[i].user_name)
    #     dic['user_email'].append(responses[i].user_email)
    #     dic['phone_number'].append(responses[i].phone_number)
    #     dic['sem'].append(responses[i].sem)
    #     dic['cpi'].append(responses[i].cpi)
    #     dic['precentage_10'].append(responses[i].precentage_10)
    #     dic['precentage_12'].append(responses[i].precentage_12)
    # print(dic)
    df = pd.DataFrame(dic)

    response = HttpResponse(content_type='text/csv')
    # your filename
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    writer.writerow(['S.No.', 'User', 'Programming language', 'Level', 'Code', 'Question', 'Selected answer', 'Correct answer', 'Decision', 'Marks'])
    for ind in range(df.shape[0]):
        writer.writerow([ind, df['User'][ind], df['Programming language'][ind], df['Level'][ind],df['Code'][ind],df['Question'][ind],df['Selected answer'][ind],df['Correct answer'][ind],df['Decision'][ind], df['Marks'][ind]])

    return response
  



@api_view(['GET', 'POST', 'DELETE'])
def getcode(request):
  if request.method == 'GET': 
    # id = pk
    print("quesry params",request.query_params)
    latest_id = 1
    programming_language = Expertise.objects.get(fuid = latest_id).programming_language
    question_bank_id = QuestionBank.objects.get(admin_programming_language = programming_language).qbid
    queries = request.query_params
    level = QuestionBankLevel.objects.get(fqbid = question_bank_id, qlevel = queries['level'][0]).qblid
    id = Code.objects.filter(fqblid = level)[int(queries['code'][0])].cid
    
    stu = Code.objects.get(cid=id)
    serializer = CodeSerializer(stu)
    return Response(serializer.data)

    # stu = Code.objects.all()
    # serializer = CodeSerializer(stu, many=True)
    # return Response(serializer.data)
