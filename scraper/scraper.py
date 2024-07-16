import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Hedef URL
url = 'https://scrapeme.live/shop/'

# URL'ye istek gönder
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"URL'ye erişirken bir hata oluştu: {e}")
    exit(1)

# HTML içeriğini ayrıştır
soup = BeautifulSoup(response.text, 'html.parser')

# Ürünleri topla
products = []
for product in soup.select('.product'):
    title = product.select_one('.woocommerce-loop-product__title').text
    price = product.select_one('.woocommerce-Price-amount').text
    products.append({'title': title, 'price': price})

# Kafka Producer'ı oluştur
try:
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',  # Kafka broker adresi
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except KafkaError as e:
    print(f"Kafka Producer oluşturulurken bir hata oluştu: {e}")
    exit(1)

# Ürünleri Kafka konusuna gönder
for product in products:
    try:
        future = producer.send('my_topic', product)
        result = future.get(timeout=10)  # Mesajın başarılı olup olmadığını kontrol et
        print(f"Mesaj gönderildi: {product}")
    except KafkaError as e:
        print(f"Mesaj gönderilirken bir hata oluştu: {e}")
    sleep(1)

# Producer'ı flush et ve kapat
producer.flush()
producer.close()
