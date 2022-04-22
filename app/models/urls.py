from datetime import datetime
from random import randint
from app.models import db, ma
from string import ascii_letters


class URL(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    real_link = db.Column(db.String(700), nullable=False)

    endpoint = db.Column(db.String(10), unique=True)

    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    @staticmethod
    def add(url: str):
        _url: URL = URL(real_link=url, endpoint=URL.get_random_url())

        db.session.add(_url)
        db.session.commit()

        return _url

    def change_url(self, new_url: str):

        self.real_link = new_url
        db.session.commit()

        return self
    
    @staticmethod
    def delete(url_id: int):
        _url: URL = URL.query.get(url_id)

        if _url:
            return _url.pop()

        return _url

    def pop(self):
        
        db.session.delete(self)
        db.session.commit()
        
        return self

    @staticmethod
    def get_random_url(n=10):

        N = len(ascii_letters)
        endpoint = "".join([ascii_letters[randint(0, N)] for _ in range(n)])

        if URL.endpoint_exists(endpoint):
            return URL.get_random_url(n)

        return endpoint

    @staticmethod
    def endpoint_exists(endpoint: str) -> bool:
        _url: URL = URL.query.filter_by(endpoint=endpoint).first()
        
        return _url is not None

class URLShema(ma.SQLAlchemyAutoSchema):

    class Meta:

        model = URL
