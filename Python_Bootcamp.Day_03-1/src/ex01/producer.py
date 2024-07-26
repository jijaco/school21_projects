import json
import redis
import logging
import random
import argparse
import time


def generate_message() -> dict:
    sender_number: int = random.randrange(1111111111, 9999999999, 1111111111)
    recepient_number: int = random.randrange(
        1111111111, 9999999999, 1111111111)
    amount: int = random.randint(-100000, 100000)

    random_subdict: dict = {'from': sender_number, 'to': recepient_number}
    random_dict: dict = dict(metadata=random_subdict, amount=amount)

    return random_dict


def generate_wrong_message() -> dict:
    sender_number: int = random.randint(-1000, 1000)
    recepient_number: int = random.randint(-1000, 1000)
    amount: int = random.randint(-100000, 100000)

    random_subdict: dict = {'from': sender_number, 'to': recepient_number}
    random_dict: dict = dict(metadata=random_subdict, amount=amount)

    return random_dict


def send_message(message: dict, number_of_message: int, r):
    start_msg = 'FROM {} TO {} SENT: {}'
    error_msg1 = 'FROM {} TO {} NOT SENT: Must be positive number'
    error_msg2 = 'FROM {} TO {} NOT SENT: Must be ten digits'

    if message["metadata"]["from"] <= 0 or len(str(message["metadata"]["to"])) <= 0:
        logging.basicConfig(
            format='%(threadName)s %(name)s %(levelname)s: %(message)s',
            level=logging.ERROR)

        logging.error(error_msg1.format(
            message['metadata']['from'], message['metadata']['to']))
    elif len(str(message["metadata"]["from"])) != 10 or len(str(message["metadata"]["to"])) != 10:
        logging.basicConfig(
            format='%(threadName)s %(name)s %(levelname)s: %(message)s',
            level=logging.ERROR)

        logging.error(error_msg2.format(
            message['metadata']['from'], message['metadata']['to']))
    else:
        logging.basicConfig(
            format='%(threadName)s %(name)s %(levelname)s: %(message)s',
            level=logging.INFO)

        string_json = json.dumps(message)
        r.publish('transactions', string_json)
        logging.info(start_msg.format(
            message['metadata']['from'], message['metadata']['to'], message['amount']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('number', type=int, nargs='?', default=5)
    parser.add_argument('-t', '--test', type=str, nargs='?', const='default')
    args = parser.parse_args()
    number_of_message: int = 0

    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    pubsub = r.pubsub()

    if args.test:
        while number_of_message < 5:
            number_of_message += 1
            message: dict = generate_wrong_message()
            send_message(message, number_of_message, r)
    else:
        while True:
            message: dict = generate_message()
            send_message(message, number_of_message, r)
            time.sleep(2)
