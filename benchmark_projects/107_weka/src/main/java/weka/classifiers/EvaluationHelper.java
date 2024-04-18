package weka.classifiers;

import java.io.Serializable;

public class EvaluationHelper implements Serializable {
    /**
     * Calculate the number of true positives with respect to a particular class.
     * This is defined as
     * <p/>
     *
     * <pre>
     * correctly classified positives
     * </pre>
     *
     * @param classIndex the index of the class to consider as "positive"
     * @return the true positive rate
     */
    public double numTruePositives(int classIndex, double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {

        double correct = 0;
        for (int j = 0; j < thisM_NumClasses; j++) {
            if (j == classIndex) {
                correct += thisM_ConfusionMatrix[classIndex][j];
            }
        }
        return correct;
    }

    /**
     * Calculate the true positive rate with respect to a particular class. This
     * is defined as
     * <p/>
     *
     * <pre>
     * correctly classified positives
     * ------------------------------
     *       total positives
     * </pre>
     *
     * @param classIndex the index of the class to consider as "positive"
     * @return the true positive rate
     */
    public double truePositiveRate(int classIndex, double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {

        double correct = 0, total = 0;
        for (int j = 0; j < thisM_NumClasses; j++) {
            if (j == classIndex) {
                correct += thisM_ConfusionMatrix[classIndex][j];
            }
            total += thisM_ConfusionMatrix[classIndex][j];
        }
        if (total == 0) {
            return 0;
        }
        return correct / total;
    }

    /**
     * Calculates the weighted (by class size) true positive rate.
     *
     * @return the weighted true positive rate.
     */
    public double weightedTruePositiveRate(double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {
        double[] classCounts = new double[thisM_NumClasses];
        double classCountSum = 0;

        for (int i = 0; i < thisM_NumClasses; i++) {
            for (int j = 0; j < thisM_NumClasses; j++) {
                classCounts[i] += thisM_ConfusionMatrix[i][j];
            }
            classCountSum += classCounts[i];
        }

        double truePosTotal = 0;
        for (int i = 0; i < thisM_NumClasses; i++) {
            double temp = truePositiveRate(i, thisM_ConfusionMatrix, thisM_NumClasses);
            truePosTotal += (temp * classCounts[i]);
        }

        return truePosTotal / classCountSum;
    }

    /**
     * Calculate the number of true negatives with respect to a particular class.
     * This is defined as
     * <p/>
     *
     * <pre>
     * correctly classified negatives
     * </pre>
     *
     * @param classIndex the index of the class to consider as "positive"
     * @return the true positive rate
     */
    public double numTrueNegatives(int classIndex, double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {

        double correct = 0;
        for (int i = 0; i < thisM_NumClasses; i++) {
            if (i != classIndex) {
                for (int j = 0; j < thisM_NumClasses; j++) {
                    if (j != classIndex) {
                        correct += thisM_ConfusionMatrix[i][j];
                    }
                }
            }
        }
        return correct;
    }

    /**
     * Calculate the true negative rate with respect to a particular class. This
     * is defined as
     * <p/>
     *
     * <pre>
     * correctly classified negatives
     * ------------------------------
     *       total negatives
     * </pre>
     *
     * @param classIndex the index of the class to consider as "positive"
     * @return the true positive rate
     */
    public double trueNegativeRate(int classIndex, double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {

        double correct = 0, total = 0;
        for (int i = 0; i < thisM_NumClasses; i++) {
            if (i != classIndex) {
                for (int j = 0; j < thisM_NumClasses; j++) {
                    if (j != classIndex) {
                        correct += thisM_ConfusionMatrix[i][j];
                    }
                    total += thisM_ConfusionMatrix[i][j];
                }
            }
        }
        if (total == 0) {
            return 0;
        }
        return correct / total;
    }

    /**
     * Calculates the weighted (by class size) true negative rate.
     *
     * @return the weighted true negative rate.
     */
    public double weightedTrueNegativeRate(double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {
        double[] classCounts = new double[thisM_NumClasses];
        double classCountSum = 0;

        for (int i = 0; i < thisM_NumClasses; i++) {
            for (int j = 0; j < thisM_NumClasses; j++) {
                classCounts[i] += thisM_ConfusionMatrix[i][j];
            }
            classCountSum += classCounts[i];
        }

        double trueNegTotal = 0;
        for (int i = 0; i < thisM_NumClasses; i++) {
            double temp = trueNegativeRate(i, thisM_ConfusionMatrix, thisM_NumClasses);
            trueNegTotal += (temp * classCounts[i]);
        }

        return trueNegTotal / classCountSum;
    }

    /**
     * Calculate number of false positives with respect to a particular class.
     * This is defined as
     * <p/>
     *
     * <pre>
     * incorrectly classified negatives
     * </pre>
     *
     * @param classIndex the index of the class to consider as "positive"
     * @return the false positive rate
     */
    public double numFalsePositives(int classIndex, double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {

        double incorrect = 0;
        for (int i = 0; i < thisM_NumClasses; i++) {
            if (i != classIndex) {
                for (int j = 0; j < thisM_NumClasses; j++) {
                    if (j == classIndex) {
                        incorrect += thisM_ConfusionMatrix[i][j];
                    }
                }
            }
        }
        return incorrect;
    }

    /**
     * Calculate the false positive rate with respect to a particular class. This
     * is defined as
     * <p/>
     *
     * <pre>
     * incorrectly classified negatives
     * --------------------------------
     *        total negatives
     * </pre>
     *
     * @param classIndex the index of the class to consider as "positive"
     * @return the false positive rate
     */
    public double falsePositiveRate(int classIndex, double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {

        double incorrect = 0, total = 0;
        for (int i = 0; i < thisM_NumClasses; i++) {
            if (i != classIndex) {
                for (int j = 0; j < thisM_NumClasses; j++) {
                    if (j == classIndex) {
                        incorrect += thisM_ConfusionMatrix[i][j];
                    }
                    total += thisM_ConfusionMatrix[i][j];
                }
            }
        }
        if (total == 0) {
            return 0;
        }
        return incorrect / total;
    }

    /**
     * Calculates the weighted (by class size) false positive rate.
     *
     * @return the weighted false positive rate.
     */
    public double weightedFalsePositiveRate(double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {
        double[] classCounts = new double[thisM_NumClasses];
        double classCountSum = 0;

        for (int i = 0; i < thisM_NumClasses; i++) {
            for (int j = 0; j < thisM_NumClasses; j++) {
                classCounts[i] += thisM_ConfusionMatrix[i][j];
            }
            classCountSum += classCounts[i];
        }

        double falsePosTotal = 0;
        for (int i = 0; i < thisM_NumClasses; i++) {
            double temp = falsePositiveRate(i, thisM_ConfusionMatrix, thisM_NumClasses);
            falsePosTotal += (temp * classCounts[i]);
        }

        return falsePosTotal / classCountSum;
    }

    /**
     * Calculate number of false negatives with respect to a particular class.
     * This is defined as
     * <p/>
     *
     * <pre>
     * incorrectly classified positives
     * </pre>
     *
     * @param classIndex the index of the class to consider as "positive"
     * @return the false positive rate
     */
    public double numFalseNegatives(int classIndex, double[][] thisM_ConfusionMatrix, int thisM_NumClasses) {

        double incorrect = 0;
        for (int i = 0; i < thisM_NumClasses; i++) {
            if (i == classIndex) {
                for (int j = 0; j < thisM_NumClasses; j++) {
                    if (j != classIndex) {
                        incorrect += thisM_ConfusionMatrix[i][j];
                    }
                }
            }
        }
        return incorrect;
    }
}