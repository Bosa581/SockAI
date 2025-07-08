import socket
import os
from llamaAPI import llamaAPI
class Client:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5230
        self.buffer_size = 8192 #8kb is the limit for amount of data to be sent, will become an issue as this becomes multi conversational
        self.user_input = input("Enter a prompt: ")
        self.api = llamaAPI() #instantiating llamaAPI

    #user input for simulation gpt's  conversation
    def start_client(self):
        #establishing a connection to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host,self.port))
                #initial user's prompt
                #calls the get_response method of the llamaAPI class
                s.sendall(self.user_input.encode())  #only way to send message since its an array of the assitances conversation
                reply = s.recv(self.buffer_size)
                print(reply.decode())
                while True:
                    print("*********************************************************************************************************")
                    seconduser_input = input("Enter more prompts: ")
                    if seconduser_input.strip() == "exit" or not seconduser_input.strip():
                       break
                    s.sendall(seconduser_input.encode())
                    reply2 = s.recv(self.buffer_size)
                    print(reply2.decode())
                    self.api.getPrevMessage(self.user_input,reply.decode()) #passes the user's past as an input to the 
                    self.user_input = seconduser_input
                
if __name__ == "__main__":
    print("[Debug] Starting client...")
    client = Client()
    client.start_client()
