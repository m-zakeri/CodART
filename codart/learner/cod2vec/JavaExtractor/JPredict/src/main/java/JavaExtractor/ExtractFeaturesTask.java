package JavaExtractor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;

import org.apache.commons.lang3.StringUtils;
import java.io.IOException;

import com.github.javaparser.ParseException;
import JavaExtractor.Common.Common;
import JavaExtractor.FeaturesEntities.ProgramFeatures;

public class ExtractFeaturesTask implements Callable<String> {
    String code; // Changed from Path to String

    public ExtractFeaturesTask(String code) {
        this.code = code;
    }

    @Override
    public String call() throws IOException{
        System.out.println("Extracting code...");
        try {
            String result = processFile(); // processFile may throw exceptions
            System.out.println("Done with code extraction.");
            return result; // Return the result from processFile
        } catch (Exception e) {
            e.printStackTrace();
            return "Error during code extraction: " + e.getMessage();
        }
    }

     public String processFile() {
        ArrayList<ProgramFeatures> features;
        try {
            features = extractSingleFile();
        } catch (ParseException e) {
            e.printStackTrace();
            return "Error in processing file"; // Return an error message
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
         if (features == null || features.isEmpty()) {
            return "No features found"; // Return message if no features are found
        }
        return featuresToString(features); // Return features as a string
    }

    public ArrayList<ProgramFeatures> extractSingleFile() throws ParseException, IOException {
        // Directly use the 'code' string without reading from a file
        FeatureExtractor featureExtractor = new FeatureExtractor();
        ArrayList<ProgramFeatures> features = featureExtractor.extractFeatures(code);
        return features;
    }

    public String featuresToString(ArrayList<ProgramFeatures> features) {
        if (features == null || features.isEmpty()) {
            return Common.EmptyString;
        }

        List<String> methodsOutputs = new ArrayList<>();

        for (ProgramFeatures singleMethodfeatures : features) {
            StringBuilder builder = new StringBuilder();

            String toPrint = Common.EmptyString;
            toPrint = singleMethodfeatures.toString();
            toPrint = toPrint.replace(" ", "\n\t");
            builder.append(toPrint);

            methodsOutputs.add(builder.toString());
        }
        return StringUtils.join(methodsOutputs, "\n");
    }
}