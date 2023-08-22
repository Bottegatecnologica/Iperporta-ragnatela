from vosk import Model, KaldiRecognizer
from pythonosc import udp_client
import time
import pyaudio
import socket
import threading

# Inserisci l'indirizzo IP e la porta corretti di TouchDesigner
touchdesigner_ip = 'localhost'
touchdesigner_port = 12345
terminate_threads = False

# Dichiarazione della variabile per tenere traccia dell'ultima istanza inviata
ultima_istanza_inviata = None

# Crea il client
client = udp_client.SimpleUDPClient(touchdesigner_ip, touchdesigner_port)

# Crea il socket per la comunicazione
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)  # Indirizzo e porta del server
sock.bind(server_address)
sock.listen(1)

#Tabella
def cambia_istanza(parola, istanza_corrente, istanze):
    nuove_istanze = {
         0: { #START
            "start": 1,
            "icona": 1
        },
        1: { #scorcio
            "suoni": 3,
            "fiori": 4,
            "istante": 2,
            "stop": 0
        },
        2: { #ora
            "climax": 15,
            "stop": 0
            
        },
        3: { #silenzio
            "vettori": 16,
            "linfe": 13,
            "stop": 0
            
        },
        4: { #crogioli di sole
            "sensi": 5,
            "sole": 6,
            "muori": 7,
            "stop": 0
        },
        5: { #colori primari
            "reale": 9,
            "stop": 0
        },
        
         6: { #il guinzaglio del sole
            "biotti": 14,
            "parole": 23,
            "stop": 0
        },
        7: { #una densa partizione
            "attrito":8,
            "sazi": 11,
            "stop": 0
            
        },
       8: { #ohm
            "rovente": 16,
            "spezza": 10,
            "colore": 5,
            "stop": 0
        },
        9: { #seme immortale
            "crepa": 10,
            "stop": 0
            
        },
        10: { #avvio
            "nemico": 20,
            "stop": 0
            
        },
        11: { #pilota
            "dogane":8,
            "fulmini": 12,
            "stop": 0
            
        },
         12: { #boato splendente
            "morente": 10,
            "stop": 0
        },
        13: { #l'orto
            "tavolo": 21,
            "stop": 0
            
        },
        14: { #surfconscio
            "gemelli": 16,
            "stop": 0
            
        },
        15: { #pudore
            "luce": 22,
            "spogliare": 14,
            "stop": 0
            
        },
         16: { #negativo e positivo
            "canto": 17,
            "notte": 12,
            "stop": 0
        },
        17: { #la sublime impronta
            "amore": 18,
            "stop": 0
        },
        18: { #asimmetrico equilibrio
            "nidi": 19,
            "finestre": 13,
            "stop": 0
        },
        19: { #compro luce
            "scivolo": 20,
            "stop": 0
        },
        20: { #gioco
            "gioco": 23,
            "stop": 0
           
        },
        21: { #la tovaglia sulle stelle
            "infinito": 17,
            "cuore": 10,
            "stop": 0
        },
        22: { #la brace
            "luce": 19,
            "istante": 21,
            "stop": 0
            
        },
        23: { #ventaglio
            "delirio": 1,
            "stop": 0
        }

        #altre istanze / aggiungi attributi nome e ID
    }

        #dispatcher

    if istanza_corrente in nuove_istanze and parola in nuove_istanze[istanza_corrente]:
        return nuove_istanze[istanza_corrente][parola]
    else:
        return istanza_corrente
        #divisore
def estrai_parole(testo):
    
    parole = testo.lower().split()
    return parole

# Handle client
def handle_client(connection, address):

    global istanza_corrente
    while not terminate_threads:
    

        data = connection.recv(1024)
        if not data:
            break

        transcribed_text = data.decode()
        parole = estrai_parole(transcribed_text)

        nuova_istanza = None
        for parola in parole:
            nuova_istanza = cambia_istanza(parola, istanza_corrente, istanze)

            if nuova_istanza != istanza_corrente:
                istanza_corrente = nuova_istanza
                print(f"Istanza corrente: {istanza_corrente}")


    connection.close()

# Ricezione audio
def audio_recognition():
    global istanza_corrente

    while not terminate_threads:
        
        # Resto del thread

        data = stream.read(4096)

        if recognizer.AcceptWaveform(data):

            text = recognizer.Result()
            transcribed_text = text[14:-3]  # Estrai il testo trascritto

            parole = estrai_parole(transcribed_text)

            nuova_istanza = None
            for parola in parole:
                nuova_istanza = cambia_istanza(parola, istanza_corrente, istanze)

                if nuova_istanza != istanza_corrente:
                    istanza_corrente = nuova_istanza
                    print(f"Istanza corrente: {istanza_corrente}")
            
            print(f"Testo trascritto: {transcribed_text}")

# Funzione per inviare il messaggio tramite TCP/IP
def invia_messaggio_tcp(istanza_corrente, connection):
    try:
        
        # Converti il valore di istanza_corrente in una stringa
        msg = str(istanza_corrente)

        # Invia il messaggio al componente TouchDesigner tramite la connessione TCP/IP
        connection.sendall(msg.encode())
        print(f"Inviato messaggio TCP/IP: {msg}")

    except:
        pass

## Main
if __name__ == "__main__":

    istanza_corrente = 0
    istanze = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    model = Model(r"C:\Users\yourdirectoryfor the model")
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=32768)
    stream.start_stream()
    audio_thread = threading.Thread(target=audio_recognition)
    audio_thread.start()

    print("In attesa di connessioni...")

    while True:

        connection, client_address = sock.accept()
        print(f"Connessione accettata da {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(connection, client_address))
        client_handler.start()

        while True:

            # Verifica se l'istanza corrente è diversa dall'ultima istanza inviata
            if istanza_corrente != ultima_istanza_inviata:

                # Invia il messaggio TCP/IP con l'istanza corrente
                invia_messaggio_tcp(istanza_corrente, connection)

                # Aggiorna l'ultima istanza inviata
                ultima_istanza_inviata = istanza_corrente

            
            time.sleep(0.1)
