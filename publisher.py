#-*- coding=utf-8 -*-

#!/usr/bin/env python

import pika
import sys
import leveldb

MQ_SVR = '172.18.2.2'
#connection = pika.BlockingConnection(pika.ConnectionParameters(
#        host='112.74.68.197'))
def publish(message, exchange):
    credentials = pika.PlainCredentials('bc', 'bc123456')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   MQ_SVR, 5672, '/', credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange,
                             type='fanout')
    #message = ' '.join(sys.argv[1:]) or "info: 您好世界!hello, world!"
    ldb = leveldb.LevelDB('./distsdb')
    selected = ldb.Get(exchange)
    body = '&&'.join([message, selected])
    print body
    channel.basic_publish(exchange=exchange,
                          routing_key='',
                          body=body)
    #print(" [x] Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    message = 'advds&&/mnt/htc/bc/beautiful_country/static/userdirs/dipuadmin/advds/mov_bbb.mp4'
    publish(message, 'dipuadmin')
