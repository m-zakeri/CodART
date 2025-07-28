package JavaExtractor;

import java.io.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.net.Socket;
import java.net.ServerSocket;


public class App {
	public static void main(String[] args) {
		try {
			extractFromSocket(8888);
		} catch (Exception e) {
			e.printStackTrace();
			return;
		}
	}

	 private static void extractFromSocket(int port) {
        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(1);
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Waiting for connections on port " + port);
            while (true) {
                Socket socket = serverSocket.accept();
                executor.submit(() -> handleSocketConnection(socket));
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            executor.shutdown();
        }
    }

    private static void handleSocketConnection(Socket socket) {
        System.out.println("Connected :)");
        try (BufferedInputStream inputStream = new BufferedInputStream(socket.getInputStream());
             PrintWriter writer = new PrintWriter(socket.getOutputStream(), true)) {

            StringBuilder codeBuilder = new StringBuilder();
            byte[] buffer = new byte[1024]; // Buffer to hold the incoming data
            int bytesRead;

            // Continuously read until the connection is closed
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                String chunk = new String(buffer, 0, bytesRead);
                codeBuilder.append(chunk);

                // You can check for a specific condition in the received data
                if (codeBuilder.toString().contains("#ENDCODE")) {
                    break;
                }
            }

            String code = codeBuilder.toString().replace("#ENDCODE", "");
            ExtractFeaturesTask extractFeaturesTask = new ExtractFeaturesTask(code);
            String response = extractFeaturesTask.call(); // Assuming this method is callable
            response = response+"#ENDRESPONSE";
            writer.println(response);

        } catch (IOException e) {
            e.printStackTrace();
            // Optionally send an error response back to the socket here
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
