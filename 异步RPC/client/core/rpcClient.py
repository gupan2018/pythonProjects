# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import pika
import uuid
import time
import os
import socket

class RpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='192.168.17.136',
            credentials=pika.PlainCredentials("admin", '123456')
        ))

        self.channel = self.connection.channel()

        # 声明exchange
        self.channel.exchange_declare(
            exchange="test",
            exchange_type="direct"
        )

        # 随机生成消息队列
        result = self.channel.queue_declare(
            exclusive=True
        )
        self.callback_queue = result.nethod_queue

        # 注册处理函数
        self.channel.basic_consume(
            consumer_callback=self.on_response,
            queue=self.callback_queue,
            no_ack=True
        )

        # 获取本机ip地址
        myname = socket.getfqdn(socket.gethostname())
        self.myaddr = socket.gethostbyname(myname)

        self.channel.queue_bind(
            exchange="test",
            routing_key=self.myaddr,
            queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        if props.correlation_id == self.myaddr:
            self.target_host = props.user_id
            res = os.popen(body.decode()).read()
            self.response = res.encode("utf-8")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self):
        self.response = None

        while True:
            # 相当于非阻塞的start_consuming
            while self.response is None:
                self.connection.process_data_events()

            # 当response不是None时，发布消息
            self.channel.basic_publish(exchange='test',
                                       routing_key='rpc_queue',
                                       properties=pika.BasicProperties(
                                           reply_to=self.callback_queue,
                                           correlation_id=self.target_host,
                                           user_id=self.myaddr
                                       ),
                                       body=self.response)
            # 清理资源
            self.response = None
            self.target_host = None

                # 可以在这里干其他事，实现非阻塞
                # time.sleep(0.5)
            # return int(self.response)