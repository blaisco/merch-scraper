import sys
import pika

class PikaClient(object):

  def __init__(self):
    # Construct a queue name we'll use for this instance only
    self.queue_name = 'test'
    self.routing_key = 'merch'
    self.host = 'localhost'
    self.port = 5672

    # Default values
    self.connected = False
    self.connecting = False
    self.connection = None
    self.channel = None
    self.message = None
    
  def publish(self, message):
    if self.connecting:
      pika.log.info('PikaClient: Already connecting to RabbitMQ')
      return
    pika.log.info('PikaClient: Connecting to RabbitMQ on ' + self.host + ':' + str(self.port))
    self.connecting = True
    self.message = message

    parameters = pika.ConnectionParameters(host=self.host,
                                      port=self.port,
                                      virtual_host="/")
     
    self.connection = pika.SelectConnection(parameters, self.on_connected)
    self.connection.ioloop.start()

  def on_connected(self, connection):
    pika.log.info('PikaClient: Connected to RabbitMQ on ' + self.host + ':' + str(self.port))
    self.connected = True
    self.connecting = False
    self.connection = connection
    self.connection.channel(self.on_channel_open)

  def on_channel_open(self, channel):
    pika.log.info('PikaClient: Channel Open, Declaring Queue')
    self.channel = channel
    channel.queue_declare(
        queue=self.queue_name, 
        durable=True,
        exclusive=False, 
        auto_delete=False,
        callback=self.on_queue_declared)

  def on_queue_declared(self, frame):
    pika.log.info('PikaClient: Queue Declared, Sending Messages')
    
    self.channel.basic_publish(
        exchange='',
        routing_key=self.routing_key,
        body=self.message,
        properties=pika.BasicProperties(
        content_type="text/plain",
        delivery_mode=1))
        
    # Close our connection
    self.connection.close()
    
    
if __name__ == '__main__':
  pika.log.setup(color=True)
  pc = PikaClient()
  pc.publish("RAWR")
