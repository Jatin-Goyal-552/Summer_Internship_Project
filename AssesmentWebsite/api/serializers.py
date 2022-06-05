from attr import field
from rest_framework import serializers
from .models import *

class DemographicSerializer(serializers.ModelSerializer):
  class Meta:
    model = Demographic
    fields = '__all__'
    # fields = ['name','email','dob','age','gender','state','country','profession']
    

  
class ExpertiseSerializer(serializers.ModelSerializer):
  # print(Demographic.objects.order_by('-uid'))
  # fuid = serializers.PrimaryKeyRelatedField(queryset=Demographic.objects.filter(uid = Demographic.objects.order_by('-uid')[0].uid),
  #                                                 many=False)
  class Meta:
    model = Expertise
    fields = '__all__'

class QuestionBankSerializer(serializers.ModelSerializer):
  # print(Demographic.objects.order_by('-uid'))
  # fuid = serializers.PrimaryKeyRelatedField(queryset=Demographic.objects.filter(uid = Demographic.objects.order_by('-uid')[0].uid),
  #                                                 many=False)
  class Meta:
    model = QuestionBank
    fields = '__all__'
  
class CodeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Code
    fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Question
    fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Evaluation
    fields = '__all__'

class QuestionBankEvaluationSerializer(serializers.ModelSerializer):
  class Meta:
    model = QuestionBankEvaluation
    fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Score
    fields = "__all__"