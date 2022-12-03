import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request


class Blockchain(object):

    #основной класс, который отвечает за управление цепями

    def __init__(self):
        self.chain=[]
        self.current_transaction=[]
        # Создание первоначального блока прородителя
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        #Создание нового блока в блокчейне
        block = {
            'index': len(self.chain) + 1,#текущий индекс транзакции
            'timestamp': time(),#время транзакции
            'transactions': self.current_transaction, #текущая транзакция
            'proof': proof, #Доказательства проведенной работы
            'previous_hash': previous_hash or self.hash(self.chain[-1]), #хэш предыдущего блока
        }

        # Перезагрузка текущего списка транзакций
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self,sender, recipient, amount):
        #метод отвечающий за внесение транзакций в наш блок
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1 #вернет индекс блока, в который должна быть внесена транзакция, а именно следующая

    @staticmethod
    def hash(block):
        #хэширование блока
        block_string= json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        #метод возвращающий последний блок в цепочке
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Простая проверка алгоритма:
                 - Поиска числа p`, так как hash(pp`) содержит 4 заглавных нуля, где p - предыдущий
                 - p является предыдущим доказательством, а p` - новым
        :param last_proof: <int>
        :return: <int>
        """
        proof=0
        while self.valid_proof(last_proof,proof) is False:
            proof+=1
        return proof
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Подтверждение доказательства: Содержит ли hash(last_proof, proof) 4 заглавных нуля?
        :param last_proof: <int> Предыдущее доказательство
        :param proof: <int> Текущее доказательство
        :return: <bool> True, если правильно, False, если нет.
        """
        guess=f'{last_proof}{proof}'.encode()
        guess_hash=hashlib.sha256(guess).hexdigest()
        return guess_hash[:4]=="0000"