from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError(f'{key.capitalize()} cannot be empty.')
        if self.__class__.query.filter_by(name=name).first():
            raise ValueError(f'Duplicate {key}.')
        return name

    @validates('phone_number')
    def validate_phone_number(self, _, phone_number):
        if not phone_number.isdigit():
            raise ValueError('Phone number must contain only numbers.')
        if len(phone_number) != 10:
            raise ValueError('Phone number must be exactly 10 digits.')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word.lower() in title.lower() for word in clickbait_words):
            raise ValueError(
                f'{key.capitalize()} must include one of the following values: {clickbait_words}.'
            )
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError(
                f'{key.capitalize()} must be at least 250 characters long.')
        return content

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
