from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Створення додатку
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app) #  об'єкт SQLAlchemy


# Створюємо клас для статті
class Article(db.Model): # все наслідуємо від об'єкта db.Model
    id = db.Column(db.Integer, primary_key=True) # primary_key=True - унікальність кожного id
    title = db.Column(db.String(100), nullable=False) # назва, nullable=False - не може бути пустим
    intro = db.Column(db.String(300), nullable=False) # вступна частина
    text = db.Column(db.Text, nullable=False) # основний текст
    date = db.Column(db.DateTime, default=datetime.utcnow) # дата публікації

    def __repr__(self): # магічний метод; буде видаватись об'єкт Article і його id
        return '<Article %r>' % self.id


# Декоратор (URL адрес)
@app.route("/") # "/" - головна сторінка нашого сайту
@app.route("/home")
def index():
    return render_template('index.html')


@app.route("/about") # сторінка про наш сайт
def about():
    return render_template('about.html')


@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all() # всі записи сортувати по даті
    return render_template('posts.html', articles=articles) # в шаблон articles передаємо стисок articles


@app.route("/posts/<int:id>")
def post_detail(id):
    article = Article.query.get(id) # отримували інформацію про статтю з БД
    return render_template('post_detail.html', article=article)


@app.route("/posts/<int:id>/del")
def post_delete(id):
    article = Article.query.get_or_404(id) # якщо не буде знайдена стаття видасть помилку 404

    try:
        db.session.delete(article)  # видаляємов базу даних
        db.session.commit()  # зберігаємо базу даних
        return redirect('/posts')
    except:  # обробка помилок
        return "При видаленні статті виникла помилка"


@app.route("/posts/<int:id>/update", methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)  # получаємо потрібну статтю і записуємо в змінну article
    if request.method == "POST":  # редагуємо статтю
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()  # оновлюємо article в базу даних
            return redirect('/posts')
        except:  # обробка помилок
            return "При редагуванні статті виникла помилка"
    else:
        return render_template('post_update.html', article=article)


@app.route("/create-article", methods=['POST', 'GET']) #  сторінка створення статті
def create_article():
    if request.method == "POST": # заповнюємо статтю
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try: # додавання статті в базу даних
            db.session.add(article) # доваляємо article в базу даних
            db.session.commit() # зберігаємо article в базу даних
            return redirect('/posts')
        except: # обробка помилок
            return  "При добавлені статті виникла помилка"
    else:
        return render_template('create-article.html')

# Запуск додатку
if __name__ == "__main__":
    app.run(debug=True) # Запуск локального веб-сервера, debug=True - щоб бачити всі полимики в браузері