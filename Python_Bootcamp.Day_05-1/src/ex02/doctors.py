from threading import Thread, Semaphore, RLock, Lock
from time import sleep

_semaphore = Semaphore(value=5)
lock9 = Lock()
lock10 = Lock()
lock11 = Lock()
lock12 = Lock()
lock13 = Lock()


class Doctors:
    def __init__(self) -> None:
        self.screwdrivers: int = 1
        self.blasted: int = 0
        self.number: int = -1
        self.numbers: list = [9, 10, 11, 12, 13]
        pass


class Doctor9(Doctors):
    def __init__(self) -> None:
        super().__init__()
        self.number = 9

    def use_screwdrivers(self) -> None:
        # print('Wait for lock13')
        lock13.acquire()
        # print('Wait for lock9')
        lock9.acquire()

        # print('Blasting')
        sleep(0.1)

        print(f'Doctor {self.number}: BLAST!')
        lock9.release()
        lock13.release()


class Doctor10(Doctors):
    def __init__(self) -> None:
        super().__init__()
        self.number = 10

    def use_screwdrivers(self) -> None:
        # print('Wait for lock9')
        lock9.acquire()
        # print('Wait for lock10')
        lock10.acquire()

        # print('Blasting')
        sleep(0.1)

        print(f'Doctor {self.number}: BLAST!')
        lock10.release()
        lock9.release()


class Doctor11(Doctors):
    def __init__(self) -> None:
        super().__init__()
        self.number = 11

    def use_screwdrivers(self) -> None:
        # print('Wait for lock10')
        lock10.acquire()
        # print('Wait for lock11')
        lock11.acquire()

        # print('Blasting')
        sleep(0.1)

        print(f'Doctor {self.number}: BLAST!')
        lock11.release()
        lock10.release()


class Doctor12(Doctors):
    def __init__(self) -> None:
        super().__init__()
        self.number = 12

    def use_screwdrivers(self) -> None:
        # print('Wait for lock11')
        lock11.acquire()
        # print('Wait for lock12')
        lock12.acquire()

        # print('Blasting')
        sleep(0.1)

        print(f'Doctor {self.number}: BLAST!')
        lock12.release()
        lock11.release()


class Doctor13(Doctors):
    def __init__(self) -> None:
        super().__init__()
        self.number = 13

    def use_screwdrivers(self) -> None:
        # print('Wait for lock12')
        lock12.acquire()
        # print('Wait for lock13')
        lock13.acquire()

        # print('Blasting')
        sleep(0.1)

        print(f'Doctor {self.number}: BLAST!')
        lock13.release()
        lock12.release()


d1 = Doctor9()
d2 = Doctor10()
d3 = Doctor11()
d4 = Doctor12()
d5 = Doctor13()

# threads = [Thread(target=) for i in range(5)]
thread1 = Thread(target=d1.use_screwdrivers)
thread2 = Thread(target=d2.use_screwdrivers)
thread3 = Thread(target=d3.use_screwdrivers)
thread4 = Thread(target=d4.use_screwdrivers)
thread5 = Thread(target=d5.use_screwdrivers)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
# rounds: int = 5
# for round in range(1, rounds + 1):
#     print(f'turn {round}')

#     d1.take_screwdriver(d5)
#     d1.take_screwdriver(d5)
#     d2.take_screwdriver(d1)
#     d2.take_screwdriver(d1)
#     d3.take_screwdriver(d2)
#     d3.take_screwdriver(d2)
#     d4.take_screwdriver(d3)
#     d4.take_screwdriver(d3)
#     d5.take_screwdriver(d4)
#     d5.take_screwdriver(d4)
