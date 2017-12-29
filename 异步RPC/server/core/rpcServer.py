# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import pika
import uuid
import time
import os
import socket

class RpcServer(object):
    def __init__(self, *args):
        self.hosts = args[0]
        self.lock = args[1]
        self.q = args[2]
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='192.168.17.136',
            credentials=pika.PlainCredentials("admin", '123456')
        ))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange="test", exchange_type="direct")

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

        for host in self.hosts:
            self.channel.queue_bind(
                exchange="test",
                routing_key=host,
                queue=self.callback_queue
            )

    def on_response(self, ch, method, props, body):
        corr_host, target_host = props.correlation_id.split(",")
        if corr_host == self.myaddr:
            self.lock.acquire()
            self.q.put(body.decode())
            self.lock.release()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, cmd, host):
        # 发布命令
        corr_id = host + "," + self.myaddr
        self.channel.basic_publish(exchange='test',
                                   routing_key='192.168.17.136',
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,
                                       reply_to=self.callback_queue,
                                       correlation_id=corr_id,
                                   ),
                                   body=cmd)
        self.response = None

        while True:
            # 相当于非阻塞的start_consuming
            if self.response is None:
                self.connection.process_data_events()
            # 清理资源
            self.response = None
            self.target_host = None