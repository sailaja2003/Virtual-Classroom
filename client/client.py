import socket
import os
#IP="127.0.0.1"
IP = "192.168.35.102"
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
CLIENT_DATA = "client_data"
attempt=0
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print()
    print("------------------------------------------------------------WELCOME TO THE VIRTUAL CLASSROOM-------------------------------------------------")
    
    print("")
    opt = input("CHOOSE 1 IF YOU ARE A TEACHER AND 2 FOR A STUDENT: ")
    if opt=="1":
        print()
        print("For commands type HELP1")
        name=input("Enter your name:")
        passwd=input("Enter the password:")
        if passwd=="3214":
            while True:
                data = client.recv(SIZE).decode(FORMAT)
                cmd, msg = data.split("@")

                if cmd == "DISCONNECTED":
                    print(f"[SERVER]: {msg}")
                    break
                elif cmd == "OK":
                    print(f"{msg}")
                data = input("> ")
                data = data.split(" ")
                cmd = data[0]
                
                if cmd == "HELP1":
                    client.send(cmd.encode(FORMAT))
                elif cmd == "LOGOUT":
                    client.send(cmd.encode(FORMAT))
                    break
                elif cmd == "VIEW":
                    client.send(cmd.encode(FORMAT))
                elif cmd == "DELETE":
                    client.send(f"{cmd}@{data[1]}".encode(FORMAT))
                elif cmd == "UPLOAD":
                    path = data[1]

                    with open(os.path.join("client_data",path), "r",errors="ignore") as f:#ignoreeeee
                        text = f.read()

                    filename = path.split("/")[-1]
                    send_data = f"{cmd}@{filename}@{text}"
                    client.send(send_data.encode(FORMAT))

                elif cmd == "DOWNLOAD":
                    path = data[1]
                    filename = path.split("/")[-1]
                    send_data = f"{cmd}@{filename}"
                    client.send(send_data.encode(FORMAT))
                    with open(os.path.join("client_data", filename), 'wb') as file_to_write:
                        d = client.recv(1024)
                        file_to_write.write(d)
                        file_to_write.close()
                    send_data="DOWN_CONF"
                    client.send(send_data.encode(FORMAT))   
                elif cmd == "QUIZ1":
                    path = data[1]

                    with open(os.path.join("client_data",path), "r",errors="ignore") as f:#ignoreeeee
                        text = f.read()

                    filename = path.split("/")[-1]
                    send_data = f"{cmd}@{filename}@{text}"
                    client.send(send_data.encode(FORMAT))
                elif cmd=="RESULT":
                    send_data = f"DOWNLOAD@res.txt"
                    client.send(send_data.encode(FORMAT))
                    with open(os.path.join("client_data","res.txt"), 'wb') as file_to_write:            
                        d = client.recv(1024)
            
                        file_to_write.write(d)
                        file_to_write.close()
                    send_data="DOWN_CONF"
                    client.send(send_data.encode(FORMAT)) 
                else :
                    send_data="WRONG"
                    client.send(send_data.encode(FORMAT)) 
                    print("Enter right command") 
        else :
            print("Please enter the correct password.")  
            client.close()      
    elif(opt=="2"):
        print()
        print("For commands type HELP2")
        name=input("Enter your name: ")
        while True:
            data = client.recv(SIZE).decode(FORMAT)
            cmd, msg = data.split("@")
            if cmd == "DISCONNECTED":
                print(f"[SERVER]: {msg}")
                break
            elif cmd == "OK":
                print(f"{msg}")
            data = input("> ")
            data = data.split(" ")
            cmd = data[0]
            if cmd == "HELP2":
                client.send(cmd.encode(FORMAT))
            elif cmd == "LOGOUT":
                client.send(cmd.encode(FORMAT))
                break
            elif cmd == "VIEW":
                client.send(cmd.encode(FORMAT))
            elif cmd == "DELETE":
                client.send(f"{cmd}@{data[1]}".encode(FORMAT))
            elif cmd == "UPLOAD":
                path = data[1]

                with open(os.path.join("client_data",path), "r",errors="ignore") as f:#ignoreeeee
                    text = f.read()

                filename = path.split("/")[-1]
                send_data = f"{cmd}@{filename}@{text}"
                client.send(send_data.encode(FORMAT))

            elif cmd == "DOWNLOAD":
                path = data[1]
                filename = path.split("/")[-1]
                send_data = f"{cmd}@{filename}"
                client.send(send_data.encode(FORMAT))
                with open(os.path.join("client_data", filename), 'wb') as file_to_write:
                    d = client.recv(1024)
                    #print(d)
                    file_to_write.write(d)
                    file_to_write.close()
                send_data="DOWN_CONF"
                client.send(send_data.encode(FORMAT))   
            elif cmd == "QUIZ2":
                global attempt
                attempt=attempt+1
                if attempt>=2:
                    print("You have already submitted your response")
                    print()
                else:
                    client.send(cmd.encode(FORMAT))
                    data=client.recv(1024)
                    data=data.decode(FORMAT)
                    data=data.split("@")
                    ques=data[1]
                    ans=data[2]
                    ques=ques.split(",")
                    ans=ans.split(",")
                    marks=0
                    for i in range(len(ques)):
                        print(ques[i])
                        ns=input("Enter the answer:")
                        if(ns==ans[i]):
                            print("Correct answer")
                            marks=marks+1
                        else:
                            print("Incorrect answer")
                    send_data="QUIZ_COMP"
                    client.send(send_data.encode(FORMAT))   
                    res = open("res.txt","a")
                    res.write(f"{name}:{marks},")
                    res.close()
                    with open("res.txt", "r",errors="ignore") as f:
                        text = f.read()
                    send_data = f"UPLOAD@res.txt@{text}"
                    client.send(send_data.encode(FORMAT))
            else :
                send_data="WRONG"
                client.send(send_data.encode(FORMAT)) 
                print("Enter right command") 

                
    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    #attempt=0
    main()