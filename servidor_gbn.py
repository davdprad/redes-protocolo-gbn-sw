import socket

IP = '10.0.0.8'
PORT = 5000
BUFFER_SIZE = 1024

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))

    expected_seq = 0

    with open('output.txt', 'wb') as file:
        print('Servidor aguardando dados...')

        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            if len(data) < 2:
                continue  # Pacote inválido

            seq = int.from_bytes(data[:2], 'big')
            payload = data[2:]

            if not payload:
                print(f'Recebido quadro final seq={seq}.')
                sock.sendto(seq.to_bytes(2, 'big'), addr)
                break

            if seq == expected_seq:
                file.write(payload)
                print(f'Recebido seq={seq}, dados gravados.')
                sock.sendto(seq.to_bytes(2, 'big'), addr)
                expected_seq += 1
            else:
                print(f'Recebido seq={seq}, descartado. Esperado: {expected_seq}')
                ack_num = expected_seq - 1 if expected_seq > 0 else 0
                sock.sendto(ack_num.to_bytes(2, 'big'), addr)

    sock.close()

if __name__ == '__main__':
    main()
