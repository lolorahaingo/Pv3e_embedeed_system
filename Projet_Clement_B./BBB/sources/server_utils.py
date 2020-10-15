#!/usr/bin/env python

#   ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
#  ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
#  ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
#   ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
#        ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
#  ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
#   ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########
#
# Script name:   computations.py
# Created on:    09/03/2019
# Author:        raymas
#
# Purpose:      Server utils for subscribing and publishing
#
# History:      v0.1 creation of file
#
#
# |-----------------------------------------------------------------|
# | C O N F I D E N T I A L   D O   N O T   R E D I S T R I B U T E |
# |-----------------------------------------------------------------|
import pika


class Publisher(object):

    def __init__(self, topic):
        self.s = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.s.channel()
        self.topic = topic
        self.channel.exchange_declare(exchange=self.topic, exchange_type='fanout')
        self.data = ""

    def run(self):
        while True:
            self.channel.basic_publish(exchange=self.topic, routing_key='', body=self.data)
        self.s.close()


class Subscriber(object):

    def __init__(self, topic):
        self.s = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.s.channel()
        self.topic = topic

        self.channel.exchange_declare(exchange=self.topic, exchange_type='fanout')
        self.result = self.channel.queue_declare(exclusive=True, arguments={"x-max-length": 10})
        self.queue_name = self.result.method.queue
        self.channel.queue_bind(exchange=self.topic, queue=self.queue_name)
        self.channel.basic_consume(self.callback, queue=self.queue_name, no_ack=True)

        self.data = ""

    def run(self):
        while True:
            self.channel.start_consuming()
        self.s.close()

    def callback(self, ch, method, properties, body):
        self.data = body
