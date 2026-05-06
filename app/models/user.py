from app import db
from datetime import datetime


# Abstract base class — uses SQLAlchemy's __abstract__ = True
# This tells SQLAlchemy not to create a table for BaseModel itself
class BaseModel(db.Model):
    __abstract__ = True  # SQLAlchemy-native way to declare an abstract model

    def to_dict(self):
        """Every subclass should override this — simulates abstract method contract."""
        raise NotImplementedError(f"{self.__class__.__name__} must implement to_dict()")

    @classmethod
    def get_all(cls):
        """Class method shared by all models — returns every record."""
        return cls.query.all()

    def save(self):
        """Instance method to save current object to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Instance method to delete current object from the database."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'


class User(BaseModel):
    # Primary key column
    id = db.Column(db.Integer, primary_key=True)

    # User identification fields
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Timestamp for record creation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Constructor (__init__) override
    def __init__(self, username, email):
        self.username = username
        self.email = email

    # ---------------- Properties ----------------

    @property
    def display_name(self):
        """Computed field — returns a formatted display name."""
        return self.username.capitalize()

    @property
    def email_domain(self):
        """Computed field — extracts the domain from the email address."""
        return self.email.split('@')[-1]

    # ---------------- Class Methods ----------------

    @classmethod
    def find_by_email(cls, email):
        """Class method — looks up a user by email address."""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        """Class method — looks up a user by username."""
        return cls.query.filter_by(username=username).first()

    # ---------------- Static Methods ----------------

    @staticmethod
    def is_valid_email(email):
        """Static method — validates email format without needing an instance."""
        return '@' in email and '.' in email.split('@')[-1]

    # ---------------- Abstract method implementation ----------------

    def to_dict(self):
        """Converts the User object to a plain dictionary (e.g. for JSON APIs)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<User {self.username}>'
