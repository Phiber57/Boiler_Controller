import socket
import time

HOST = '192.168.57.69'
PORT = 1234
INTERVALLE = 20
message = b'\xA5\x02\x11\x36'

print(f"Démarrage du client TCP - Envoi toutes les {INTERVALLE} secondes")
print("Appuyez sur Ctrl+C pour arrêter")

compteur = 0

try:
    while True:
        try:
            # Créer et connecter le socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            print(f"[{time.strftime('%H:%M:%S')}] Connecté au serveur")
            
            # Boucle d'envoi
            while True:
                client_socket.sendall(message)
                compteur += 1
                print(f"[{time.strftime('%H:%M:%S')}] Message #{compteur} envoyé")
                time.sleep(INTERVALLE)
                
        except (ConnectionRefusedError, BrokenPipeError, OSError) as e:
            print(f"[{time.strftime('%H:%M:%S')}] Connexion perdue. Reconnexion dans 5 secondes...")
            try:
                client_socket.close()
            except:
                pass
            time.sleep(5)
            
except KeyboardInterrupt:
    print("\nArrêt demandé par l'utilisateur")
finally:
    try:
        client_socket.close()
    except:
        pass
    print("Programme terminé")