from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField

gender_choices =(
    ("1", "Female"),
    ("2", "Male"),
    ("3", "NaN")
)

profession_choices =(
    ("1", "Student"),
    ("2", "Industrialist"),
    ("3", "Professor")
)

language_choices =(
    ("1", "Python"),
    ("2", "C++"),
    ("3", "Java")
)

level_choices =(
    ("1", "Beginner"),
    ("2", "Intermediate"),
    ("3", "Expert")
)

duration_choices =(
    ("1", "<1 year"),
    ("2", "1-3 years"),
    ("3", ">3 years")
)

decision_choices =(
    ("1", "Correct"),
    ("2", "Incorrect")
)
# Create your models here.
class Demographic(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(choices=gender_choices, max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    profession = models.CharField(choices=profession_choices, max_length=100)
    def __str__(self):
        return f"{self.uid}"

class Expertise(models.Model):
    eid = models.AutoField(primary_key=True)
    fuid = models.ForeignKey(Demographic,related_name='demographic_id', on_delete=models.CASCADE, null= True)
    programming_language = models.CharField(choices=language_choices, max_length=100)
    level = models.CharField(choices=level_choices, max_length=100)
    duration = models.CharField(choices=duration_choices, max_length=100)
    time = models.IntegerField()
    last_used = models.CharField(max_length=100, null=True, blank=True)
 
class QuestionBank(models.Model):
    qbid = models.AutoField(primary_key=True)
    # aid = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    admin_programming_language = models.CharField(choices=language_choices, max_length=100)
    # level = models.CharField(choices=level_choices, max_length=100)
    
class QuestionBankLevel(models.Model):
    qblid = models.AutoField(primary_key=True)
    fqbid = models.ForeignKey(QuestionBank,on_delete=models.CASCADE, null= True)
    qlevel = models.CharField(choices=level_choices, max_length=100)

class Code(models.Model):
    cid = models.AutoField(primary_key=True)
    fqblid = models.ForeignKey(QuestionBankLevel,on_delete=models.CASCADE, null= True)
    code_image = models.ImageField()
    code_text = models.CharField(max_length=500, null=True)
    code_time = models.IntegerField(null=True)
    # code_read_time = models.IntegerField(null=True)
    question_time = models.IntegerField(null=True)
    # question_read_time = models.IntegerField(null=True)
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    fcid = models.ForeignKey(Code, on_delete=models.CASCADE, null= True)
    question_text = models.CharField(max_length=500, null=True)
    option1 = models.CharField(max_length=500, null=True)
    option2 = models.CharField(max_length=500, null=True)
    option3 = models.CharField(max_length=500, null=True)
    option4 = models.CharField(max_length=500, null=True)
    correct_option = models.CharField(max_length=500, null=True)
    marks = models.FloatField(null=True)
    question_time = models.IntegerField(null=True)

class Evaluation(models.Model):
    evid = models.AutoField(primary_key=True)
    ffuid = models.ForeignKey(Demographic, on_delete=models.CASCADE, null= True)
    ffqbid = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, null= True)
    
# class QuestionBankEvaluation(models.Model):
#     evqbid = models.AutoField(primary_key=True)
#     fevid = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null= True)
#     ffqbid = models.ForeignKey(QuestionBank,on_delete=models.CASCADE, null= True)

class Score(models.Model):
    sid = models.AutoField(primary_key=True)
    fevid = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null= True)
    fqid = models.ForeignKey(Question, on_delete=models.CASCADE, null= True)
    selected_answer = models.CharField(max_length=500, null=True)
    decision = models.CharField(choices=decision_choices, max_length=100, null=True)
    marks = models.FloatField(null=True)
    