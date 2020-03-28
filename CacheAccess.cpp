#include <iostream>
#include <random>
#include <fstream>
#include <algorithm>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <random>
#include <chrono>
#include "/usr/local/Cellar/libomp/9.0.1/include/omp.h"

// Parameters
int MAX_SIZE = 1024 * 1024 * 64;
int MIN_SIZE = 64;

void** generateMem(std::size_t size) {
   std::size_t len = size / sizeof(void*);
   void** memory = new void*[len];

   // Generate a ordered number array
   size_t* indices = new std::size_t[len];
   for (std::size_t i = 0; i < len; ++i) {
      indices[i] = i;
   }

   std::default_random_engine generator;

   // Shuffle values of this array to be randomized
   for (std::size_t i = 0; i < len-1; ++i) {
      // Generate a random number based on uniform distribution
      std::uniform_int_distribution<int> distribution(0,len - i - 1);
      std::size_t j = i + distribution(generator);

      // Swap value
      if (i != j) {
        std::swap(indices[i], indices[j]);
      }
   }

   // fill memory with randomized pointer references
   for (std::size_t i = 1; i < len; ++i) {
      memory[indices[i-1]] = (void*) &memory[indices[i]];
   }
   memory[indices[len-1]] = (void*) &memory[indices[0]];

   delete[] indices;
   return memory;
}

volatile void* chase_pointers_global;

// Memory Access
double memAccess(void** mem, size_t size, bool rw) {
  // chase the pointers count times
  void** ptr = (void**) mem;
  size_t count = size;
  void** next;
  void** a;

  auto start = std::chrono::high_resolution_clock::now();
  if (rw) {
    while (count > 0) {
      next = (void**) *ptr;
      a = (void**) *ptr;
      a = (void**) ((uintptr_t) a & 0x7fffffffffffffff);  /* where your data is known to be less than 30 bits */
      *ptr = a;
      ptr = next;
      count--;
    }
  } else {
    while (count > 0) {
      ptr = (void**) *ptr;
      count--;
    }
  }
  auto finish = std::chrono::high_resolution_clock::now();

  double latency = std::chrono::duration_cast<std::chrono::nanoseconds>(finish-start).count();
  chase_pointers_global = *ptr;
  return latency;
}

std::string getFileName(int numThread, bool rw) {
  if (rw) {
    return "t" + std::to_string(numThread) + "_rw.csv";
  } else {
    return "t" + std::to_string(numThread) + "_r.csv";
  }
}

int main(int argc, char *argv[]) {
  int NUM_THREAD = 1;
  int RW = false;

  for(int i=1; i<argc; i++) {
    std::string arg = argv[i];
    if ((arg == "-t")) {
      i +=1;
      NUM_THREAD = atoi(argv[i]);
    } else if (arg == "-rw") {
      RW = true;
    } else {
      exit(0);
    }
  }

  std::ofstream output;
  std::string fileName = getFileName(NUM_THREAD, RW);
  std::cout << "Thread: " << NUM_THREAD << " rw: " << RW << "\n";
  output.open (fileName);
  for (std::size_t memsize = MIN_SIZE; memsize <= MAX_SIZE; memsize *= 2) {
    double latency_sum = 0;
    std::size_t count = std::max(memsize * 16, (std::size_t(1)) << 30);
    #pragma omp parallel num_threads(NUM_THREAD)
    {
      void** memory = generateMem(memsize);
      double latency = memAccess(memory, count, RW);
      #pragma omp atomic
        latency_sum = latency_sum + latency;
      delete[] memory;
    }

    double averageLatency = (latency_sum / NUM_THREAD) / count;
    std::cout << "Size: " << memsize << ", Latency: " <<  averageLatency << "\n";
    output << memsize << "," <<  averageLatency << "\n";
  }
  output.close();

  return 0;
}
