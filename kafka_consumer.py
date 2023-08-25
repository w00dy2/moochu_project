from kafka import KafkaConsumer
from json import loads, JSONDecodeError
import connection
def json_deserializer(x):
    try:
        return loads(x.decode('utf-8'))
    except JSONDecodeError:
        print(f'Error decoding message: {x.decode("utf-8")}')
        return None

# topic, broker list
consumer = KafkaConsumer(
    'user_log',
     bootstrap_servers=[connection.kafka2, connection.kafka3, connection.kafka4],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=json_deserializer,
     consumer_timeout_ms=1000
)

# consumer list를 가져온다
print('[begin] get consumer list')
for message in consumer:
    print("Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s" % (
        message.topic, message.partition, message.offset, message.key, message.value
    ))
    print(message.value[-1])
print('[end] get consumer list')
