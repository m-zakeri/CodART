public class DataDependencyExample {
public int deleteParent(int nParent, Instances _Instances) {
int iParent = 0;
while ((m_nParents[iParent] != nParent) && (iParent < m_nNrOfParents)) {
iParent++;
}
int iParent2 = -1;
if (iParent < m_nNrOfParents) {
iParent2 = iParent;
}
if (iParent < m_nNrOfParents) {
while (iParent < m_nNrOfParents - 1) {
m_nParents[iParent] = m_nParents[iParent + 1];
iParent++;
}
m_nNrOfParents--;
m_nCardinalityOfParents /= _Instances.attribute(nParent).numValues(); }
return iParent2;
}
}
//
// //
// public class DataDependencyExample {
// Void SortAndNormalize(int ArrayIn[], int X){
//  int n = ArrayIn.length;
//  for (int i = 0; i < n-1; i++){
//  for (int j = 0; j < n-i-1; j++){
//  if (ArrayIn [j] > ArrayIn [j+1]){
//  int temp = ArrayIn [j];
//  ArrayIn [j] = ArrayIn [j+1];
//  ArrayIn [j+1] = temp;
// }
// }
// }
//  System.out.println(ArrayIn);
//  int k = n-1;
//  while (k >= 0){
//  int difference = ArrayIn [k] - ArrayIn [k-1];
//  if(difference <= X){
//  ArrayIn [k-1] = ArrayIn [k];
//  ArrayIn [k] = ArrayIn [k] + X;
// }
// else {
//  ArrayIn [k-1] = ArrayIn [k] - X;
//  ArrayIn [k] = ArrayIn [k] + X / 2;
// }
//  k--;
// }
//  System.out.println(ArrayIn);
// }
// }
// public class DataDependencyExample {
//     int Method() {
//         int x = 10;
//         int y = 11;
//
//         if (y > 0) {
//             x++;
//             y++;
//
//             if (true) {
//                 for (int i = 0; i < 10; i++) {
//                     y++;
//                     x++;
//                 }
//                 x++;
//                 x++;
//                 y++;
//                 for (int j = 0; j < 10; j++) {
//                     y++;
//                     x++;
//                     System.out.println(x);
//                 }
//             }
//         }
//
//     }
// }


//
// public class DataDependencyExample {
//     public static void main() {
//         int x = 0;
//         int y = 0;
//         int w,s,z;
//
//         if (x > 10) {
//             x--;
//             s++;
//
//
//         } else {
//             y++;
//             s++;
//         }
//         s++;
//         y++;
//         w=x+y;
//         s++;
//
//         z=w;
//
//         return z+y;
//     }
// }
//
// public class SimpleIfElseTest {
//     public static void math() {
//         int x = 0;
//         int y = 0;
//         int z;
//
//         if (x > 10) {
//             x = x + 1;
//         } else {
//             y = y + 1;
//         }
//
//
//         System.out.println("Final value of x: " + x);
//         System.out.println("Final value of y: " + y);
//     }
// }
// public class SimpleProgram {
//
//
//     int Method() {
//         int x = 10;
//         int y = 11;
//
//         if (y > 0) {
//             x++;
//             y++;
//
//             if (true) {
//                 for (int i = 0; i < 10; i++) {
//                     y++;
//                     x++;
//                 }
//                 x++;
//                 x++;
//                 y++;
//                 for (int j = 0; j < 10; j++) {
//                     y++;
//                     x++;
//                     System.out.println(x);
//                 }
//             }
//         }
//
//     }
//
//     public static void main(String[] args) {
//         int number = 10;
//
//         if (number > 5) {
//             System.out.println("Value inside if block: " + number);
//         }
//
//         for (int i = 0; i < 1; i++) {
//             number += 5;
//             System.out.println("Value inside loop: " + number);
//         }
// //         return number;
//     }
// }
# def main(file_path):
#     output_list = cfg_main(file_path)
#
#     cfg_analyzer = CFGAnalyzer(output_list)
#     paths = cfg_analyzer.paths
#
#     testability_calculator = TestabilityCalculator(paths, output_list)
#     method_testability = testability_calculator.method_testability
#     average_testability = testability_calculator.calculate_average_testability()
#     weighted_average_testability = testability_calculator.calculate_weighted_average_testability()
#
#     print("\nAll Paths:")
#     for method_paths in paths:
#         for p in method_paths:
#             print("Path:", p)
#
#     for method_name, node_testability in method_testability.items():
#         print(f"\nMethod: {method_name}")
#         for node, testability in node_testability.items():
#             print(f"Node {node} testability: {testability:.4f}")
#         print(f"Average Testability for {method_name}: {average_testability[method_name]:.4f}")
#
#     print(f"\nWeighted Average Testability for the entire file: {weighted_average_testability:.4f}")

import os
from cfg_generator.src.cfg_from_stdin import main as cfg_main