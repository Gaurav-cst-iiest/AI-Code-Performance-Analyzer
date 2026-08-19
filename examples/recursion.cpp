#include <iostream>
using namespace std;

// Recursive functions. The analyzer flags recursion for manual review,
// because a naive recursion like fibonacci can be exponential.

int factorial(int n)
{
    if (n <= 1)
    {
        return 1;
    }
    return n * factorial(n - 1);
}

int fibonacci(int n)
{
    if (n <= 1)
    {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main()
{
    return 0;
}
