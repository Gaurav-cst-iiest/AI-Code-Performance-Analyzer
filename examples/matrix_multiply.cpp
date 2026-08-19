#include <iostream>
using namespace std;

// Matrix multiplication — a triple nested loop, so time is O(n^3).
// It uses 2D arrays, so space is O(n^2). A strong "bottleneck" demo.

void multiplyMatrix(int a[10][10], int b[10][10], int n)
{
    int result[10][10];

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            result[i][j] = 0;
            for (int k = 0; k < n; k++)
            {
                result[i][j] = result[i][j] + a[i][k] * b[k][j];
            }
        }
    }
}

int main()
{
    return 0;
}
