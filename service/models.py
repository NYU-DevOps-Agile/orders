"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from typing_extensions import assert_type
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from service import app
import json
logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()
migrate = Migrate(app, db)


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Order(db.Model):
    """
    Class that represents a Order Model
    id: int
    items: list[int]
    """
    __tablename__ = "order"
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.String(63), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<User {self.user_id} Create Time={self.create_time} Status={self.status}>"

    def create(self):
        """
        Creates a YourResourceModel to the database
        """
        logger.info("Creating %s %s %s", self.id, self.create_time, self.status)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.id)
        db.session.commit()

    def delete(self):
        """ Removes a YourResourceModel from the data store """
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a YourResourceModel into a dictionary """
        return {"id": self.id, "user_id": self.user_id, "create_time": self.create_time, "status": self.status}

    def deserialize(self, data):
        """
        Deserializes a YourResourceModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try: 
            # assert_type(data["user_id"], int)
            # assert_type(data["create_time"], str)
            # assert_type(data["status"], int)
            if isinstance(data["user_id"], int):
                    self.user_id = data["user_id"]
            else:
                raise DataValidationError(
                    "Invalid type for int [user_id]: "
                    + str(type(data["user_id"]))
                )

            if isinstance(data["create_time"], str):
                self.create_time = data["create_time"]
            else:
                raise DataValidationError(
                    "Invalid type for str [create_time]: "
                    + str(type(data["create_time"]))
                )
            if isinstance(data["status"], int):
                self.status = data["status"]
            else:
                raise DataValidationError(
                    "Invalid type for int [status]: "
                    + str(type(data["status"]))
                )
        except KeyError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: missing " + error.args[0]
            ) from error
        return self

    @classmethod
    def init_db(cls, app: Flask):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the YourResourceModels in the database """
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a YourResourceModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_user_id(cls, user_id):
        """Returns all YourResourceModels with the given name

        Args:
            name (string): the name of the YourResourceModels you want to match
        """
        logger.info("Processing name query for %s ...", user_id)
        return cls.query.filter(cls.user_id == user_id)

class Items(db.Model):
        """
        Class that represents a Item-Order matching Model
        id: int
        oder_id:int
        item_id:int
        """
        __tablename__ = "items"
        app = None

        # Table Schema
        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.Integer, ForeignKey("order.id"), nullable=False)
        item_id = db.Column(db.Integer, nullable=False)

        def __repr__(self):
            return "<Order id=[{self.order_id}] Item id=[{self.item_id}]>"

        def create(self):
            """
            Creates a YourResourceModel to the database
            """
            logger.info("Creating %s", self.id)
            self.id = None  # id must be none to generate next primary key
            db.session.add(self)
            db.session.commit()

        def update(self):
            """
            Updates a YourResourceModel to the database
            """
            logger.info("Saving %s", self.name)
            db.session.commit()

        def delete(self):
            """ Removes a YourResourceModel from the data store """
            logger.info("Deleting %s", self.id)
            db.session.delete(self)
            db.session.commit()

        def serialize(self):
            """ Serializes a YourResourceModel into a dictionary """
            return {"id": self.id, "order_id": self.order_id, "item_id": self.item_id}

        def deserialize(self, data):
            """
            Deserializes a YourResourceModel from a dictionary

            Args:
                data (dict): A dictionary containing the resource data
            """
            try:
                self.items = data["item"]
                self.user_id = data["user_id"]
                self.create_time = data["create_time"]
                self.status = data["status"]
            except KeyError as error:
                raise DataValidationError(
                    "Invalid YourResourceModel: missing " + error.args[0]
                ) from error
            except TypeError as error:
                raise DataValidationError(
                    "Invalid YourResourceModel: body of request contained bad or no data - "
                    "Error message: " + error
                ) from error
            return self

        @classmethod
        def init_db(cls, app):
            """ Initializes the database session """
            logger.info("Initializing database")
            cls.app = app
            # This is where we initialize SQLAlchemy from the Flask app
            db.init_app(app)
            app.app_context().push()
            db.create_all()  # make our sqlalchemy tables

        @classmethod
        def all(cls):
            """ Returns all of the YourResourceModels in the database """
            logger.info("Processing all YourResourceModels")
            return cls.query.all()

        @classmethod
        def find(cls, by_id):
            """ Finds a YourResourceModel by it's ID """
            logger.info("Processing lookup for id %s ...", by_id)
            return cls.query.get(by_id)

        @classmethod
        def find_by_name(cls, name):
            """Returns all YourResourceModels with the given name

            Args:
                name (string): the name of the YourResourceModels you want to match
            """
            logger.info("Processing name query for %s ...", name)
            return cls.query.filter(cls.name == name)