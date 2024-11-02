import socket


def communicate_with_java_server(host, port, code):
    try:
        # Connect to the server
        with socket.create_connection((host, port)) as sock:
            print(f"Connected to server at {host}:{port}")

            # Send the code line-by-line
            for line in code.splitlines():
                sock.sendall((line + "\n").encode("utf-8"))
            # Send a newline to signal end of data if needed
            sock.sendall(b"\n")

            # Receive the response from the server
            response = []
            with sock.makefile('r') as sock_file:
                for line in sock_file:
                    response.append(line.strip())

            return "\n".join(response)
    except Exception as e:
        print("Error communicating with server:", e)
        return None


if __name__ == "__main__":
    # Host and port must match the Java server
    host = "localhost"
    port = 8888
    # Replace with the code you want to send
    # code_to_send = """public class Example {
    #                     public void method() {
    #                         System.out.println("Hello from Python client!");
    #                     }
    #                  }#ENDCODE"""
    code_to_send = "#ENDCODE"

    # Send the code and print the response from the server
    response = communicate_with_java_server(host, port, code_to_send)
    if response:
        print("Response from Java server:\n", response)