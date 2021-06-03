from common.db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def match_password(self, password):
        if password != self.password:
            raise UserModel.PasswordDoesNotMatch

    class PasswordDoesNotMatch(BaseException):
        pass

    class DoesNotExist(BaseException):
        pass
   

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self):
        db.session.commit()

    @classmethod
    def get_user(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_user_by_email(cls, email):
        user =  cls.query.filter_by(email=email).first()
        if not user:
            raise UserModel.DoesNotExist
        return user

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_user(cls):
        return cls.query.all()
