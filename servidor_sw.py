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
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                seq = data[0]
                payload = data[1:]

                if not payload:
                    print(f'Recebido seq={seq}, finalizando.')
                    sock.sendto(seq.to_bytes(1, 'big'), addr)
                    break

                if seq == expected_seq:
                    file.write(payload)
                    print(f'Recebido seq={seq}, dados gravados.')
                    sock.sendto(seq.to_bytes(1, 'big'), addr)
                    expected_seq = 1 - expected_seq
                else:
                    print(f'Recebido seq={seq}, descartado. Esperado: {expected_seq}')
                    sock.sendto((1 - expected_seq).to_bytes(1, 'big'), addr)
            except Exception as e:
                print(f'Erro: {e}')
                break

    sock.close()

if __name__ == '__main__':
    main()
