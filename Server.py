import socket
import llamaAPI
class Server:
    #server script must be ran first
    #setting up a tcp connection 
    #connection to another server is only possible by knowing its IP
    #reserving a port
    def __init__(self):
        self.port = 5230
        self.host = "127.0.0.1"
        self.backlog = 5
        self.buffer_size = 8192
        self.api = llamaAPI() #instantiating llamaAPI
    #making a socket  AF_INET accepts IPv4,ipv6 or local
    def connect_to_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #allows for the reuseablility of the port
            s.bind((self.host,self.port))
            s.listen(self.backlog) #now enbaled to listen for incomming connections
            conn, addr = s.accept()
            #dealing with first user prompt
            data = conn.recv(self.buffer_size)
            decoded = data.decode()
            self.sent_prompt = self.api.get_response(decoded)
            conn.sendall(self.sent_prompt.encode()) #sending first reply back data to the client
            while True:
                print(f"[+] Connected to {addr}")
                data = conn.recv(self.buffer_size) # recived the user prompt from the client side
                decoded = data.decode() # decoded raw data to string
                if decoded.strip().lower() == "exit":
                    break;
                self.sent_prompt = self.api.get_response(decoded)
                conn.sendall(self.sent_prompt.encode()) #sending further replies back data to the client
            conn.close()
                
                

if __name__ == "__main__":
    Server().connect_to_client()