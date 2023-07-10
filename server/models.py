
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt


car_customers = db.Table(
    "car_customer",
    db.Column("car_id", db.ForeignKey("cars.id"), primary_key=True),
    db.Column("customer_id", db.ForeignKey("customers.id"), primary_key=True),
    extend_existing=True
)

class Car(db.Model, SerializerMixin):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    image_url= db.Column(db.String)
    color = db.Column(db.String)
    description = db.Column(db.String)
    year= db.Column(db.Integer)
    reviews = db.relationship("Review", backref="car")
    serialize_rules = ("-customers.cars",)

    def __repr__(self):
        return f"{self.name} was manufactured in {self.year}" 
    
class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    reviews = db.relationship("Review", backref="customer")
    serialize_rules = ("-cars.customers",)

    @hybrid_property
    def password_hash(self):
        return AttributeError("Password hash should not be viewed")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode("utf-8"))

    def __repr__(self):
        return f"Customer {self.username}, ID: {self.id}"
    
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comments=db.Column(db.String)
    rating = db.Column(db.Integer)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    serialize_rules = ("-car.reviews", "-customer.reviews",)

    def __repr__(self):
        return f"Review {self.id} | comments: {self.comments}"
