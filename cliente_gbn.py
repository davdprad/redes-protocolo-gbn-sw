import socket
import time
import os

SERVER_IP = '10.0.0.8'
PORT = 5000
TIMEOUT = 2
BLOCK_SIZE = 512
WINDOW_SIZE = 4  # Janela do Go-Back-N

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
        data_blocks = []
        while True:
            data = file.read(BLOCK_SIZE)
            if not data:
                break
            data_blocks.append(data)

    base = 0
    next_seq = 0
    num_blocos = len(data_blocks)

    while base < num_blocos:
        # Envia pacotes dentro da janela
        while next_seq < base + WINDOW_SIZE and next_seq < num_blocos:
            packet = next_seq.to_bytes(2, 'big') + data_blocks[next_seq]
            sock.sendto(packet, (SERVER_IP, PORT))
            print(f'Enviado quadro com seq={next_seq}')
            total_enviados += 1
            next_seq += 1

        try:
            ack, _ = sock.recvfrom(2)
            ack_num = int.from_bytes(ack, 'big')
            print(f'ACK {ack_num} recebido')
            if ack_num >= base:
                base = ack_num + 1
        except socket.timeout:
            print('[TIMEOUT] Reenviando janela...')
            for i in range(base, next_seq):
                packet = i.to_bytes(2, 'big') + data_blocks[i]
                sock.sendto(packet, (SERVER_IP, PORT))
                print(f'Reenviado quadro com seq={i}')
                total_enviados += 1
                retransmissoes += 1

    # Enviar pacote de fim (sem payload)
    end_packet = next_seq.to_bytes(2, 'big')  # 2 bytes para seq
    sock.sendto(end_packet, (SERVER_IP, PORT))
    print(f'Enviado quadro final seq={next_seq}')
    total_enviados += 1

    try:
        ack, _ = sock.recvfrom(2)
        if int.from_bytes(ack, 'big') == next_seq:
            print('ACK final recebido')
    except socket.timeout:
        retransmissoes += 1
        print('Timeout no quadro final. Encerrando mesmo assim.')

    end_time = time.time()
    tempo_total = end_time - start_time
    sock.close()

    # Relatório final
    print("\n=== MÉTRICAS DE TRANSMISSÃO (GBN) ===")
    print(f"Tamanho do arquivo: {file_size} bytes")
    print(f"Tempo total de transmissão: {tempo_total:.4f} segundos")
    print(f"Total de pacotes enviados (incluindo retransmissões): {total_enviados}")
    print(f"Total de retransmissões: {retransmissoes}")

if __name__ == '__main__':
    main()
