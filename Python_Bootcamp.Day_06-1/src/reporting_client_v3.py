from __future__ import print_function
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import ARRAY
from sqlalchemy import PickleType
from sqlalchemy import Table, MetaData, func, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import declarative_base, aliased
from sqlalchemy.orm import relationship
import ships_pb2
import ships_pb2_grpc
import grpc
import json
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Annotated
from google.protobuf.json_format import MessageToJson, MessageToDict
from sys import argv
import logging
from enum import Enum
from typing import List


class AlignmentType(str, Enum):
    ALLY = 'ALLY'
    ENEMY = 'ENEMY'


class ClassType(str, Enum):
    CORVETTE = 'CORVETTE'
    FRIGATE = 'FRIGATE'
    CRUISER = 'CRUISER'
    DESTROYER = 'DESTROYER'
    CARRIER = 'CARRIER'
    DREADNOUGHT = 'DREADNOUGHT'


class Officer(BaseModel):
    firstName: str
    lastName: str
    rank: str


Base = declarative_base()


class Spaceships(Base):
    __tablename__ = "CorrectSpaceships"

    alignment = Column(String(5))
    name = Column(String(), primary_key=True)
    length = Column(Integer)
    _class = Column(String(15))
    size = Column(Float)
    armedStatus = Column(Boolean)

    UniqueConstraint('alignment', 'name', name='u_an')


class Officers(Base):
    __tablename__ = "certainofficers"

    id = Column(Integer, primary_key=True)
    shipname = Column(String(), ForeignKey("CorrectSpaceships.name"))
    shipalignment = Column(String(5))
    firstName = Column(String())
    lastName = Column(String())
    rank = Column(String())

    shiprel = relationship("Spaceships", back_populates="officers")

    ForeignKeyConstraint(['shipname', 'shipalignment'],
                         ['CorrectSpaceships.name', 'CorrectSpaceships.alignment'])


Spaceships.officers = relationship(
    "Officers", back_populates="shiprel")


class Traitors(Base):
    __tablename__ = 'traitors'

    id = Column(Integer, primary_key=True)
    firstName = Column(String())
    lastName = Column(String())
    rank = Column(String())


class Spaceship(BaseModel):
    Alignment: AlignmentType
    name: str
    length: float
    Class: ClassType
    size: int
    armedStatus: bool
    officers: List[Officer]


def CheckInput(spaceship: Spaceship):
    if spaceship.Class == ClassType.CORVETTE:
        if (spaceship.length >= 80 and spaceship.length <= 250) and (spaceship.size >= 4 and spaceship.size <= 10):
            return spaceship
    elif spaceship.Class == ClassType.FRIGATE:
        if (spaceship.length >= 300 and spaceship.length <= 600) and (spaceship.size >= 10 and spaceship.size <= 15) and spaceship.Alignment == AlignmentType.ALLY:
            return spaceship
    elif spaceship.Class == ClassType.CRUISER:
        if (spaceship.length >= 500 and spaceship.length <= 1000) and (spaceship.size >= 15 and spaceship.size <= 30):
            return spaceship
    elif spaceship.Class == ClassType.DESTROYER:
        if (spaceship.length >= 800 and spaceship.length <= 2000) and (spaceship.size >= 50 and spaceship.size <= 80) and spaceship.Alignment == AlignmentType.ALLY:
            return spaceship
    elif spaceship.Class == ClassType.CARRIER:
        if (spaceship.length >= 1000 and spaceship.length <= 4000) and (spaceship.size >= 120 and spaceship.size <= 250) and spaceship.armedStatus == 0:
            return spaceship
    elif spaceship.Class == ClassType.DREADNOUGHT:
        if (spaceship.length >= 5000 and spaceship.length <= 20000) and (spaceship.size >= 300 and spaceship.size <= 500):
            return spaceship
    return None


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    # if len(argv) != 7:
    #     print("Need six arguments")
    #     exit(1)
    print("Will try to send located spaceship ...")
    with grpc.insecure_channel("localhost:8888") as channel:
        stub = ships_pb2_grpc.LocatedSpaceshipStub(channel)
        print("Client received:")
        engine = create_engine(
            "postgresql://postgres:Gad777333@localhost:5432/postgres")
        # metadata = MetaData()
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            if argv[1] == 'list_traitors':
                list_of_traitors = session.query(Traitors)
                for traitor in list_of_traitors:
                    traitor_dict = {'first_name': traitor.firstName,
                                    'last_name': traitor.lastName, 'rank': traitor.rank}
                    print(json.dumps(traitor_dict))
                pass
            else:
                coordinates = ships_pb2.Coordinate()
                coordinates.right_ascension_hours = float(argv[-6])
                coordinates.right_ascension_minutes = float(argv[-5])
                coordinates.right_ascension_seconds = float(argv[-4])
                coordinates.declination_degrees = float(argv[-3])
                coordinates.declination_minutes = float(argv[-2])
                coordinates.declination_seconds = float(argv[-1])
                if argv[1] == 'scan':
                    Officers_alias = aliased(Officers)
                    s = session.query(
                        func.concat(
                            Officers.firstName, ' ',
                            Officers.lastName
                        ).label(
                            'ful_name'
                        )
                    ).group_by(
                        'firstName', 'lastName'
                    ).having(
                        func.count(
                            '*'
                        ) > 1
                    ).subquery()
                    s = session.query(
                        Officers
                    ).where(
                        func.concat(
                            Officers.firstName, ' ',
                            Officers.lastName
                        ) == s
                    ).order_by('firstName', 'lastName', 'shipalignment')
                    x = {}
                    x['firstName'] = '1'
                    x['lastName'] = '1'
                    x['rank'] = '1'
                    if s.count() > 1:
                        for row in s:
                            if row.shipalignment == 'ALLY':
                                x['firstName'] = row.firstName
                                x['lastName'] = row.lastName
                                x['rank'] = row.rank
                            else:
                                if x['firstName'] == row.firstName and x['lastName'] == row.lastName:
                                    traitor = Traitors(
                                        id=session.query(Traitors).count() + 1,
                                        firstName=x['firstName'],
                                        lastName=x['lastName'],
                                        rank=x['rank']
                                    )
                                    session.add(traitor)
                else:
                    for responce in stub.GetCoordinate(coordinates):
                        try:
                            responce = CheckInput(
                                Spaceship(**MessageToDict(responce)))
                            print('--------------------------------------------------------------\n\n\n',
                                  [i.__dict__ for i in responce.officers], '--------------------------------------------\n\n\n')
                            print(responce.model_dump_json())
                            print('----------------------------------')
                            spaceship = Spaceships(
                                alignment=responce.Alignment,
                                name=responce.name,
                                length=responce.length,
                                _class=responce.Class,
                                size=responce.size,
                                armedStatus=responce.armedStatus
                                # officers=[
                                #     i.__dict__ for i in responce.officers]
                            )
                            # officer = Officers()
                            # num_officers = Table('certainofficers', 'id')
                            for i in responce.officers:
                                x: dict = i.__dict__
                                x['id'] = session.query(Officers).count() + 1
                                x['shipname'] = responce.name
                                x['shipalignment'] = responce.Alignment
                                print(x)
                                officer = Officers(**x)
                                spaceship.officers.append(officer)
                                session.add(officer)
                            session.add(spaceship)
                            print(
                                '-------------------------------------------------------------------------')
                        except AttributeError as e:
                            print("Wrong data")
                            print(e)

                #     spa = session.query(Spaceships).all()
                #     for i in spa:
                #         print(i.officers)
            session.commit()


if __name__ == "__main__":
    logging.basicConfig()
    run()
