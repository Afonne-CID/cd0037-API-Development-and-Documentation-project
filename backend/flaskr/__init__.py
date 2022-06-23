from locale import currency
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_selection(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formated_selection = [question.format() for question in selection]
    current_selections = formated_selection[start:end]

    return current_selections
    

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response


    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        }), 200



    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_selection(request, selection)
        categories = Category.query.order_by(Category.id).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': [category.format() for category in categories],
            'current_category': []
        }), 200


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)
            if not question:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_selection(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(selection)
            }), 200

        except Exception as e:
            abort(422)


    @app.route('/questions', methods=['POST'])
    def add_question():

        search = request.args.get('searchTerm', None)

        try:
            if search:
                ''''''
                question = Question.query.ilike(f'%{search}%').all()

            else:
                ''''''
                question = Question(**request.form)
                question.insert()
            
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_selection(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
            }), 200

        except Exception as e:
            abort(422)


    @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(cat_id):

        cat_id += 1
        category = Category.query.filter_by(id=cat_id).first()
        selection = Question.query.order_by(Question.id).filter(Question.category==cat_id).all()
        current_questions = paginate_selection(request, selection)
        categories = Category.query.order_by(Category.id).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': [category.format() for category in categories],
            'current_category': category.format()
        }), 200


    @app.route('/quizzes', methods=['POST'])
    def start_quiz():
        try:
            ''''''
            prev_questions = request.args.get('previous_questions', None)
            quiz_category = request.args.get('quiz_category', None)
            cat_id = quiz_category['id']

            if cat_id == 0:
                ''''''
                questions = Question.filter(
                    Question.id.notin_(prev_questions)).all()
            else:
                ''''''
                questions = Question.filter(
                    Question.id.notin_(prev_questions),
                    Question.category==cat_id
                    ).all()
            
            question = None
            if questions:
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            }), 200

        except Exception as e:
            abort(422)


    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not Processable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500


    return app