#include <iostream>
using namespace std;


// 1. Logarithmic while loop
void logWhile(int n)
{
    int i = 1;

    while(i < n)
    {
        i *= 2;
    }
}


// 2. Logarithmic for loop
void logFor(int n)
{
    for(int i = 1; i < n; i *= 2)
    {
        cout << i;
    }
}


// 3. Division logarithmic loop
void divideLoop(int n)
{
    while(n > 1)
    {
        n /= 2;
    }
}


// 4. Bit shift logarithmic loop
void shiftLoop(int n)
{
    while(n > 1)
    {
        n >>= 1;
    }
}


// 5. Normal linear for loop
void linearFor(int n)
{
    for(int i = 0; i < n; i++)
    {
        cout << i;
    }
}


// 6. Normal linear while loop
void linearWhile(int n)
{
    int i = 0;

    while(i < n)
    {
        i++;
    }
}


// 7. No loop
void noLoop(int n)
{
    int x = n * 2;
    cout << x;
}


// 8. Multiplication outside loop
void multiplicationOutside(int n)
{
    int x = n;
    x *= 2;

    cout << x;
}


// 9. Nested loop
void nested(int n)
{
    for(int i = 0; i < n; i++)
    {
        for(int j = 1; j < n; j *= 2)
        {
            cout << j;
        }
    }
}


// 10. Multiple operations
void multiple(int n)
{
    for(int i = 1; i < n; i *= 2)
    {
        int x = 10;

        while(x < n)
        {
            x *= 2;
        }
    }
}


int main()
{
    return 0;
}