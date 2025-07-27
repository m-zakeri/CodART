public class MatrixDependencyAnalyzer {
    public static void main(String[] args) {
        int[][] matrix = new int[5][5];
        int[][] result = new int[5][5];

        // Initialize matrix
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                matrix[i][j] = i * j;
            }
        }

        // Calculate result matrix with dependencies
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                if (i > 0) {
                result[i][j] += matrix[i - 1][j];
                result[i][j] += matrix[i - 1][j];
                    if(true){

                    result[i][j] += matrix[i - 1][j];
                    result[i][j] += matrix[i - 1][j];
                    result[i][j] += matrix[i - 1][j];
                    print(result)
                    }

                    result[i][j] += matrix[i - 1][j];
                }
                if (j > 0) {
                    result[i][j] += matrix[i][j - 1];
                }
                if (i > 0 && j > 0) {
                    result[i][j] += matrix[i - 1][j - 1];
                }
            }
        }

        // Print results
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                System.out.print(result[i][j] + " ");
            }
            System.out.println();
        }
    }
}
