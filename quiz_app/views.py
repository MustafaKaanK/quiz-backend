from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import OptionSimplifiedSerializer, OptionDetailedSerializer, QuestionSimplifiedSerializer, QuestionDetailedSerializer, QuizSimplifiedSerializer, QuizDetailedSerializer, ResultDetailedSerializer
from .models import  Option, Question, Quiz, Result, Submission
import numpy as np

# Returns all quizzes with simplified information.
# .../quizzes/
@api_view(['GET'])
def getQuizzes(request):
    quizzes = Quiz.objects.all()
    serializer = QuizSimplifiedSerializer(quizzes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Returns the selected quiz with detailed information.
# .../quizzes/<str:pk>/
@api_view(['GET'])
def getQuiz(request, pk):
    try:
        quiz = Quiz.objects.get(id=pk)
        serializer = QuizDetailedSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Quiz.DoesNotExist:
        return Response({"error": f"Quiz with id {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)

# Returns all questions for selected quiz with simplified information.
# .../quizzes/<str:pk>/questions/
@api_view(['GET'])
def getQuestions(request, pk):
    try:
        quiz = Quiz.objects.get(id=pk)
        questions = quiz.questions.all()
        serializer = QuestionSimplifiedSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Quiz.DoesNotExist:
        return Response({"error": f"Quiz with id {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)

# Returns the selected question for selected quiz with detailed information.
# .../quizzes/<str:pk>/questions/<str:pk>/
@api_view(['GET'])
def getQuestion(request, pk1, pk2):
    try:
        quiz = Quiz.objects.get(id=pk1)
        question = quiz.questions.get(number_order=pk2)
        serializer = QuestionDetailedSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Quiz.DoesNotExist:
        return Response({"error": f"Quiz with id {pk1} does not exist!"}, status=status.HTTP_404_NOT_FOUND)
    except Question.DoesNotExist:
        return Response({"error": f"Question with number {pk2} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

# Submits answers for selected quiz then, calculates and returns the result.
# .../quizzes/<str:pk>/submission/
@api_view(['POST'])
def submitAnswers(request, pk):
    try:
        selected_options_nums = request.data['selected_options']
        selected_options_nums_size = len(selected_options_nums)
        selected_quiz = Quiz.objects.get(id=pk)
        selected_quiz_results_size = selected_quiz.results.count()
        if selected_options_nums_size != selected_quiz.number_of_questions:
            raise ValueError("Size of selected_options does not match with the number of questions in selected quiz!")
        result_factor_list = np.zeros(selected_quiz_results_size)
        for i in range(1, selected_options_nums_size + 1):
            try:
                selected_question = selected_quiz.questions.get(number_order=i)
                selected_option = selected_question.options.get(number_order=selected_options_nums[i - 1])
                if len(selected_option.result_factor_list) != selected_quiz_results_size:
                    raise ValueError("Size of result factor list for selected option does not match with the selected quiz results size!")
                result_factor_list += selected_option.result_factor_list
            except Question.DoesNotExist:
                return Response({"error": f"Question with number {i} does not exist!"}, status=status.HTTP_404_NOT_FOUND)
            except Option.DoesNotExist:
                return Response({"error": f"Quiz with number {selected_options_nums[i - 1]} does not exist!"}, status=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        result_index = np.argmax(result_factor_list)
        result = selected_quiz.results.all().order_by('id')[int(result_index)]
        result.serializer = ResultDetailedSerializer(result)
        Submission.objects.create(
            quiz_id = int(pk),
            selected_options_ids = request.data['selected_options']
        )
        # TODO(MBM): Add error handling for if submission creating fails.
        return Response(result.serializer.data, status=status.HTTP_200_OK)
    except KeyError:
        return Response({"error": "'selected_options' not found in request data!"}, status=status.HTTP_400_BAD_REQUEST)
    except Quiz.DoesNotExist:
        return Response({"error": f"Quiz with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)