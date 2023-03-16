# quizbot

A simple quizbot wriiten in python that extracts topic of interest from the user and quizzes them on it.
- Gets data from user responses to find a specific topic of interest
- Engages the user in an interactive quiz
- Scores +1 for correct answer and -0.25 for wrong answer
- Ability to change the topic of interest for the quiz

## Workflow
<div align="center">
  <img src="screenshots/workflow.jpg" height=350 width=400>
</div>

1. The user starts interacting with the chatbot.
2. Our bot tries to find the area of interest, on which user wants to take the quiz. 
3. Once the quiz topic is decided, user is quizzed on it, this is phase 2.
4. User takes the quiz and is shown questions fetched from the question bank.
5. User answers the questions which is checked with the correct option in question bank.
6. Once the quiz is complete and the user is satisfied, the user will be redirected to the initial phase i.e, phase 1.



## Demo
![](/screenshots/2.png?raw=true)
<br></br>

![](/screenshots/3.png?raw=true)
