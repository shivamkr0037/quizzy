import json
from pprint import pprint
import random
from random import randint
import os
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

WUP_Threshold = 0.8
greeting = ['Hi there, how are you doing today!\nI am quizzy, let\'s play a quiz today!', 'Hi I\'m quizzy, your quizmaster!', 'Quizzy here, let\'s start']
wrong_category = ['Hmm! We currently do not have any quizzes on that.', 'Sorry we don\'t have any questions regarding that.', 'Hmm, pick another one!']
next_question = ['Here comes the next question!', 'Get ready for the next one!', 'Here comes another']
correct_answer = ['Correct answer, well done!', 'You\'re smart!', 'You\'re a genius']
wrong_answer = ['Sorry, wrong answer. Nevermind', 'Wrong! Buck up', 'Nah! Come on!']


def extractNounsAndAdjectives(words):
        NJ = []
        pos = nltk.pos_tag(words)
        for word, tag in pos:
                if tag[0] in ('N', 'J'):
                        NJ.append(word)
        return NJ

# Wu-Palmer similarity
def WUPSimilarity(w1, w2):
        w1 = wn.synsets(w1)
        w2 = wn.synsets(w2)
        max_WUP = 0
        # Checking for the first 3 synonyms in order to avoid noise
        for i in range(0, min(3, len(w1))):
                for j in range(0, min(3, len(w2))):
                        sim = w1[i].wup_similarity(w2[j])
                        if sim is not None:
                                max_WUP = max(max_WUP, sim)
        return max_WUP

# Compute possible categories based on user response
def computeCategories(categories, user_response_NJ):
        probable_categories = {}
        for w1 in categories:
                for w2 in user_response_NJ:
                        for w in w1.split('-'):
                                sim = WUPSimilarity(w, w2)
                                # print(w, w2, sim)
                                if sim >= 1:
                                        probable_categories.clear()
                                        probable_categories[w1] = w2
                                        return probable_categories
                                elif sim >= WUP_Threshold:
                                        probable_categories[w1] = w2
        return probable_categories

# Compute the possible choices present in user_response
def computeChoices(user_response, choices):
        # # Use this if you want to confirm for ambiguous user answers
        # uniqueInChoices = []
        # for i in range(0, len(choices)):
        #         unique_choice = nltk.word_tokenize(choices[i].lower())
        #         unique_choice = [i for i in unique_choice if i not in punctuations and i not in stop_words]
        #         unique_choice = set(unique_choice)
        #         for j in range(0, len(choices)):
        #                 if i != j:
        #                         unique_choice = unique_choice - set(nltk.word_tokenize(choices[j].lower()))
        #         uniqueInChoices.append(list(unique_choice))
        punctuations = list(string.punctuation)
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        ct = 'a'
        probable_choices = []
        user_response = nltk.word_tokenize(user_response.lower())
        user_response = [lemmatizer.lemmatize(word, pos='v') for word in user_response]
        user_response = [i for i in user_response if i not in punctuations and i not in stop_words]
        user_response = set(user_response)
        for choice in choices:
                # print(choice)
                choice = nltk.word_tokenize(choice.lower())
                choice = [lemmatizer.lemmatize(word, pos='v') for word in choice]
                choice = [i for i in choice if i not in punctuations and i not in stop_words]
                choice = set(choice)
                if len(user_response.intersection(choice)) > 0:
                        probable_choices.append(ct)
                ct = chr(ord(ct) + 1)
        return probable_choices

def displayBotResponse(score, responses, isCorrect, answer_choice=''):
        print(random.choice(responses))
        if isCorrect:
                score += 1
        else:
                score -= 0.25
                print("The correct answer is {}".format(answer_choice.upper()))
        print ('Score = {}'.format(score))
        return score

def loadAllCategories():
        categories = set()
        for root, dirs, files in os.walk("./OpenTriviaQA_JSON"):
                for name in files:
                        categories.add(name[: -5])
        return categories

