#!usr/bin/env python3
from faker import Faker
from app import app
from models import db, Car, Customer, car_customers, Review
from random import randint, choice as rc

fake = Faker()

with app.app_context():
    Car.query.delete()
    Customer.query.delete()

    bmw = Car(
        name= "BMW",
        image_url= "https://hips.hearstapps.com/hmg-prod/image_urls/bmw-1669908626.jpeg?crop=0.801xw:0.601xh;0.151xw,0.254xh&resize=800:*",
        color="Black",
        description= "So BMW's smallest crossover has grown. In fact, a glance at the specifications shows that the new model approaches the exterior dimensions of the very first X3, launched in the mid-2000s.",
        year=2020
    )
    audi=Car(
        name= "Audi",
        image_url= "https://hips.hearstapps.com/hmg-prod/image_urls/audi-1669908451.jpeg?crop=0.824xw:0.673xh;0.155xw,0.277xh&resize=800:*",
        color="Blue",
        description= "Audi is one of today's most successful luxury brands, having effectively leveraged its minimalist styling and Quattro all-wheel-drive system into a compelling image_url of modernity and innovation.",
        year= 2019
    )
    mercerdes =Car(
        name= "Mercedes",
        image_url= "https://hips.hearstapps.com/hmg-prod/image_urls/mercedes-benz-1669908909.jpeg?crop=0.699xw:0.522xh;0.301xw,0.478xh&resize=800:*",
        color="Maroon",
        description= "The German luxury-car legend is known for high-dollar, high-tech premium sedans, SUVs, coupes, wagons, and convertibles. At one end of spectrum is the CLA-class, which is a great subcompact sedan.",
        year= 2021
    )
    chevrolet=Car(
        name= "Chevrolet",
        image_url= "https://hips.hearstapps.com/hmg-prod/image_urls/chevrolet-1669909255.jpeg?crop=0.803xw:0.604xh;0.153xw,0.291xh&resize=800:*",
        color="Grey",
        description= " Chevrolet has for decades leveraged its all-American heritage to foster showroom success. As a full-line automaker fielding a diverse product lineup, many of its vehicles are also available from other General Motors brands.",
        year= 2018
    )
    porshe=Car(
        name= "Porsche",
       image_url= "https://hips.hearstapps.com/hmg-prod/image_urls/porsche-1669909866.jpeg?crop=1.00xw:0.753xh;0,0.100xh&resize=800:*",
       color="Red",
       description= "Having established its status in the sports-car hall of fame with the legendary 911, Porsche also makes some of the best SUVs to be had. The Macan is a realistic choice as a daily driver, offering the performance of a sports car with the utility of an SUV.",
       year= 2022
    )
    bentley=Car(
        name= "Bentley",
        image_url= "https://hips.hearstapps.com/hmg-prod/images/bentley-1669908521.jpeg?crop=0.803xw:0.604xh;0.0635xw,0.200xh&resize=800:*",
        color="Silver",
        description= "Bentley offers a compelling blend of old-world British charm mixed with modern luxury tech and performance courtesy of its owner, the Volkswagen Group.entley recently expanded into the realm of SUVs with the Bentayga joining the ranks of the Flying Spur sedan and Continental GT coupe.",
        year= 2010
    )
    db.session.add_all([bmw, audi, mercerdes, chevrolet, porshe, bentley])

    customers = []
    for i in range(10):
        customer=Customer(
            username=fake.first_name(),
            _password_hash = fake.password(),
        )
        customers.append(customer)
    db.session.add_all(customers)

    reviews = []
    for customer in customers:
        for i in range(20):
            review = Review(
            comments=fake.sentence(),
            rating = randint(1, 5),
            car_id = randint(1, 5),
            customer_id = randint(1, 10)
        )
        reviews.append(review)
    db.session.add_all(reviews)

    for car in [bmw, audi, mercerdes, chevrolet, porshe, bentley]:
        r=rc(reviews)
        car.review=r
        reviews.remove(r)

    combinations = set()
    for _ in range(10):
        car_id = randint(1, 5)
        customer_id = randint(1, 10)

        if (car_id, customer_id) in combinations:
            continue
        combinations.add((car_id, customer_id))
        car_customer_data = {"car_id": car_id, "customer_id": customer_id}
        statement = db.insert(car_customers).values(car_customer_data)
        db.session.execute(statement)
        db.session.commit()
    db.session.commit()

