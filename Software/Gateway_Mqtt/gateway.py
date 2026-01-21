import paho.mqtt.client as mqtt
import socket
import time
import struct
import json
import credential
import credential.credential
import time
import traceback

# Configuration mqtt : fill variabes (BROKER, MQTT_USERNAME, MQTT_PASSWORD)  in a file named credential/credential.py
BROKER=credential.credential.BROKER
PORT=credential.credential.PORT
MQTT_USERNAME=credential.credential.MQTT_USERNAME
MQTT_PASSWORD=credential.credential.MQTT_PASSWORD

SERVEUR_TCP=credential.credential.LOCAL_ADDRESS
PORT_TCP=1234


TOPIC_PUB_BOILER = "gatewayBBA/temperature_boiler"  # Température de la chaudière
TOPIC_PUB_OUTSIDE = "gatewayBBA/temperature_outside"  # Température extérieure
TOPIC_PUB_INSTRUCTION = "gatewayBBA/temperature_instruction"  # Température à atteindre.
TOPIC_PUB_REFERENCE = "gatewayBBA/temperature_boiler_ref"  # Température de référence 20°C.
TOPIC_PUB_DAY = "gatewayBBA/mode_day"  # 
TOPIC_PUB_NIGHT = "gatewayBBA/mode_night"  # 
TOPIC_TIMESTAMP = "gatewayBBA/timestamp"
TOPIC_STATE_BOILER = "gatewayBBA/state_boiler" # Etat de fonctionnement : 1->allumé, 0->Eteint

TOPIC_ASK_BOILER_RUNNING_MODE = "gatewayBBA/ask_boiler_running_mode" # Mode de fonctionnement : 0->Eteint, 1-> Mode manuel
TOPIC_GET_BOILER_RUNNING_MODE = "gatewayBBA/get_boiler_running_mode"
TOPIC_SET_BOILER_RUNNING_MODE = "gatewayBBA/set_boiler_running_mode"

TOPIC_ASK_ROOM_TEMPERATURES = "gatewayBBA/ask_room_temperatures" # Temperature jour et nuit
TOPIC_GET_ROOM_TEMPERATURES = "gatewayBBA/get_room_temperatures" # Temperature jour et nuit
TOPIC_SET_ROOM_TEMPERATURES = "gatewayBBA/set_room_temperatures" # Temperature jour et nuit


TOPIC_ASK_START_WATER_OUTSIDE_TEMPERATURES = "gatewayBBA/ask_start_water_temperatures" 
TOPIC_START_WATER_OUTSIDE_TEMPERATURES = "gatewayBBA/get_start_water_temperature"   # Temperature à la sortie du boiler(correspond à la temperature du depart des radiateurs) 
                                                                                # et la température de la sonde extérieure

#TOPIC_ASK_HEATING_CURVE_PARAMETERS = "gatewayBBA/ask_heating_curve_parameters"
TOPIC_GET_HEATING_CURVE_PARAMETERS = "gatewayBBA/get_heating_curve_parameters"          # Paramètre de la courbe de la loi d'eau (coefficient et parallel shift)
TOPIC_SET_HEATING_CURVE_PARAMETERS = "gatewayBBA/set_heating_curve_parameters"          # Paramètre de la courbe de la loi d'eau (coefficient et parallel shift)


TOPIC_GET_SENSORS_CELSIUS_TEMPERATURES = "gatewayBBA/get_sensors_celcius_temperatures"
TOPIC_GET_SENSORS_RAW_TEMPERATURES = "gatewayBBA/get_sensors_raw_temperatures"

TOPIC_GET_MIXING_VALVE_POSITION = "gatewayBBA/get_MIXING_VALVE_POSITION"

BOILER_PROTOCOL_MAGIC_NUMBER=0xA5

BOILER_COMMAND_GET_FIRMWARE_VERSION=0
BOILER_COMMAND_GET_SENSORS_RAW_TEMPERATURES=1 #TOPIC_GET_SENSORS_RAW_TEMPERATURES
BOILER_COMMAND_GET_SENSORS_CELSIUS_TEMPERATURES=2 #TOPIC_GET_SENSORS_CELSIUS_TEMPERATURES
BOILER_COMMAND_GET_MIXING_VALVE_POSITION=3 #TOPIC_GET_MIXING_VALVE_POSITION
BOILER_COMMAND_SET_NIGHT_MODE=4
BOILER_COMMAND_GET_DESIRED_ROOM_TEMPERATURES=5 # TOPIC_GET_ROOM_TEMPERATURES
BOILER_COMMAND_SET_DESIRED_ROOM_TEMPERATURES=6 # TOPIC_SET_ROOM_TEMPERATURES
BOILER_COMMAND_GET_TRIMMERS_RAW_VALUES=7
BOILER_COMMAND_GET_BOILER_RUNNING_MODE=8 # TOPIC_GET_BOILER_RUNNING_MODE
BOILER_COMMAND_SET_BOILER_RUNNING_MODE=9 # TOPIC_SET_BOILER_RUNNING_MODE
BOILER_COMMAND_GET_TARGET_START_WATER_TEMPERATURE=10 # TOPIC_START_WATER_OUTSIDE_TEMPERATURES
BOILER_COMMAND_GET_HEATING_CURVE_PARAMETERS=11 #TOPIC_GET_HEATING_CURVE_PARAMETERS
BOILER_COMMAND_SET_HEATING_CURVE_PARAMETERS=12 #TOPIC_SET_HEATING_CURVE_PARAMETERS
BOILER_COMMANDS_COUNT=13

