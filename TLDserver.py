import socket
import pymysql

# 데이터베이스에서 도메인에 해당하는 IP 주소 조회
def query_upper_domain(domain):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='0000',
                           database='upper_dns_db')
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

# 상위 DNS 서버 설정
def start_upper_dns_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 5357))  
    
    print("상위 DNS 서버가 5357 포트에서 실행 중입니다.")
    
    while True:
        data, addr = server_socket.recvfrom(1024)
        domain = data.decode('utf-8')
        print(f"Local DNS 서버로부터 도메인 요청 받음: {domain}")
        
        ip_address = query_upper_domain(domain)
        if ip_address:
            response = f"{domain}의 IP 주소는 {ip_address}입니다."
        else:
            response = f"{domain}의 IP 주소를 찾을 수 없습니다."
        
        server_socket.sendto(response.encode('utf-8'), addr)

if __name__ == "__main__":
    start_upper_dns_server()
