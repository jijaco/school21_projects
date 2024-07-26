from __future__ import print_function
from google.protobuf.json_format import MessageToJson
from sys import argv
import logging
import json
import grpc
import ships_pb2
import ships_pb2_grpc


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
            print(MessageToJson(responce))


if __name__ == "__main__":
    logging.basicConfig()
    run()
