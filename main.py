import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
import blockchain as bl
#создаем экземпляр узла
app = Flask(__name__)

#генерируем уникальный на глобальном уровне адрес для этого узла
node_identifier = str(uuid4()).replace('-','')

#Создаем экземпляр блокчейна
blockchain=bl.Blockchain()


#Создание конечной точки /mine, которая является GET-запросом;
@app.route('/mine', methods=['GET'])
def mine():
    # Мы запускаем алгоритм подтверждения работы, чтобы получить следующее подтверждение…
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Мы должны получить вознаграждение за найденное подтверждение
    # Отправитель “0” означает, что узел заработал крипто-монету
    blockchain.new_transaction(
    sender = "0",
    recipient = node_identifier,
    amount = 1,
    )

    # Создаем новый блок, путем внесения его в цепь
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
    'message': "New Block Forged",
    'index': block['index'],
    'transactions': block['transactions'],
    'proof': block['proof'],
    'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


#Создание конечной точки /transactions/new, которая является POST-запросом, так как мы будем отправлять туда данные;
@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values=request.get_json()
    #Убедимся в наличии необходимых данных
    required=['sender','recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values',400
    index=blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response={'message': f'Transaction will be added to Block {index}'}
    return jsonify(response),201


#Создание конечной точки /chain, которая возвращает весь блокчейн;
@app.route('/chain', methods=['GET'])
def full_chain():
    response={
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response), 200

#Запускает сервер на порт: 5000.
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)