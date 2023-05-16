from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship




class NilmModel(Model):
    """
    A class of the NILM models that have been pre-trained in the first part
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(100), unique=True, nullable=True)

    def __repr__(self) -> str:
        return self.name

class Appliance(Model):
    """
    A class representing an appliance that was modelled in the first part
    """
    id = Column(Integer, primary_key=True)
    label = Column(String(50), unique=True, nullable=False)

    def __repr__(self) -> str:
        return self.label

class ModelInstance(Model):
    """
    A class representing an instance of the model included in NilmModel
    """
    id_appliance = Column(Integer, ForeignKey('appliance.id'), nullable = False)
    appliance = relationship('Appliance')
    id_model = Column(Integer, ForeignKey('nilmModel.id'), nullable = False)
    model = relationship('NilmModel')
    path_weights = Column(String(50), unique=True, nullable=True)
    mean = Column(float, nullable=False)
    std = Column(float, nullable=False)
    metadata = Column(String(500), unique=True, nullable=True)

    def __repr__(self) -> str:
        return super().__repr__()

class History(Model):
    """
    A class to save the hsitorical data of the users
    """
    id_user = Column(Integer, ForeignKey('appliance.id'), nullable = False)