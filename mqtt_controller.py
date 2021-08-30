import json
from private import MQTT_USER, MQTT_PASS, MQTT_PORT, CLIENT_ID, BROKER
from private import SUSCRIPTION_LIST
import paho.mqtt.client as mqtt


LIGHT_STATUS = False
LIGHT_DATA = ""
LIGHT_RAW_DATA = ""

def on_message(client, userdata, message):
    global LIGHT_DATA, LIGHT_RAW_DATA
    msg = str(message.payload.decode("utf-8"))
    LIGHT_RAW_DATA = msg
    # print(" < received message ", msg)
    parser_json = json.loads(msg)
    try:
        id = parser_json['id']
        # print("El id es: ", id)
        LIGHT_DATA = str(parser_json['id'])
        client.disconnect()
    except:
        pass


# publish a message
def publish(topic, message, wait_for_ack=False):
    QoS = 2 if wait_for_ack else 0
    pass


def on_publish(client, userdata, mid):
    pass
    # print(" > published message: {}".format(mid))


def mqtt_light_change():
    global LIGHT_STATUS, LIGHT_DATA, LIGHT_RAW_DATA

    client = mqtt.Client(CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect(BROKER)

    if LIGHT_STATUS:
        for s in SUSCRIPTION_LIST:
            client.publish( s +"action", "{\"light\":\"1\"}")
        LIGHT_STATUS = False
    else:
        for s in SUSCRIPTION_LIST:
            client.publish( s +"action", "{\"light\":\"0\"}")
        LIGHT_STATUS = True
    return LIGHT_STATUS


def mqtt_read_status_lamp():
    global LIGHT_STATUS, LIGHT_DATA, LIGHT_RAW_DATA
    client = mqtt.Client(CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect(BROKER)
    for s in SUSCRIPTION_LIST:
        client.subscribe( s +"data")
    client.loop_forever()
    return LIGHT_DATA, LIGHT_RAW_DATA
