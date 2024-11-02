package JavaExtractor;

import java.io.IOException;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.net.Socket;
import java.net.ServerSocket;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;


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
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter writer = new PrintWriter(socket.getOutputStream(), true)) {
            StringBuilder codeBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                codeBuilder.append(line).append('\n');
                if (line.endsWith("#ENDCODE"))
                    break;
            }
            String code = codeBuilder.toString().replace("#ENDCODE", "");
            ExtractFeaturesTask extractFeaturesTask = new ExtractFeaturesTask(code);
            String response = extractFeaturesTask.call(); // This now properly catches IOException
            writer.println(response);
        } catch (IOException e) {
            e.printStackTrace();
            // Optionally send an error response back to the socket here
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
