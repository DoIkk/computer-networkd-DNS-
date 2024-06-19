import socket

def query_dns_server(domain):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(domain.encode('utf-8'), ('localhost', 5356))  
    
    response, _ = client_socket.recvfrom(1024)
    print("서버 응답:", response.decode('utf-8'))
    client_socket.close()

if __name__ == "__main__":
    domain = input("조회할 도메인 이름을 입력하세요: ")
    query_dns_server(domain)
