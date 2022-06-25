# API Development + Documentation + Testing (Project)

## The Trivia App

This project was finished by me for (and while learning API development on) Udacity so that it can start holding trivia to discover, regularly or once in a while, who's the most knowledgeable of the bunch at the team over there.

## The Story

A bunch of team members at Udacity got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

So as a pro at API development and everything Python (Web/Mobile/Ai), I had to jump on it.

## What I Have/Will Do[ne]

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## The Milestone

Completing this trivia app will give me the ability to structure, plan, implement, and test an API - skills essential for enabling my future applications to communicate with others in the tech industry.

## Dependencies
### Backend
The following dependencies were used in this project:
* Python 3.7: Follow instructions to install the latest version of python for your platform in the python docs
* Virtual Enviornment: We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs
* PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:
* Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.
* SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.
* Flask-CORS, the extension we'll use to handle cross origin requests from our frontend server.

    pip install -r requirements.txt

### Frontend
#### Installing Node and NPM
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from https://nodejs.com/en/download.

The NPM is used to manage software dependencies in this project. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

    npm install

## Database Setup
With Postgres running, restore a database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

    psql trivia < trivia.psql

## Running the server
From within the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run

## Testing
To run the tests, run

    dropdb trivia_test
    createdb trivia_test
    psql trivia_test < trivia.psql
    python test_flaskr.py


## Running Your Frontend in Dev Mode
The frontend app was built using create-react-app. In order to run the app in development mode use npm start. You can change the script in the package.json file.

Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.

    npm start


## Endpoints
### GET '/categories'
* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
* Request Arguments: None
* Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

Example: curl http://localhost:5000/categories
    {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    }

### GET '/questions'
* Fetches a dictionary of questions, paginated in groups of 10.
* Returns JSON object of categories, questions dictionary with answer, category, difficulty, id and question.

Example: curl http://localhost:5000/questions
    {
        "categories": [
            "Science",
            "Art",
            "Geography",
            "History",
            "Entertainment",
            "Sports"
        ],
        "current_category": [],
        "questions": [
            {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            }
            ... # omitted for brevity 
        ],
        "success": true,
        "total_questions": 33
    }

### DELETE '/questions/int:question_id'
* Deletes selected question by id
* Returns 200 if question is successfully deleted.
* Returns 404 if question did not exist
* Returns JSON object of deleted id, remaining questions, and length of total questions

Example: curl -X DELETE http://localhost:5000/question/2
    {
        "deleted": 2,
        "questions": [
            {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }    
            ... # omitted for brevity 
        ],
        "success": true,
        "total_questions": 32
    }

### POST '/questions'
* Creates a new question posted from the react front end.
* Fields are: answer, difficulty and category.
* Returns a success value and ID of the question.
* If search field is present will return matching expressions

Example (Create): curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '

    {"question":"Who is Tony Stark?", "answer":"Iron Man", "category":"4", "difficulty":"2"}'

    {
    ... # shortened for brevity
    "success": true, 
    "total_questions": 35
    }

Example (Search):

    curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Lestat"}'

    {
    "questions": [
        {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }
    ], 
    "success": true, 
    "total_questions": 1
    }

### GET '/categories/<cat_id>/questions'
* Returns JSON response of current_category, and the questions pertaining to that category

Example: `curl http://localhost:5000/categories/1/questions`
    {
    "current_category": {
        "id": 1, 
        "type": "Science"
    }, 
    "questions": [
        {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
        }, 
    ... # omitted for brevity
    ], 
    "success": true, 
    "total_questions": 6
    }

### POST '/quizzes'
* Generates a quiz based on category or a random selection depending on what the user chooses.
* Returns a random question

Example: `curl http://localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"type":"Art","id":2}}'`

    {
    "question": {
        "answer": "One", 
        "category": 2, 
        "difficulty": 4, 
        "id": 18, 
        "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    "success": true
    }