def chooseCategory():
        categories = loadAllCategories()
        flag = False
        category = ""
        print('What would you liked to be quizzed on?')
        while flag == False:
                user_response = input()
                print()
                if len(user_response) > 0 and user_response[0] == '@':
                        if user_response[1: ] == 'list_quizzes':
                                for c in categories:
                                        print(c)
                                print()
                                continue
                words = nltk.word_tokenize(user_response)
                user_response_NJ = extractNounsAndAdjectives(words)
                probable_categories = computeCategories(categories, user_response_NJ)

                if len(probable_categories) == 0:
                        print("{} Type @list_quizzes to list categories".format(random.choice(wrong_category)))
                elif len(probable_categories) == 1:
                        category = list(probable_categories.keys())[0]
                        print('Alright! One quiz on {}({}) coming right up!'.format(category, probable_categories[category]))
                        print('We score +1 for a correct answer and -0.25 for a wrong one. Enjoy!')
                        print('Type @stop_quiz anytime to quit the quiz')
                        print('To change topics type @change_quiz\n')
                        flag = True
                else:
                        print("OK, judging by your response I have multiple categories.")
                        keys = probable_categories.keys()
                        for key in keys:
                                print("{}({})".format(key, probable_categories[key]))
                        print()
                        print("Which one would you like?")
                        print("To list all my categories, you can type @list_quizzes\n")
        return category

def loadCategoryData(category):
        # Open quiz bank for particular category
        dir_path = os.path.join('OpenTriviaQA_JSON')
        with open(os.path.join(dir_path, category + '.json'), encoding='utf8') as data_file:
                data = json.load(data_file)
        return data

def displayScores(category_scores, total_score):
        keys = category_scores.keys()
        print('Here are your categorical scores')
        for key in keys:
                print("{}: {}".format(key, category_scores[key]))
        print('Your total score is {}'.format(total_score))


def quiz():
        print(random.choice(greeting))
        category = chooseCategory()
        data = loadCategoryData(category)

        # Start quiz!
        genarated = []
        stop = False
        score = 0
        category_scores = {}
        total_score = 0

        print('\nHere we go!')
        while stop == False:
                rand = randint(-1, len(data) - 1)
                while rand in genarated:
                        rand = randint(-1, len(data) - 1)
                genarated.append(rand)

                print(data[rand]['question'])
                ct = 'A'
                answer = data[rand]['answer']
                answer_choice = ''
                for c in data[rand]['choices']:
                        print('{}. {}'.format(ct, c))
                        if c == answer:
                                answer_choice = ct
                        ct = chr(ord(ct) + 1)

                unambiguous_response = False
                while unambiguous_response == False:
                        user_response = input()
                        print()
                        if len(user_response) > 0 and user_response[0] == '@':
                                if user_response[1: ] == 'stop_quiz':
                                        unambiguous_response = True
                                        stop = True
                                        category_scores[category] = score
                                        total_score += score
                                        displayScores(category_scores, total_score)
                                        print('Thanks for playing. Until next time!')
                                        continue
                                elif user_response[1: ] == 'change_quiz':
                                        unambiguous_response = True
                                        category_scores[category] = score
                                        total_score += score
                                        category = chooseCategory()
                                        data = loadCategoryData(category)
                                        displayScores(category_scores, total_score)
                                        continue
                        response_words = nltk.word_tokenize(user_response.lower())
                        answer_choice = answer_choice.lower()
                        probable_choices = computeChoices(user_response, data[rand]['choices'])
                        # print(probable_choices)

                        if answer_choice in response_words:
                                score = displayBotResponse(score, correct_answer, True)
                                unambiguous_response = True
                        elif len(probable_choices) >= 1:
                                if len(probable_choices) == 1:
                                        unambiguous_response = True
                                        if probable_choices[0].lower() == answer_choice:
                                                score = displayBotResponse(score, correct_answer, True)
                                        else:
                                                score = displayBotResponse(score, wrong_answer, False, answer_choice)
                                else:
                                        print('Hmm. You seem to have picked more than one option. Pick one')
                                        print(probable_choices)
                        else:
                                score = displayBotResponse(score, wrong_answer, False, answer_choice)
                                unambiguous_response = True
                if stop == False:
                        print(random.choice(next_question))
                print()


if __name__ == '__main__':
        quiz()
