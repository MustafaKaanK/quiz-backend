from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.getQuizzes),
    path('quizzes/<str:pk>/', views.getQuiz),
    path('quizzes/<str:pk>/questions/', views.getQuestions),
    path('quizzes/<str:pk1>/questions/<str:pk2>/', views.getQuestion),
    path('quizzes/<str:pk>/submission/', views.submitAnswers),
]