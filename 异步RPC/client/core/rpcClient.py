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
        self.callback_queue = result.method.queue

        # 注册处理函数
        self.channel.basic_consume(
            consumer_callback=self.on_response,
            queue=self.callback_queue,
            no_ack=False
        )

        # 获取本机ip地址
        myname = socket.getfqdn(socket.gethostname())
        self.myaddr = socket.gethostbyname(myname)

        # 绑定到主机的routing_key
        self.channel.queue_bind(
            exchange="test",
            routing_key="192.168.17.136",
            queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        print("body:", body)
        corr_host, target_host = props.correlation_id.split(",")
        if corr_host == self.myaddr:
            res = os.popen(body.decode()).read()
            print(res)
            self.response = res.encode("utf-8")
            self.target_host = target_host
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self):
        self.response = None

        while True:
            # 相当于非阻塞的start_consuming
            if self.response is None:
                self.connection.process_data_events()
            if self.response is not None:
                # 当response不是None时，发布消息
                corr_id = self.target_host + "," + self.myaddr
                self.channel.basic_publish(exchange='test',
                                           routing_key='rpc_queue',
                                           properties=pika.BasicProperties(
                                               delivery_mode=2,
                                               reply_to=self.callback_queue,
                                               correlation_id=corr_id,
                                           ),
                                           body=self.response)
                # 清理资源
                self.response = None
                self.target_host = None

                # 可以在这里干其他事，实现非阻塞
                # time.sleep(0.5)
            # return int(self.response)