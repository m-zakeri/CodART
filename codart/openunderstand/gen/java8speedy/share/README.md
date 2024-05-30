sudo g++ -O3 -Wall -shared -std=c++11 -fPIC -I /home/y/Desktop/iust/OpenUnderstand/openunderstand/gen/java8speedy/antlr4-runtime/include/  -L /home/y/Desktop/iust/OpenUnderstand/openunderstand/gen/java8speedy/antlr4-runtime/lib/ -Wl,--no-undefined $(python3 -m pybind11 --includes) sa_javalabeled_cpp_parser.cpp -o sa_javalabeled_cpp_parser_4.so

