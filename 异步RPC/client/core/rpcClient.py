# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import pika
import uuid
import time
import os

class RpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='192.168.17.136',
            credentials=pika.PlainCredentials("admin", '123456')
        ))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        # consumer端发给producer端消息时，将自己的id也一起发送，处理消息时通过这个标志位判断是不是自己要处理的消息
        if self.corr_id == props.correlation_id:
            res = os.popen(body.decode()).read()
            self.response = res.encode("utf-8")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body='')
        while self.response is None:
            # 相当于非阻塞的start_consuming
            self.connection.process_data_events()
            # print('waiting....')
            time.sleep(0.5)
        return int(self.response)