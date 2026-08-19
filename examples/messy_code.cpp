#include <iostream>
using namespace std;

// This file is intentionally messy: magic numbers, duplicate lines,
// unused variables, and a deeply nested loop. It should get a LOW score
// and produce several optimization suggestions — great for a demo.

int calculate(int n)
{
    int unusedVar = 50;
    int total = 0;

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            for (int k = 0; k < n; k++)
            {
                total = total + i * 7;
                total = total + i * 7;
                total = total * 3;
            }
        }
    }

    int discount = total * 15;
    int discount2 = total * 15;

    return total;
}

int main()
{
    int x = calculate(100);
    cout << x;
    return 0;
}
