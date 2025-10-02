#!/usr/bin/env python3
"""
TCP Client for CSNETWK Socket Programming Lab
Author: John Q. Smith
Description: Client that connects to server, sends client name and user-input integer,
             receives server response, and displays the results.
"""

import socket
import sys
import json

def get_user_input():
    """Get integer input from user (1-100)"""
    while True:
        try:
            user_input = input("Enter an integer between 1 and 100: ")
            number = int(user_input)
            return number  # Return the number even if out of range (server will handle shutdown)
        except ValueError: # Python Built in Exception (you will learn this in Java)
            print("Please enter a valid integer.")

def main():
    # Client configuration
    HOST = 'localhost'  # Server address
    PORT = 6769 # Server port
    CLIENT_NAME = "Client of Justine Corpuz and Ryan Malapitan"
    
    # Get integer input from user
    client_number = get_user_input()
    print(f"You entered: {client_number}")
    
    # Create TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        print(f"Connecting to server at {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Connected to server!")
        
        # Prepare message to send as JSON file
        message = {
            'name': CLIENT_NAME,
            'number': client_number
        } # this data structure is a python dictionary
        
        # Send message to server
        message_json = json.dumps(message) # convert python dictionary into json file for sending to server
        client_socket.send(message_json.encode('utf-8'))
        print("Message sent to server")
        
        # Wait for server response
        print("Waiting for server response...")
        response_data = client_socket.recv(1024).decode('utf-8')
        
        if not response_data:
            print("No response received from server")
            return
        
        # Parse server response
        try:
            server_response = json.loads(response_data)
            server_name = server_response['name']
            server_number = server_response['number']
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing server response: {e}")
            return
        
        # Display results
        print("\n" + "="*50)
        print("COMMUNICATION RESULTS:")
        print("="*50)
        print(f"Client name: {CLIENT_NAME}")
        print(f"Server name: {server_name}")
        print(f"Client integer: {client_number}")
        print(f"Server integer: {server_number}")
        
        # Calculate and display sum
        sum_result = client_number + server_number
        print(f"Sum: {client_number} + {server_number} = {sum_result}")
        print("="*50)
        
        print("\nCommunication completed successfully!")
        
    except ConnectionRefusedError:
        print("Error: Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"Client error: {e}")
    
    finally:
        # Close client socket
        client_socket.close()
        print("Client socket closed")

if __name__ == "__main__":
    main() # starts at main function