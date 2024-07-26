import redis
import json
import argparse
import logging
import re


def change_transaction(transaction: dict):
    trans: dict = transaction.copy()

    t = trans['metadata']['from']
    trans['metadata']['from'] = trans['metadata']['to']
    trans['metadata']['to'] = t

    return trans


parser = argparse.ArgumentParser()
parser.add_argument('-e', '--bad-guys', type=str, nargs='+',
                    help='List of bad guys account numbers separated by commas')
args = parser.parse_args()

if not args.bad_guys:
    logging.error("Bad guys list not provided.")

bad_guys: list = list(map(int, re.split(r'[ ,]+', ','.join(args.bad_guys))))

args = parser.parse_args()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe('transactions')
for message in pubsub.listen():
    if message['type'] == 'message':
        transaction: dict = json.loads(message['data'])
        if transaction['metadata']['to'] in bad_guys and transaction['amount'] > 0:
            transaction = change_transaction(transaction)
        print(transaction)
