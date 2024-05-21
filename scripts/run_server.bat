@echo off
echo Activating the virtual environment...

call djenv\Scripts\activate.bat

echo Running Django migrations...

python online_quiz\manage.py makemigrations
python online_quiz\manage.py migrate

echo Starting the Django development server...

python online_quiz\manage.py runserver