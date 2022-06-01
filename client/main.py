#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import os
import pika
import sys

def main():
    if len(sys.argv) != 3:
        exit("Usage: main.py HOST PORT")

    host, port = sys.argv[1:]

    desired_messages = 10
    sent_messages = 0
    received_messages = 0

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()

    channel.queue_declare(queue="notifications")

    for i in range(desired_messages):
        sent_messages += 1

        channel.basic_publish(exchange="", routing_key="notifications", body="Hi")

        print(f"Sent message {sent_messages}")

    def callback(ch, method, properties, body):
        nonlocal received_messages
        received_messages += 1

        print(f"Received message {received_messages}")

        if received_messages == desired_messages:
            channel.stop_consuming()

    channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
