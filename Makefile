default: CacheAccess

CPP = /usr/local/opt/llvm/bin/clang++
CPPFLAGS= -I/usr/local/opt/llvm/include -fopenmp
LDFLAGS="-L/usr/local/opt/llvm/lib"

CacheAccess: CacheAccess.cpp
	$(CPP) $(CPPFLAGS) CacheAccess.cpp -o CacheAccess $(LDFLAGS)
