from rest_framework.serializers import ModelSerializer
from .models import Option, Question, Result, Quiz, Submission


# Serializers for Option model
class OptionSimplifiedSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = ('description', 'number_order')

class OptionDetailedSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = ('description', 'number_order', 'updated_date', 'created_date')


# Serializers for Question model
class QuestionSimplifiedSerializer(ModelSerializer):
    options = OptionSimplifiedSerializer(many=True)
    class Meta:
        model = Question
        fields = ('description', 'number_order', 'options')

class QuestionDetailedSerializer(ModelSerializer):
    options = OptionDetailedSerializer(many=True)
    class Meta:
        model = Question
        fields = ('description', 'number_order', 'options', 'updated_date', 'created_date')


# Serializers for Quiz model
class QuizSimplifiedSerializer(ModelSerializer):
    questions = QuestionSimplifiedSerializer(many=True)
    class Meta:
        model = Quiz
        fields = ('id', 'description', 'number_of_questions', 'questions')

class QuizDetailedSerializer(ModelSerializer):
    questions = QuestionDetailedSerializer(many=True)
    class Meta:
        model = Quiz
        fields = ('id', 'description', 'number_of_questions', 'questions', 'updated_date', 'created_date')


# Serializer for Result model
class ResultDetailedSerializer(ModelSerializer):
    class Meta:
        model = Result
        fields = ('description', 'updated_date', 'created_date')