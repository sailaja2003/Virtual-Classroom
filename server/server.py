
from distutils import errors
import os
import socket
import threading

#IP="127.0.0.1"
IP = "192.168.35.102"
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to Server.".encode(FORMAT))
    while True:
        data = conn.recv(SIZE)
        data=data.decode(FORMAT,errors="ignore")
        data = data.split("@")
        cmd = data[0]
        if cmd == "VIEW":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            st = text
            #text=' '.join(format(ord(x), 'b') for x in st)
            st.encode("ascii")
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w",errors="ignore") as f:
                f.write(st)

            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))

        elif cmd == "DOWNLOAD":
            reqFile = data[1]
            with open(os.path.join("server_data", reqFile),"rb") as file_to_send:
                for d in file_to_send:
                    conn.sendall(d)
            
        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"del {SERVER_DATA_PATH}\{filename}")
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break
        elif cmd == "HELP1":
            data = "OK@"
            data += "VIEW: view all submissions of students\n"
            data += "UPLOAD <path>: post an assignment \n"
            data += "DELETE <filename>: Delete a file \n"
            data += "DOWNLOAD <filename>: View student's assignment\n"
            data += "LOGOUT: Logout of account\n"
            data += "HELP1: Instructions to navigate the application"
            data +="QUIZ1 <ques name>: to upload quiz"
            data +="QUIZ1 <ans name>:to upload answer file"
            conn.send(data.encode(FORMAT))
        elif cmd == "HELP2":
            data = "OK@"
            data += "VIEW: view all assignment\n"
            data += "UPLOAD <path>: submit an assignment format=SRN_NAME in docx.\n"
            data += "DELETE <filename>: Delete an assignment\n"
            data += "DOWNLOAD <filename>: view an assignment\n"
            data += "LOGOUT: LOGOUT\n"
            data += "HELP2: Instructions to navigate the application\n"
            data +="QUIZ2 : to attempt quiz"
            conn.send(data.encode(FORMAT))
        if cmd=="DOWN_CONF":
            send_data = "OK@File downloaded successfully."
            conn.send(send_data.encode(FORMAT))
        elif cmd=="QUIZ1":
            name, text = data[1], data[2]
            st = text
            #text=' '.join(format(ord(x), 'b') for x in st)
            st.encode("ascii")
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w",errors="ignore") as f:
                f.write(st)

            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))
        elif cmd == "QUIZ2":
            name1="ques.txt"
            name2="ans.txt"
            ques=open(os.path.join(SERVER_DATA_PATH,name1),"r")
            ques1=ques.read()
            
            answer=open(os.path.join(SERVER_DATA_PATH,name2),"r")
            ans=answer.read()
            send_data=f"quiz@{ques1}@{ans}"
            conn.send(send_data.encode(FORMAT))
            print("sent")
        elif cmd=="WRONG":
            send_data=f"OK@RE enter"
            conn.send(send_data.encode(FORMAT))

        if cmd=="QUIZ_COMP":
            send_data = "OK@QUIZ COMPLETED."
            conn.send(send_data.encode(FORMAT))
                


    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()