def int_to_bytes(value):
    """Convertit un entier en un buffer de 2 octets."""
    return struct.pack('>H', int(value))

def int_to_byte(value):
    """Convertit un entier en un buffer de 1 octet."""
    return struct.pack('>B', int(value))


# Callback - Connexion au broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT")
        client.subscribe(TOPIC_PUB_BOILER) # S'abonner à un topic
        client.subscribe(TOPIC_PUB_OUTSIDE)
        client.subscribe(TOPIC_PUB_INSTRUCTION)
        client.subscribe(TOPIC_PUB_REFERENCE)
        client.subscribe(TOPIC_PUB_DAY)
        client.subscribe(TOPIC_PUB_NIGHT)
        client.subscribe(TOPIC_TIMESTAMP)
        client.subscribe(TOPIC_STATE_BOILER)  
        client.subscribe(TOPIC_ASK_BOILER_RUNNING_MODE)  
        client.subscribe(TOPIC_START_WATER_OUTSIDE_TEMPERATURES)
        client.subscribe(TOPIC_SET_ROOM_TEMPERATURES)
        client.subscribe(TOPIC_SET_HEATING_CURVE_PARAMETERS)
        client.subscribe(TOPIC_ASK_ROOM_TEMPERATURES)
        client.subscribe(TOPIC_ASK_START_WATER_OUTSIDE_TEMPERATURES)
        #client.subscribe(TOPIC_ASK_HEATING_CURVE_PARAMETERS)
        client.subscribe(TOPIC_SET_BOILER_RUNNING_MODE)
        client.subscribe(TOPIC_GET_SENSORS_CELSIUS_TEMPERATURES)
        client.subscribe(TOPIC_GET_SENSORS_RAW_TEMPERATURES)
    else:
        print(f"Erreur de connexion. Code : {rc}")

