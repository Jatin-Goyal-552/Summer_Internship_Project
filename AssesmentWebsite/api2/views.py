# from matplotlib import interactive
from .models import *
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

# request.session['user_id'] = None 
user_id = None
question_bank_id = None
question_bank_level_id = None
code_id = None
evaluation_id = None
# questionbankevaluation_id = None
user_code_id = None



@api_view(['GET', 'POST', 'DELETE'])
def demographic(request, pk=None):
    global user_id
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
            print("now i am here")
            serializer.save()
            # request.session['user_id'] = Demographic.objects.order_by('-uid')[0].uid 
            user_id = Demographic.objects.order_by('-uid')[0].uid 
            
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id = pk
        stu = Demographic.objects.get(uid=id)
        stu.delete()
        return Response({'msg':'Data Deleted'})


@api_view(['GET', 'POST','PUT', 'DELETE'])
def expertise(request, pk=None):
    if request.method == 'GET': 
        id = pk
        if id is not None:
            exp = Expertise.objects.get(eid=id)
            serializer = ExpertiseSerializer(exp)
            return Response(serializer.data)
        exp = Expertise.objects.all()
        serializer = ExpertiseSerializer(exp, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        dic = request.data
        # dic['fuid'] = request.session['user_id']
        dic['fuid'] = user_id
        
        serializer = ExpertiseSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        id = pk
        exp = Expertise.objects.get(eid=id)
        serializer = ExpertiseSerializer(exp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Updated'})
        return Response(serializer.errors)


    if request.method == 'DELETE':
        id = pk
        exp = Expertise.objects.get(eid=id)
        exp.delete()
        return Response({'msg':'Data Deleted'})


@api_view(['POST'])
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
            quebank = QuestionBank.objects.get(qbid=id)
            serializer = QuestionBankSerializer(quebank)
            return Response(serializer.data)

        quebank = QuestionBank.objects.all()
        serializer = QuestionBankSerializer(quebank, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        dic = request.data
        serializer = QuestionBankSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            # request.session['question_bank_id'] = QuestionBank.objects.order_by('-qbid')[0].qbid
            question_bank_id = QuestionBank.objects.order_by('-qbid')[0].qbid
            
            # print("question_bank_id", request.session['question_bank_id'])
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id = pk
        quebank = QuestionBank.objects.get(qbid=id)
        quebank.delete()
        return Response({'msg':'Data Deleted'})

@api_view(['GET', 'POST', 'DELETE'])
def questionbanklevel(request, pk=None):
    global question_bank_level_id
    if request.method == 'GET': 
        id = pk
        if id is not None:
            quebanklevel = QuestionBankLevel.objects.get(qblid=id)
            serializer = QuestionBankLevelSerializer(quebanklevel)
            return Response(serializer.data)

        quebanklevel = QuestionBankLevel.objects.all()
        serializer = QuestionBankLevelSerializer(quebanklevel, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        dic = request.data
        # dic['fqbid'] = request.session['question_bank_id']
        dic['fqbid'] = question_bank_id
        
        serializer = QuestionBankLevelSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            # request.session['question_bank_level_id'] = QuestionBankLevel.objects.order_by('-qblid')[0].qblid
            question_bank_level_id = QuestionBankLevel.objects.order_by('-qblid')[0].qblid
            
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id = pk
        quebanklevel = QuestionBankLevel.objects.get(qblid=id)
        quebanklevel.delete()
        return Response({'msg':'Data Deleted'})


@api_view(['GET', 'POST', 'DELETE'])
def code(request, pk=None):
    global code_id
    if request.method == 'GET': 
        id = pk
        if id is not None:
            cod = Code.objects.get(cid=id)
            serializer = CodeSerializer(cod)
            return Response(serializer.data)

        cod = Code.objects.all()
        serializer = CodeSerializer(cod, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        dic = request.data
        # dic['fqblid'] = request.session['question_bank_level_id']
        dic['fqblid'] = question_bank_level_id
        
        serializer = CodeSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            # request.session['code_id'] = Code.objects.order_by('-cid')[0].cid
            code_id = Code.objects.order_by('-cid')[0].cid
            
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id = pk
        cod = code.objects.get(cid=id)
        cod.delete()
        return Response({'msg':'Data Deleted'})


@api_view(['GET', 'POST', 'DELETE'])
def question(request, pk=None):
    if request.method == 'GET': 
        id = pk
        if id is not None:
            que = Question.objects.get(qid=id)
            serializer = QuestionSerializer(que)
            return Response(serializer.data)

        que = Question.objects.all()
        serializer = QuestionSerializer(que, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        dic = request.data
        # dic['fcid'] = request.session['code_id']
        dic['fcid'] = code_id
         
        serializer = QuestionSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id = pk
        que = Question.objects.get(qid=id)
        que.delete()
        return Response({'msg':'Data Deleted'})

@api_view(['GET', 'POST', 'DELETE'])
def evaluation(request, pk=None):
    global evaluation_id
    if request.method == 'GET': 
        id = pk
        if id is not None:
            eval = Evaluation.objects.get(evid=id)
            serializer = EvaluationSerializer(eval)
            return Response(serializer.data)

        eval = Evaluation.objects.all()
        serializer = EvaluationSerializer(eval, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        dic = request.data
        # dic['ffuid'] = request.session['user_id']
        dic['ffuid'] = user_id
        
        # questionbanklang = Expertise.objects.get(fuid=request.session['user_id']).programming_language
        questionbanklang = Expertise.objects.get(fuid=user_id).programming_language
        
        dic['ffqbid'] = QuestionBank.objects.get(admin_programming_language = questionbanklang).qbid
        serializer = EvaluationSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            # request.session['evaluation_id'] = Evaluation.objects.order_by('-evid')[0].evid
            evaluation_id = Evaluation.objects.order_by('-evid')[0].evid
            
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id = pk
        eval = Evaluation.objects.get(evid=id)
        eval.delete()
        return Response({'msg':'Data Deleted'})

@api_view(['GET'])
def getcode(request):
    global user_code_id
    if request.method == 'GET': 
        # user_id = 1\
        programming_language = Expertise.objects.get(fuid = user_id).programming_language
        question_bank_id = QuestionBank.objects.get(admin_programming_language = programming_language).qbid
        queries = request.query_params
        level = QuestionBankLevel.objects.get(fqbid = question_bank_id, qlevel = queries['level'][0]).qblid
        # request.session['question_code_id'] = Code.objects.filter(fqblid = level)[int(queries['code'][0])].cid
        user_code_id = Code.objects.filter(fqblid = level)[int(queries['code'][0])].cid
        
        # stu = Code.objects.get(cid=request.session['question_code_id'])
        stu = Code.objects.get(cid=user_code_id)
        serializer = CodeSerializer(stu)
        return Response(serializer.data)

  
@api_view(['GET'])
def getquestion(request):
    if request.method == 'GET': 
        # request.session['question_code_id'] = 1
        # question_code_id = 1
        print("quesry params",request.query_params)
        # user_id = 1
        queries = request.query_params
        id = Question.objects.filter(fcid = user_code_id)[int(queries['question'][0])].qid
        stu = Question.objects.get(qid=id)
        serializer = QuestionSerializer(stu)
        return Response(serializer.data)

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
        # dic['fevid'] = None
        #   questionbankevaluation_id = 6 
        # language = Expertise.objects.get(fuid=request.session['user_id']).programming_language
        language = Expertise.objects.get(fuid=user_id).programming_language
        temp_questionbank_id = QuestionBank.objects.get(admin_programming_language = language).qbid
        queries = request.query_params
        temp_questionbanklevel_id = QuestionBankLevel.objects.get(fqbid = temp_questionbank_id, qlevel = queries['level'][0] )
        #   temp_questionbank_id = QuestionBankEvaluation.objects.get(evqbid =questionbankevaluation_id).ffqbid
        #   queries = request.query_params
        temp_code_id = Code.objects.filter(fqblid = temp_questionbanklevel_id)[int(queries['code_no'][0])].cid
        temp_question_id = Question.objects.filter(fcid = temp_code_id)[int(queries['question_no'][0])].qid
        dic['fqid'] = temp_question_id
        if dic['selected_answer'] == Question.objects.get(qid = temp_question_id).correct_option:
            dic['marks'] =  Question.objects.get(qid = temp_question_id).marks
            dic['decision'] = "1"
        else:
            dic['marks'] =  0
            dic['decision'] = "2"
        serializer = ScoreSerializer(data=dic)
        # print("questionbankevaluation_id id",questionbankevaluation_id)
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
    
@api_view(['GET', 'POST', 'DELETE'])
def time(request, pk=None):
    print("quesry params",request.query_params)
    if request.method == 'GET': 
        id = pk
        if id is not None:
            stu = Time.objects.get(sid=id)
            serializer = TimeSerializer(stu)
            return Response(serializer.data)

        stu = Time.objects.all()
        serializer = TimeSerializer(stu, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
    
        print("hello post ")
        print("request data",request.data)
        dic = request.data
        # print("questionbankevaluation_id id", questionbankevaluation_id)
        # dic['fevid'] = request.session['evaluation_id']
        # dic['ffevid'] = None
        #   questionbankevaluation_id = 6 
        # language = Expertise.objects.get(fuid=request.session['user_id']).programming_language
        dic['fevid'] = evaluation_id
        
        language = Expertise.objects.get(fuid=user_id).programming_language
        temp_questionbank_id = QuestionBank.objects.get(admin_programming_language = language).qbid
        queries = request.query_params
        temp_questionbanklevel_id = QuestionBankLevel.objects.get(fqbid = temp_questionbank_id, qlevel = queries['level'][0] )
        #   temp_questionbank_id = QuestionBankEvaluation.objects.get(evqbid =questionbankevaluation_id).ffqbid
        #   queries = request.query_params
        temp_code_id = Code.objects.filter(fqblid = temp_questionbanklevel_id)[int(queries['code_no'][0])].cid
        # temp_question_id = Question.objects.filter(fcid = temp_code_id)[int(queries['question_no'][0])].qid
        dic['fcfid'] = temp_code_id
        # if dic['selected_answer'] == Question.objects.get(qid = temp_question_id).correct_option:
        #     dic['marks'] =  Question.objects.get(qid = temp_question_id).marks
        #     dic['decision'] = 1
        # else:
        #     dic['marks'] =  0
        #     dic['decision'] = 0
        serializer = TimeSerializer(data=dic)
        # print("questionbankevaluation_id id",questionbankevaluation_id)
        print("question bank evaluation data",dic)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id = pk
        stu = Time.objects.get(sid=id)
        stu.delete()
        return Response({'msg':'Data Deleted'})  

def getlanguage(id):
    if id == "1":
        return "Python"
    if id == "2":
        return "C++"
    if id == "3":
        return "Java"

def getdecision(id):
    if id == '1':
        return "Y"
    else:
        return "N"

def download(request):
    # global response_id
    # print("============", response_id)
    user_id = 12
    question_ids = []
    correct_answers = []
    selected_answers = []
    marks = []
    decisions = []
    code_ids = []
    dic = collections.defaultdict(list)
    program_language = Expertise.objects.get(fuid = user_id).programming_language
    levels = ["1", "2", "3"]
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
        # code_ids.append(Code.objects.filter(fqblid = id)[].cid)
        
    # question_ids = []
    # correct_answers = []
    # selected_answers = []
    # marks = []
    # decisions = []
    for id in code_ids:
        question_ids.append(Question.objects.filter(fcid = id)[0].qid)
        question_ids.append(Question.objects.filter(fcid = id)[1].qid)
        question_ids.append(Question.objects.filter(fcid = id)[2].qid)
        question_ids.append(Question.objects.filter(fcid = id)[3].qid)
        question_ids.append(Question.objects.filter(fcid = id)[4].qid)
    
    evaluation_id = Evaluation.objects.get(ffuid = user_id, ffqbid = question_bank_id).evid
    for id in question_ids:
        correct_answers.append(Question.objects.get(qid = id).correct_option)
        selected_answers.append(Score.objects.get(fevid = evaluation_id, fqid = id).selected_answer)
        marks.append(Score.objects.get(fevid = evaluation_id, fqid = id).marks)
        decisions.append(getdecision(Score.objects.get(fevid = evaluation_id, fqid = id).decision))
        
    print("user id", user_id, "programming language",program_language, "levels", levels,  "code_ids", code_ids, "question_ids", question_ids,"correct_answers",correct_answers,"selected_answers",selected_answers,"marks",marks,"decisions",decisions)
        
    # code1 = Code.objects.filter(fqblid = question_bank_level_id)[0].cid
    # print("question_bank_level_id", question_bank_level_id1, "code", code1)
    # question1 = Question.objects.filter(fcid = code1)[0].qid
    # question1 = Question.objects.get(qid = question1).correct_option
    iterative_question_id = []
    for i in range(6):
            iterative_question_id.append("Q1")
            iterative_question_id.append("Q2")
            iterative_question_id.append("Q3")
            iterative_question_id.append("Q4")
            iterative_question_id.append("Q5")
    print("-------------------------------------------")
    print(iterative_question_id, len(iterative_question_id))
    n = len(question_ids)
    print("n",n)
    # responses = Apply.objects.filter(internship=response_id)
    dic['User'] = [Demographic.objects.get(uid = user_id).name]*n
    dic['Programming language'] = [getlanguage(program_language)]*n
    dic['Level'] = (["E"]*int(n/3)) + (["M"]*int(n/3)) +  (["H"]*int(n/3))
    dic['Code']  = (["c1"]*int(n/6)) +  (["c2"]*int(n/6)) +  (["c1"]*int(n/6)) +  (["c2"]*int(n/6)) + (["c1"]*int(n/6)) + (["c2"]*int(n/6))
    dic['Question'] = iterative_question_id
    dic['Selected answer'] = selected_answers
    dic['Correct answer'] = correct_answers
    dic['Decision'] = decisions
    dic['Marks'] = marks
    for key in dic:
        print(key, len(dic[key]))
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
    print(df.head())
    response = HttpResponse(content_type='text/csv')
    # your filename
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    writer.writerow(['S.No.', 'User', 'Programming language', 'Level', 'Code', 'Question', 'Selected answer', 'Correct answer', 'Decision', 'Marks'])
    for ind in range(df.shape[0]):
        writer.writerow([ind, df['User'][ind], df['Programming language'][ind], df['Level'][ind],df['Code'][ind],df['Question'][ind],df['Selected answer'][ind],df['Correct answer'][ind],df['Decision'][ind], df['Marks'][ind]])

    return response
  





