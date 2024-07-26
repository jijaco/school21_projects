from __future__ import print_function
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
# import ships_pb2_grpc


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


class Spaceship(BaseModel):
    # model_config = {"arbitrary_types_allowed": True}
    Alignment: AlignmentType
    name: str
    length: float
    Class: ClassType
    size: int
    armedStatus: bool
    officers: List[Officer]


# class Encoder(json.JSONEncoder):
#     def default(self, o: json.Any) -> json.Any:
#         return super().default(o)


def CheckInput(spaceship: Spaceship):
    if spaceship.name == 'Unknown' and spaceship.Alignment == AlignmentType.ALLY:
        return None
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
    if len(argv) != 7:
        print("Need six arguments")
        exit(1)
    print("Will try to send located spaceship ...")
    with grpc.insecure_channel("localhost:8888") as channel:
        stub = ships_pb2_grpc.LocatedSpaceshipStub(channel)
        coordinates = ships_pb2.Coordinate()
        coordinates.right_ascension_hours = float(argv[1])
        coordinates.right_ascension_minutes = float(argv[2])
        coordinates.right_ascension_seconds = float(argv[3])
        coordinates.declination_degrees = float(argv[4])
        coordinates.declination_minutes = float(argv[5])
        coordinates.declination_seconds = float(argv[6])
        # response = stub.GetCoordinate(coordinates)
        print("Client received:")
        for responce in stub.GetCoordinate(coordinates):
            try:
                print(CheckInput(
                    Spaceship(**MessageToDict(responce))).model_dump_json())
            except:
                print("Wrong data")


if __name__ == "__main__":
    logging.basicConfig()
    run()
