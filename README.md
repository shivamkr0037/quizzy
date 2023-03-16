# Quizzy

A simple quizbot written in python that extracts topic of interest from the user and quizzes them on it.
- Gets data from user responses in natural language, to find a specific topic of interest
- Engages the user in an interactive quiz
- Scores +1 for correct answer and -0.25 for wrong answer
- Ability to change the topic of interest for the quiz
- Detects ambiguous responses

## Workflow
<div align="center">
  <img src="screenshots/workflow.jpg" height=350 width=400>
</div>

1. The user starts interacting with Quizzy.
2. Quizzy tries to find the area of interest, on which user wants to take the quiz.
3. Once the quiz topic is decided, user is quizzed on it, this is phase 2.
4. User takes the quiz and is shown questions fetched from the question bank.
5. User answers the questions in natural language, from which the answer is extracted and is checked against the correct option in the question bank.
6. Once the quiz is complete and the user is satisfied, the user will be redirected to the initial phase i.e, phase 1.


## Setup
This project is written in python 3.7

Install requirements:
```bash
pip install -r requirements.txt
```

Download the nltk resources. Inside a python shell:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

Start quizzy:
```bash
python quiz.py
```

### Commands
- `@list_quizzes` - Displays the quiz topics available. Only applicable when selecting a quiz topic
- `@stop_quiz` - Stops the quiz and displays the final score
- `@change_quiz` - Change quiz topic. Applicable when a quiz topic is already active


## Demo
![](/screenshots/2.png?raw=true)
<br></br>

![](/screenshots/3.png?raw=true)
