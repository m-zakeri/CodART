import socket


class Extractor:
    def __init__(self, config, jar_path, max_path_length, max_path_width):
        self.config = config
        self.max_path_length = max_path_length
        self.max_path_width = max_path_width
        self.jar_path = jar_path
        self.host = "localhost"  # Server host
        self.port = 8888  # Server port, must match your Java server settings

    def extract_paths(self, java_code):
        try:
            java_code = java_code+"#ENDCODE"
            with socket.create_connection((self.host, self.port)) as sock:
                print("Sending Java code...")
                for line in java_code.splitlines():
                    sock.sendall((line + "\n").encode("utf-8"))
                sock.sendall(b"\n")

                # Receive the response from the server
                response = []
                with sock.makefile('r') as sock_file:
                    for line in sock_file:
                        response.append(line.strip())
                        if "#ENDRESPONSE" in line:
                            break


                response = "\n".join(response)
                response = response.replace("#ENDRESPONSE", "")
                if not response:
                    raise ValueError("No response from server")

                # Process the response as before
                output_lines = response.splitlines()
                hash_to_string_dict = {}
                result = []
                if response == "No features found":
                    return result, ""
                for line in output_lines:
                    parts = line.rstrip().split(" ")
                    method_name = parts[0]
                    current_result_line_parts = [method_name]
                    contexts = parts[1:]  # Assuming the rest are contexts
                    for context in contexts[: int(self.config['COD2VEC']['MAX_CONTEXTS'])]:
                        context_parts = context.split(",")
                        context_word1 = context_parts[0]
                        context_path = context_parts[1]
                        context_word2 = context_parts[2]
                        hashed_path = str(self.java_string_hashcode(context_path))
                        hash_to_string_dict[hashed_path] = context_path
                        current_result_line_parts += [
                            "%s,%s,%s" % (context_word1, hashed_path, context_word2)
                        ]
                    space_padding = " " * (int(self.config['COD2VEC']['MAX_CONTEXTS']) - len(contexts))
                    result_line = " ".join(current_result_line_parts) + space_padding
                    result.append(result_line)
                return result, hash_to_string_dict

        except (socket.error, ConnectionRefusedError) as e:
            print(f"Socket error: {e}")
            raise ValueError("Failed to connect to server or send data.")

    @staticmethod
    def java_string_hashcode(s):
        """
        Imitating Java's String#hashCode, because the model is trained on hashed paths but we wish to
        Present the path attention on un-hashed paths.
        """
        h = 0
        for c in s:
            h = (31 * h + ord(c)) & 0xFFFFFFFF
        return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
