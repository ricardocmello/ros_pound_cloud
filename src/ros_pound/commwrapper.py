#!/usr/bin/env python

import sys
import yaml
import os.path
import socket
import subprocess

if(len(sys.argv) != 2):
    if(int(sys.argv[1])==0 or int(sys.argv[1])==1):
        pass
    else:
        print("Usage : {} node-id ".format(sys.argv[0]))
        print("e.g. {} 0 - for machine with local IP (robot)".format(sys.argv[0]))
        print("or   {} 1 - for machine with public IP (remote)".format(sys.argv[0]))
        sys.exit(-1)

class CommWrapper():
    def __init__(self, node_id):        
        self.node_id = int(node_id)
        
        self.read_file() # Read original config file
            
        self.open_sock() # Open corresponding socket
       
        self.start_comm("From robot rx") # Stablish communication among nodes 
        
        self.start_comm("From robot tx") # Stablish communication among nodes 

        if node_id == 1:  
            self.write_file() # Re-write config file used by remote node
        
        self.close_sock() # Close sockets so they can be re-openned by ros-pound
        
        self.run_pound() # Call ros-pound
        


    def read_file(self):
        print("In read_file()")
        parent_path = os.path.dirname(__file__)
        config_path = parent_path[:-9] + "libwrapper/config/config.yaml"
        stream = open(config_path, 'r')
        print("Path: {}".format(stream))
        self.file_content = yaml.load(stream)
        print("Content: {}".format(self.file_content))
        print("myIP: {}".format(self.file_content['node_ip'][self.node_id]))
        print("myPort_rx: {}".format(self.file_content['node_port_rx'][self.node_id]))
        print("myPort_tx: {}".format(self.file_content['node_port_tx'][self.node_id]))
        self.myIP = self.file_content['node_ip'][self.node_id]
        self.myPort_rx = self.file_content['node_port_rx'][self.node_id]
        self.myPort_tx = self.file_content['node_port_tx'][self.node_id]
        if self.node_id == 0:
            self.remoteIP = self.file_content['node_ip'][1]
            self.remotePort_rx = self.file_content['node_port_rx'][1]
            self.remotePort_tx = self.file_content['node_port_tx'][1]
        stream.close()
           
        return True

    def open_sock(self):
        print("In open_sock()")
        self.sock_rx = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM)
        print("Binding socket_rx on IP: 0.0.0.0 and Port: {}".format(self.myPort_rx))
        self.sock_rx.bind(("0.0.0.0", self.myPort_rx))

        self.sock_tx = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM)
        print("Binding socket_tx on IP: 0.0.0.0 and Port: {}".format(self.myPort_tx))
        self.sock_tx.bind(("0.0.0.0", self.myPort_tx))

        print("Out open_sock()")
        return True

    def start_comm(self, condition):
        message = "Start"
        print(message)
        if self.node_id == 0:
            self.sock_rx.settimeout(1)
            self.sock_tx.settimeout(1)
            for i in range(10):
                # Send data to stablish communication
                if condition == "From robot rx": # then we should work on remote tx
                    self.sock_rx.sendto(message, (self.remoteIP,self.remotePort_tx))
                elif condition == "From robot tx": # then we should work on remote rx
                    self.sock_tx.sendto(message, (self.remoteIP,self.remotePort_rx))
                
                try: 
                    # Wait for response
                    if condition == "From robot rx":
                        data, server = self.sock_rx.recvfrom(50)
                    elif condition == "From robot tx":
                        data, server = self.sock_tx.recvfrom(50)
                    print("[robot_wrapper] DEBUG: {} == {}".format(message,data))

                    if data == message:
                        print("[robot_wrapper] Response from server: {}".format(server[0]))
                        break
                
                except socket.timeout:
                    print("[robot_wrapper] Response timeout - Attemp #{}".format(i))
               
                print("[robot_wrapper] -----------------------------------")
                print("[robot_wrapper] It seems that something is wrong...")
                print("[robot_wrapper] -----------------------------------")
        
        else:
            # Receive data to stablish communication
            print("[cloud_wrapper] Waiting for arriving packets")
            if condition == "From robot rx": # then we should work on remote tx
                data, addr = self.sock_tx.recvfrom(50)
            elif condition == "From robot tx": # then we should work on remote rx
                data, addr = self.sock_rx.recvfrom(50)
            
            print("[cloud_wrapper] DEBUG: {} == {}".format(message,data))
            self.remoteIP = str(addr[0])
            
            if condition == "From robot rx": 
                self.remotePort_rx = int(addr[1])
            elif condition == "From robot tx":
                self.remotePort_tx = int(addr[1])
            # Send response
            for i in range(5):
                print("[cloud_wrapper] Send response to robot")
                if condition == "From robot rx":  # then we should work on remote tx
                    self.sock_tx.sendto(data, (self.remoteIP,self.remotePort_rx))
                elif condition == "From robot tx": # then we should work on remote rx
                    self.sock_rx.sendto(data, (self.remoteIP,self.remotePort_tx))
        
        return True


    def write_file(self):
        self.file_content['node_ip'][0] = self.remoteIP
        self.file_content['node_ip'][1] = "0.0.0.0"

        self.file_content['node_port_rx'][0] = self.remotePort_rx
        self.file_content['node_port_tx'][0] = self.remotePort_tx

        print(self.file_content)
        parent_path = os.path.dirname(__file__)
        config_path = parent_path.replace('ros_pound','') + "libwrapper/config/config.yaml"
        with open(config_path,'w') as stream: 
            print(self.file_content)
            yaml.dump(self.file_content, stream)
        return True

    def run_pound(self):
        print("Start ros_pound")
        subprocess.call(["rosrun", "ros_pound", "ros-pound", "--node-id", str(self.node_id)])
        return True

    def close_sock(self):
        self.sock_rx.close()
        self.sock_tx.close()


if __name__ == '__main__':
    print("node_id")
    node_id = int(sys.argv[1])        
    print(node_id)
    if node_id not in [0, 1]:
        print("Node-id should be 0 or 1")
        sys.exit(-1)
    wrapper = CommWrapper(node_id)
