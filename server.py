#!/usr/bin/env python3
"""
TCP Server for CSNETWK Socket Programming Lab
Author: John Q. Smith
Description: Server that accepts client connections, receives client name and integer,
             generates its own integer, and sends response back to client.
"""

import socket
import sys
import json

def main():
    # Server configuration
    HOST = 'localhost'  # Server will bind to localhost
    PORT = 6769       # Port to listen on
    SERVER_NAME = "Server of Justine Corpuz and Ryan Malapitan"
    SERVER_NUMBER = 99  # Server's integer (it's fine naman daw if constant)
    
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Allow socket reuse
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind socket to address and port
        server_socket.bind((HOST, PORT))
        
        # Listen for incoming connections (max 1 for now)
        server_socket.listen(1)
        
        print(f"Server '{SERVER_NAME}' is listening on {HOST}:{PORT}")
        print("Waiting for client connections...")
        print("Note: Send an integer outside 1-100 range to shutdown server")
        
        while True:
            # Accept incoming connection
            client_socket, client_address = server_socket.accept()
            print(f"\nConnection established with {client_address}")
            
            try:
                # Receive message from client
                received_data = client_socket.recv(1024).decode('utf-8') # memory aligned to 1024 bytes (modify the value to powers of 2 lng)
                # decodes the data into unicode (don't worry about unicode you will learn it in CSARCH2, it's just ASCII but better)

                if not received_data:
                    # Premature client disconnection, (didn't sent data to server)
                    print("No data received from client")
                    client_socket.close()
                    continue
                
                # Parse received JSON message
                try:
                    client_message = json.loads(received_data)
                    client_name = client_message['name'] # takes the 'name' part of the json file
                    client_number = client_message['number'] # takes the 'number' part of the json file
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error parsing client message: {e}")
                    client_socket.close()
                    continue
                
                print(f"Received from client:")
                print(f"  Client name: {client_name}")
                print(f"  Client number: {client_number}")
                
                # Check if client number is in valid range (1-100)
                if client_number < 1 or client_number > 100:
                    print(f"Client number {client_number} is out of range (1-100)")
                    print("Shutting down server...")
                    client_socket.close()
                    break
                
                # Display server information and calculations
                print(f"Server name: {SERVER_NAME}")
                print(f"Client number: {client_number}")
                print(f"Server number: {SERVER_NUMBER}")
                sum_result = client_number + SERVER_NUMBER
                print(f"Sum: {client_number} + {SERVER_NUMBER} = {sum_result}")
                
                # Prepare response message
                response = {
                    'name': SERVER_NAME,
                    'number': SERVER_NUMBER
                }
                
                # Send response to client
                response_json = json.dumps(response)
                client_socket.send(response_json.encode('utf-8'))
                print("Response sent to client")
                
            except Exception as e:
                print(f"Error handling client: {e}")
            
            finally:
                # Close client connection
                client_socket.close()
                print("Client connection closed")
    
    except KeyboardInterrupt:
        print("\nServer interrupted by user")
    except Exception as e:
        print(f"Server error: {e}")
    
    finally:
        # Close server socket
        server_socket.close()
        print("Server socket closed")

if __name__ == "__main__":
    main()