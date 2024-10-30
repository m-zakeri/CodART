package JavaExtractor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;

import org.apache.commons.lang3.StringUtils;

import com.github.javaparser.ParseException;

import JavaExtractor.Common.CommandLineValues;
import JavaExtractor.Common.Common;
import JavaExtractor.FeaturesEntities.ProgramFeatures;

public class ExtractFeaturesTask implements Callable<Void> {
    CommandLineValues m_CommandLineValues;
    String code; // Changed from Path to String

    // Change constructor to accept String
    public ExtractFeaturesTask(CommandLineValues commandLineValues, String code) {
        m_CommandLineValues = commandLineValues;
        this.code = code;
    }

    @Override
    public Void call() throws Exception {
        // System.err.println("Extracting code...");
        processFile();
        // System.err.println("Done with code extraction.");
        return null;
    }

    public void processFile() {
        ArrayList<ProgramFeatures> features;
        try {
            features = extractSingleFile();
        } catch (ParseException e) {
            e.printStackTrace();
            return;
        }
        if (features == null) {
            return;
        }

        String toPrint = featuresToString(features);
        if (toPrint.length() > 0) {
            System.out.println(toPrint);
        }
    }

    public ArrayList<ProgramFeatures> extractSingleFile() throws ParseException {
        // Directly use the 'code' string without reading from a file
        FeatureExtractor featureExtractor = new FeatureExtractor(m_CommandLineValues);
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
            if (m_CommandLineValues.PrettyPrint) {
                toPrint = toPrint.replace(" ", "\n\t");
            }
            builder.append(toPrint);

            methodsOutputs.add(builder.toString());
        }
        return StringUtils.join(methodsOutputs, "\n");
    }
}