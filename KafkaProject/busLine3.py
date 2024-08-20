from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import datetime
import uuid
import time

# Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Read bus data coordinates from json file
inputFile = open('./data/bus3.json')
json_array = json.load(inputFile)
coordinates = json_array['features'][0]['geometry']['coordinates']

# Create bus's checkpoint data
data = {}
def checkpoint(coordinate):
    i = 0
    while i < len(coordinate):
        data['busId'] = '003'
        data['key'] = data['busId'] + '_' + uuid.uuid4().hex
        data['timestamp'] = str(datetime.datetime.now())
        data['latitude'] = coordinate[i][1]
        data['longitude'] = coordinate[i][0]
        message = json.dumps(data)
        print(message)
        producer.send('busLine', message.encode('utf-8'))
        if i == len(coordinate) - 1:
            i = 0
        else:
            i += 1
        time.sleep(1)
        

checkpoint(coordinates)

'''
producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer('busData')
for msg in consumer:
    print (msg)
'''