import socket
import pymysql

# MySQL 데이터베이스에서 도메인에 해당하는 IP 주소 조회
def query_domain(domain):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='0000',
                           database='dns_db')
    try:
        with conn.cursor() as cursor:
            sql = "SELECT ip FROM domains WHERE domain=%s"
            cursor.execute(sql, (domain,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    finally:
        conn.close()

# 상위 DNS 서버에 문의
def query_upper_dns(domain):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(domain.encode('utf-8'), ('localhost', 5357))  # 포트 번호를 5357로 변경
    
    response, _ = client_socket.recvfrom(1024)
    client_socket.close()
    return response.decode('utf-8')

# Local DNS 서버 설정
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 5356)) 
    
    print("Local DNS 서버가 5356 포트에서 실행 중입니다.")
    
    while True:
        data, addr = server_socket.recvfrom(1024)
        domain = data.decode('utf-8')
        print(f"클라이언트로부터 도메인 요청 받음: {domain}")
        
        ip_address = query_domain(domain)
        if ip_address:
            response = f"{domain}의 IP 주소는 {ip_address}입니다."
        else:
            print(f"{domain}의 IP 주소를 로컬에서 찾을 수 없음. 상위 DNS 서버에 문의합니다.")
            response = query_upper_dns(domain)
        
        server_socket.sendto(response.encode('utf-8'), addr)

if __name__ == "__main__":
    start_server()
