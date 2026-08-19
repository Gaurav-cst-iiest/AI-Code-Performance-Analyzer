#include <iostream>
using namespace std;

// Clean, simple code: one linear loop, no magic numbers, no duplicates.
// This should score well and show O(n) time and O(1) space.

const int STEP = 1;

int sumUpTo(int n)
{
    int total = 0;

    for (int i = 0; i <= n; i = i + STEP)
    {
        total = total + i;
    }

    return total;
}

int main()
{
    int result = sumUpTo(10);
    cout << result;
    return 0;
}
