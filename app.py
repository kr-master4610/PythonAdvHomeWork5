from flask import Flask, request, jsonify
from flask_migrate import Migrate
from database import engine, SessionLocal, Base
import models  # Импорт моделей обязателен для работы миграций
from schemas import CategoryCreate, CategoryResponse, QuestionCreate, QuestionResponse

app = Flask(__name__)

# инициализация миграций
migrate = Migrate(app, db=engine, metadata=Base.metadata)

# Эндпоинты для Категорий
@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    validated_data = CategoryCreate(**data)
    with SessionLocal() as session:
        new_category = models.Category(name=validated_data.name)
        session.add(new_category)
        session.commit()
        session.refresh(new_category)
        return jsonify(CategoryResponse.from_orm(new_category).dict()), 201

@app.route('/categories', methods=['GET'])
def get_categories():
    with SessionLocal() as session:
        categories = session.query(models.Category).all()
        return jsonify([CategoryResponse.from_orm(c).dict() for c in categories])

@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    with SessionLocal() as session:
        category = session.query(models.Category).get(id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        category.name = data.get('name', category.name)
        session.commit()
        return jsonify(CategoryResponse.from_orm(category).dict())

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    with SessionLocal() as session:
        category = session.query(models.Category).get(id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        session.delete(category)
        session.commit()
        return '', 204

# Эндпоинты для Вопросов
@app.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json()
    validated_data = QuestionCreate(**data)
    with SessionLocal() as session:
        new_question = models.Question(
            text=validated_data.text,
            answer=validated_data.answer,
            category_id=validated_data.category_id
        )
        session.add(new_question)
        session.commit()
        session.refresh(new_question)
        return jsonify(QuestionResponse.from_orm(new_question).dict()), 201

@app.route('/questions', methods=['GET'])
def get_questions():
    with SessionLocal() as session:
        questions = session.query(models.Question).all()
        return jsonify([QuestionResponse.from_orm(q).dict() for q in questions])

if __name__ == '__main__':
    app.run(debug=True)