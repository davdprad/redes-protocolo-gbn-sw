import socket
import time
import os

SERVER_IP = '10.0.0.8'
PORT = 5000
TIMEOUT = 2
BLOCK_SIZE = 512

def main():
    input_file = 'input.txt'

    try:
        file_size = os.path.getsize(input_file)
        print(f"[INFO] Tamanho do arquivo: {file_size} bytes")
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{input_file}' não encontrado.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    total_enviados = 0
    retransmissoes = 0

    start_time = time.time()

    with open(input_file, 'rb') as file:
        seq = 0
        while True:
            data = file.read(BLOCK_SIZE)
            if not data:
                break

            acked = False
            while not acked:
                total_enviados += 1
                packet = seq.to_bytes(1, 'big') + data
                sock.sendto(packet, (SERVER_IP, PORT))
                print(f'Enviado quadro com seq={seq}')
                try:
                    ack, _ = sock.recvfrom(1)
                    if int.from_bytes(ack, 'big') == seq:
                        acked = True
                        print(f'ACK {seq} recebido')
                except socket.timeout:
                    retransmissoes += 1
                    print(f'Timeout, reenviando seq={seq}')
            seq = 1 - seq

    print('Transmissão finalizada.')
    print('Encerrando conexão.')

    acked = False
    TO = False
    while not acked and not TO:
        total_enviados += 1
        packet = seq.to_bytes(1, 'big')
        sock.sendto(packet, (SERVER_IP, PORT))
        print(f'Enviado quadro com seq={seq}')
        try:
            ack, _ = sock.recvfrom(1)
            if int.from_bytes(ack, 'big') == seq:
                acked = True
                print(f'ACK {seq} recebido')
        except socket.timeout:
            retransmissoes += 1
            print(f'Timeout, encerrando')
            TO = True

    end_time = time.time()
    tempo_total = end_time - start_time

    sock.close()

    # Relatório final
    print("\n=== MÉTRICAS DE TRANSMISSÃO ===")
    print(f"Tamanho do arquivo: {file_size} bytes")
    print(f"Tempo total de transmissão: {tempo_total:.4f} segundos")
    print(f"Total de pacotes enviados (incluindo retransmissões): {total_enviados}")
    print(f"Total de retransmissões: {retransmissoes}")

if __name__ == '__main__':
    main()
