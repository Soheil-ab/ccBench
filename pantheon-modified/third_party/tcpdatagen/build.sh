mkdir -p dataset
g++ -pthread src/sage_dataset.cc src/flow.cc -o sage_dataset
g++ src/client.c -o client
mv client sage_dataset bin/