# Callback - Réception d'un message
def on_message(client, userdata, msg):
    print(f"Message reçu sur {msg.topic} : {msg.payload.decode()}")
    messageOk = False

    if msg.topic == TOPIC_PUB_BOILER:
        print ("TOPIC_PUB_BOILER")

    elif msg.topic == TOPIC_ASK_START_WATER_OUTSIDE_TEMPERATURES:
        print ("TOPIC_GET_START_WATER_OUTSIDE_TEMPERATURES")
        buffer = bytearray(2) 
        buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER
        buffer[1] = BOILER_COMMAND_GET_TARGET_START_WATER_TEMPERATURE    
        messageOk = True

    elif msg.topic == TOPIC_ASK_ROOM_TEMPERATURES:
        print ("TOPIC_ASK_ROOM_TEMPERATURES")
        buffer = bytearray(2)
        buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER       # Modifie le premier octet
        buffer[1] = BOILER_COMMAND_GET_DESIRED_ROOM_TEMPERATURES
        messageOk = True

    elif msg.topic == TOPIC_SET_ROOM_TEMPERATURES:
        print ("TOPIC_SET_ROOM_TEMPERATURES")
        
        parameters = msg.payload.decode().split(',')
        print (parameters)
        if len(parameters) == 2:
            buffer = bytearray(4) 
            buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER 
            buffer[1] = BOILER_COMMAND_SET_DESIRED_ROOM_TEMPERATURES
            buffer[2] = int(parameters[0]) # JOUR 
            buffer[3] = int(parameters[1]) # NUIT 
            messageOk = True

    #elif msg.topic == TOPIC_ASK_HEATING_CURVE_PARAMETERS:
    #    print ("TOPIC_ASK_HEATING_CURVE_PARAMETERS")
    #    buffer = bytearray(2)
    #    buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER       # Modifie le premier octet
    #    buffer[1] = BOILER_COMMAND_GET_HEATING_CURVE_PARAMETERS
    #    messageOk = True

    elif msg.topic == TOPIC_GET_HEATING_CURVE_PARAMETERS:
        print ("TOPIC_GET_HEATING_CURVE_PARAMETERS")
        buffer = bytearray(2) 
        buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER 
        buffer[1] = BOILER_COMMAND_GET_HEATING_CURVE_PARAMETERS   
        messageOk = True

    elif msg.topic == TOPIC_SET_HEATING_CURVE_PARAMETERS:
        print ("TOPIC_SET_HEATING_CURVE_PARAMETERS")
        
        parameters = msg.payload.decode().split(',')
        if len(parameters) == 2:
            buffer = bytearray(6) 
            buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER 
            buffer[1] = BOILER_COMMAND_SET_HEATING_CURVE_PARAMETERS
            buffer.append(int_to_bytes(parameters[0])) # 16 bits
            buffer.append(int_to_bytes(parameters[1])) # 16 bits
            messageOk = True
            
    elif msg.topic == TOPIC_GET_SENSORS_CELSIUS_TEMPERATURES:
        print ("TOPIC_GET_SENSORS_CELSIUS_TEMPERATURES")
        parameters = msg.payload.decode().split(',')
        print (f"parameters {parameters}")
        buffer = bytearray(2) 
        buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER 
        buffer[1] = BOILER_COMMAND_GET_SENSORS_CELSIUS_TEMPERATURES
        messageOk = True
        print (f"Buffer {buffer}")

    elif msg.topic == TOPIC_GET_MIXING_VALVE_POSITION:
        print ("TOPIC_GET_MIXING_VALVE_POSITION")
        parameters = msg.payload.decode().split(',')
        print (f"parameters {parameters}")
        buffer = bytearray(2) 
        buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER 
        buffer[1] = BOILER_COMMAND_GET_MIXING_VALVE_POSITION
        messageOk = True
        print (f"Buffer {buffer}")


    elif msg.topic == TOPIC_GET_SENSORS_RAW_TEMPERATURES:
        print ("TOPIC_GET_SENSORS_RAW_TEMPERATURES")
        parameters = msg.payload.decode().split(',')
        print (f"parameters {parameters}")
        
        buffer = bytearray(2) 
        buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER 
        buffer[1] = BOILER_COMMAND_GET_SENSORS_RAW_TEMPERATURES
        messageOk = True
        print (f"Buffer {buffer}")


    elif msg.topic == TOPIC_ASK_BOILER_RUNNING_MODE:
        buffer = bytearray(2)  # Crée un buffer mutable de 2 octets, initialisé à b'\x00\x00'
        buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER       # Modifie le premier octet
        buffer[1] = BOILER_COMMAND_GET_BOILER_RUNNING_MODE
        messageOk = True

    elif msg.topic == TOPIC_SET_BOILER_RUNNING_MODE:
        buffer = bytearray(3)  # Crée un buffer mutable de 2 octets, initialisé à b'\x00\x00'
        buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER       # Modifie le premier octet
        buffer[1] = BOILER_COMMAND_SET_BOILER_RUNNING_MODE
        
        if msg.payload.decode() == "0":
            buffer[2] = 0x00
            print("TOPIC_SET_BOILER_RUNNING_MODE 0")
            messageOk = True
        elif msg.payload.decode() == "1":
            buffer[2] = 0x01
            print("TOPIC_SET_BOILER_RUNNING_MODE 1")
            messageOk = True
    else:
        messageOk = False

    if messageOk == True:
        try:
            print("Envoi message a la carte")
            client_socket.sendall(buffer)
            print("Attente reponse")
            analyse_boiler(3)
            print("Fin traitement de la reponse ")

        except Exception as e:
            print(f"Exception socket")

        print(f"Fin traitement sur {msg.topic}")
    

# Initialisation du client MQTT
client = mqtt.Client()
# Attacher les callbacks
client.on_connect = on_connect
client.on_message = on_message
# Connexion au broker

bSocketClientConnected = False
while bSocketClientConnected == False:

    try:
        client.connect(BROKER, PORT)
        client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
        bSocketClientConnected = True
    except Exception as e:
        print("Exception socket")
        time.sleep(10)
    
bSocketServeurCreated = False

while bSocketServeurCreated == False:

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVEUR_TCP, PORT_TCP))
        server_socket.listen(1)  # Écoute jusqu'à 1 connexion simultanée
       
        client_socket_connecte = False
        bSocketServeurCreated = True
    except Exception as e:
        print("Exception socket")
        time.sleep(10)

