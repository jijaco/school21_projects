from concurrent import futures
import logging

import grpc
import ships_pb2
import ships_pb2_grpc


class LocatedSpaceship(ships_pb2_grpc.LocatedSpaceshipServicer):
    # def PromtForSpaceship()

    def AddSpaceship(self):
        spaceship = ships_pb2.Spaceship()
        # spaceship.Alignment = ships_pb2.Spaceship.AlignmentType.ALLY
        # spaceship.name = 'susus'
        spaceship.length = 7
        # spaceship.Class = ships_pb2.Spaceship.ClassType.DREADNOUGHT
        # spaceship.size = 100000000
        # spaceship.armed_status = 1
        # spaceship.officers.extend([
        #     ships_pb2.Spaceship.Officer(
        #         first_name="syi", last_name="pizza", rank="mne"),
        #     ships_pb2.Spaceship.Officer(
        #         first_name="syi1", last_name="pizza1", rank="mne1"),
        #     ships_pb2.Spaceship.Officer(first_name="syi2", last_name="pizza2", rank="mne2")])
        coordinate = ships_pb2.Coordinate(right_ascension_hours=17,
                                          right_ascension_minutes=45,
                                          right_ascension_seconds=40.05,
                                          declination_degrees=-29,
                                          declination_minutes=0,
                                          declination_seconds=28.118)
        data = ships_pb2.SpaceshipLocationDatabase()
        data1 = data.requestedspaceship.add()
        # data1.coordinate = coordinate
        data1.coordinate.right_ascension_hours = coordinate.right_ascension_hours
        data1.coordinate.right_ascension_minutes = coordinate.right_ascension_minutes
        data1.coordinate.right_ascension_seconds = coordinate.right_ascension_seconds
        data1.coordinate.declination_degrees = coordinate.declination_degrees
        data1.coordinate.declination_minutes = coordinate.declination_minutes
        data1.coordinate.declination_seconds = coordinate.declination_seconds
        data1.spaceship.extend([spaceship])

    def GetCoordinate(self, request, context):
        spaceship = ships_pb2.Spaceship()
        spaceship.Alignment = ships_pb2.Spaceship.AlignmentType.ALLY
        spaceship.name = 'susus'
        spaceship.length = 80
        spaceship.Class = ships_pb2.Spaceship.ClassType.CORVETTE
        spaceship.size = 4
        spaceship.armed_status = 1
        spaceship.officers.extend([
            ships_pb2.Spaceship.Officer(
                first_name="syi", last_name="pizza", rank="mne"),
            ships_pb2.Spaceship.Officer(
                first_name="syi1", last_name="pizza1", rank="mne1"),
            ships_pb2.Spaceship.Officer(first_name="syi2", last_name="pizza2", rank="mne2")])

        spaceship1 = ships_pb2.Spaceship()
        spaceship1.Alignment = ships_pb2.Spaceship.AlignmentType.ENEMY
        spaceship1.name = 'amogus'
        spaceship1.length = 5
        spaceship1.Class = ships_pb2.Spaceship.ClassType.CORVETTE
        spaceship1.size = 10001000
        spaceship1.armed_status = 1
        spaceship1.officers.extend([
            ships_pb2.Spaceship.Officer(
                first_name="syiiiiiii", last_name="pizzzzzzza", rank="amne"),
            ships_pb2.Spaceship.Officer(
                first_name="syiiiiiii1", last_name="pizzzzzzza1", rank="amne1"),
            ships_pb2.Spaceship.Officer(first_name="syiiiiiii2", last_name="pizzzzzzza2", rank="amne2")])
        coordinate = ships_pb2.Coordinate(right_ascension_hours=17,
                                          right_ascension_minutes=45,
                                          right_ascension_seconds=40.05,
                                          declination_degrees=-29,
                                          declination_minutes=0,
                                          declination_seconds=28.118)

        spaceship2 = ships_pb2.Spaceship()
        spaceship2.Alignment = ships_pb2.Spaceship.AlignmentType.ENEMY
        spaceship2.name = 'sus'
        spaceship2.length = 80
        spaceship2.Class = ships_pb2.Spaceship.ClassType.CORVETTE
        spaceship2.size = 4
        spaceship2.armed_status = 1
        spaceship2.officers.extend([
            ships_pb2.Spaceship.Officer(
                first_name="syi", last_name="pizza", rank="mne"),
            ships_pb2.Spaceship.Officer(
                first_name="syi3", last_name="pizza1", rank="mne1"),
            ships_pb2.Spaceship.Officer(first_name="syi4", last_name="pizza2", rank="mne2")])

        data = ships_pb2.SpaceshipLocationDatabase()
        data1 = data.requestedspaceship.add()
        # data1.coordinate = coordinate
        data1.coordinate.right_ascension_hours = coordinate.right_ascension_hours
        data1.coordinate.right_ascension_minutes = coordinate.right_ascension_minutes
        data1.coordinate.right_ascension_seconds = coordinate.right_ascension_seconds
        data1.coordinate.declination_degrees = coordinate.declination_degrees
        data1.coordinate.declination_minutes = coordinate.declination_minutes
        data1.coordinate.declination_seconds = coordinate.declination_seconds
        data1.spaceship.extend([spaceship, spaceship1, spaceship2])
        # self.AddSpaceship()
        # return super().GetCoordinate(request, context)
        # spaceship_database = ships_pb2.SpaceshipLocationDatabase()
        # print(spaceship_database.requestedspaceship[0])
        existed_spaceships = data.requestedspaceship
        for existed_spaceship in existed_spaceships:
            # spaceships = ships_pb2.Spaceships()
            spaceship_coordinates = existed_spaceship.coordinate
            if request.right_ascension_hours != spaceship_coordinates.right_ascension_hours:
                continue
            elif request.right_ascension_minutes != spaceship_coordinates.right_ascension_minutes:
                continue
            elif request.right_ascension_seconds != spaceship_coordinates.right_ascension_seconds:
                continue
            elif request.declination_degrees != spaceship_coordinates.declination_degrees:
                continue
            elif request.declination_minutes != spaceship_coordinates.declination_minutes:
                continue
            elif request.declination_seconds != spaceship_coordinates.declination_seconds:
                continue
            else:
                for t_spaceship in existed_spaceship.spaceship:
                    yield t_spaceship
        # return spaceships


def serve():
    port = "8888"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ships_pb2_grpc.add_LocatedSpaceshipServicer_to_server(
        LocatedSpaceship(), server)
    server.add_insecure_port("localhost:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
