import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
                            'student', 'student',
                            'localhost:5432',
                            self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.new_question = {
                'question': 'Differentiate between a SE and a Developer',
                'answer': 'Different titles',
                'category': 3,
                'difficulty': 3
            }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    def test_get_questions_paginated_success(self):
        r = self.client().get('/questions')
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_404_requesting_invalid_page(self):
        r = self.client().get('/questions?page=50000')
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'Resource Not Found'])

    def test_get_categories_success(self):
        r = self.client().get('/categories')
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions_by_category_success(self):
        r = self.client().get('/categories/1/questions')
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])

    def test_404_get_questions_by_category(self):
        r = self.client().get('/categories/50000/questions')
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_add_new_question_success(self):
        r = self.client().post('/questions', json=self.new_question)
        data = json.loads(r.data)

        self.assertTrue(r.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_422_add_new_question_without_input(self):
        r = self.client().post('/questions', json={})
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Processable')

    def test_delete_question_success(self):
        r = self.client().delete('/questions/1')
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_questins'])
        self.assertTrue(data['questions'])

    def test_422_delete_nonexistent_question(self):
        r = self.client().delete('/questions/50000')
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Processable')

    def test_search_questions_successs(self):
        r = self.client().post('/questions', json={'searchTerm': 'e'})
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_422_search_questions_without_input(self):
        r = self.client().post('/questions', json={'searchTerm': None})
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Processable')

    def test_get_quiz_success(self):
        r = self.client().post('/quizzes', json={
            'previous_questions': [1],
            'quiz_category': {'id': '5', 'type': 'Science'}
        })

        data = json.loads(r.data)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['category'], 5)

    def test_422_get_quiz(self):
        r = self.client().post('/quizzes', json={
            'previous_questions': []
        })
        data = json.loads(r.data)

        self.assertEqual(r.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Processable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