def analyse_boiler(timeout=1):
    global client_socket_connecte
    try:
        client_socket.settimeout(timeout)
        data = client_socket.recv(1024)  # Taille maximale des données : 1024 octets        
        if not data:
            print("Client déconnecté.")
            client_socket_connecte = False
            client_socket.close()
        else:
            print( f"Trame recu : {data}")

            print (f"Magic : {int(data[0])} {int(BOILER_PROTOCOL_MAGIC_NUMBER)}" )
            trameDecodee =  [byte for byte in data]
            
            print( f"Trame decodee : {trameDecodee}")

            custom_keys = ["magicNumber", "key", "value1", "value2", "value3", "value4"]
            json_dict = {key: value for key, value in zip(custom_keys, trameDecodee)}
            json_string = json.dumps(json_dict, indent=4)

            print( f"json_string : {json_string}")

            if (int(data[0]) == int(BOILER_PROTOCOL_MAGIC_NUMBER)):
                if (data[1] == int(BOILER_COMMAND_GET_TARGET_START_WATER_TEMPERATURE)):
                    publier_message(TOPIC_START_WATER_OUTSIDE_TEMPERATURES, json_string)   
                elif (data[1] == int(BOILER_COMMAND_GET_DESIRED_ROOM_TEMPERATURES)):
                    publier_message(TOPIC_GET_ROOM_TEMPERATURES, json_string)  
                elif (data[1] == BOILER_COMMAND_GET_HEATING_CURVE_PARAMETERS):
                    publier_message(TOPIC_GET_HEATING_CURVE_PARAMETERS, json_string)
                elif (data[1] == BOILER_COMMAND_GET_BOILER_RUNNING_MODE):
                    publier_message(TOPIC_GET_BOILER_RUNNING_MODE, json_string) 
                elif (data[1] == BOILER_COMMAND_GET_SENSORS_RAW_TEMPERATURES):
                    publier_message(TOPIC_GET_SENSORS_RAW_TEMPERATURES, json_string) 
                elif (data[1] == BOILER_COMMAND_GET_SENSORS_CELSIUS_TEMPERATURES):
                    publier_message(TOPIC_GET_SENSORS_CELSIUS_TEMPERATURES, json_string) 
                elif (data[1] == BOILER_COMMAND_GET_MIXING_VALVE_POSITION):
                    publier_message(TOPIC_GET_MIXING_VALVE_POSITION, json_string)     
            print (f"Message publie {int(data[1])}")
        
    except socket.timeout:
        print(f"Pas de donnees")
    except Exception as e:
        print(f"Exception {e}")
        client_socket_connecte = False


def interrogation_boiler():
    print ("TOPIC_GET_ROOM_TEMPERATURES")
    buffer = bytearray(2)
    buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER       # Modifie le premier octet
    buffer[1] = BOILER_COMMAND_GET_DESIRED_ROOM_TEMPERATURES
    try:
        client_socket.sendall(buffer)
    except Exception as e:
        print(f"Exception socket {e}")
    
    analyse_boiler(3)

    buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER       # Modifie le premier octet
    buffer[1] = BOILER_COMMAND_GET_TARGET_START_WATER_TEMPERATURE

    try:
        client_socket.sendall(buffer)
    except Exception as e:
        print(f"Exception socket {e}")
    
    analyse_boiler(3)
    
    
    buffer[0] = BOILER_PROTOCOL_MAGIC_NUMBER       # Modifie le premier octet
    buffer[1] = BOILER_COMMAND_GET_TARGET_START_WATER_TEMPERATURE

    try:
        client_socket.sendall(buffer)
    except Exception as e:
        print("Exception socket {e}")

    analyse_boiler(3)

# Fonction pour publier un message
#def publier_message(topic, message):
#    client.publish(topic, message)
#    print(f"Message publié sur {topic} : {message}")


def publier_message(topic, message):
    try:
        # S'assurer que c'est une chaîne JSON
        if isinstance(message, dict):
            message_str = json.dumps(message)
        else:
            message_str = str(message)
        
        print(f"Type du message: {type(message_str)}")
        print(f"Contenu: {message_str}")
        
        # Publier
        result = client.publish(topic, message_str)
        print(f"Message publié sur {topic} : {message_str}")
        print(f"Résultat: {result}")
        
    except Exception as e:
        print(f"Erreur lors de la publication: {e}")
        traceback.print_exc()


# Boucle réseau dans un thread séparé
client.loop_start()

i = 0

# Exemple : Envoyer des commandes
try:
    while True:
        try:
            print(f"Attente connexion TCP.")
            time.sleep(2)
            client_socket, client_address = server_socket.accept()
            print (client_socket)
            client_socket_connecte = True
            time.sleep(1)
            
            #preimiere interrogation apres la connexion
            interrogation_boiler()
            
            i = 0
            while client_socket_connecte == True:
                
                analyse_boiler(1)
                i = i + 1
                #print(i)
                if i > 60: 
                    print("------------------------------------")
                    print(i)
                    interrogation_boiler()
                    i = 0
                    
        finally:
            client_socket_connecte = False
            client_socket.close()
            
finally:
    client.loop_stop()
    client.disconnect()
    print("Déconnecté du broker MQTT.")
