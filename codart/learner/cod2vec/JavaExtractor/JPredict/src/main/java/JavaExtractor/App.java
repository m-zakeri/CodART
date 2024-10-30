package JavaExtractor;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

import org.kohsuke.args4j.CmdLineException;

import JavaExtractor.Common.CommandLineValues;
import JavaExtractor.FeaturesEntities.ProgramRelation;

public class App {
	private static CommandLineValues s_CommandLineValues;

	public static void main(String[] args) {
		try {
			s_CommandLineValues = new CommandLineValues(args);
		} catch (CmdLineException e) {
			e.printStackTrace();
			return;
		}

		if (s_CommandLineValues.NoHash) {
			ProgramRelation.setNoHash();
		}

		if (s_CommandLineValues.File != null) {
			ExtractFeaturesTask extractFeaturesTask = new ExtractFeaturesTask(s_CommandLineValues,
					s_CommandLineValues.File.toPath());
			extractFeaturesTask.processFile();
		} else if (s_CommandLineValues.Dir != null) {
			extractDir();
		}
	}

	private static void extractFromSocket(int port) {
        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(s_CommandLineValues.NumThreads);
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Waiting for connections on port " + port);
            while (true) {
                Socket socket = serverSocket.accept();
                // Read code from the socket connection
                BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                StringBuilder codeBuilder = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    codeBuilder.append(line).append(".ENDCODE");
                }

                // Close socket after reading
                socket.close();

                // Create and submit the task
                String code = codeBuilder.toString();
                ExtractFeaturesTask extractFeaturesTask = new ExtractFeaturesTask(s_CommandLineValues, code);
                executor.submit(extractFeaturesTask);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            executor.shutdown();
        }
    }

	private static void extractDir() {
		ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(s_CommandLineValues.NumThreads);
		LinkedList<ExtractFeaturesTask> tasks = new LinkedList<>();
		try {
			Files.walk(Paths.get(s_CommandLineValues.Dir)).filter(Files::isRegularFile)
					.filter(p -> p.toString().toLowerCase().endsWith(".java")).forEach(f -> {
						ExtractFeaturesTask task = new ExtractFeaturesTask(s_CommandLineValues, f);
						tasks.add(task);
					});
		} catch (IOException e) {
			e.printStackTrace();
			return;
		}
		try {
			executor.invokeAll(tasks);
		} catch (InterruptedException e) {
			e.printStackTrace();
		} finally {
			executor.shutdown();
		}
	}
}
