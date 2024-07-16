from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'my_topic',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

with open('data.json', 'w') as f:
    for message in consumer:
        json.dump(message.value, f)
        f.write('\n')
