#include <iostream>
using namespace std;

int square(int x)
{
    return x * x;
}

int cube(int x)
{
    return x * x * x;
}

void helper()
{
    cout << "Helper Function\n";
}

int recursive(int n)
{
    if(n <= 1)
    {
        return 1;
    }
    return n * recursive(n - 1);
}

void calculate(int n)
{
    if(n > 0)
    {
        for(int i = 0; i < n; i++)
        {
            while(i < 3)
            {
                if(i == 1)
                {
                    cout << i << endl;
                }
                i++;
            }
        }
    }
    else if(n == 0)
    {
        cout << "Zero\n";
    }
    else
    {
        switch(n)
        {
            case -1:
                cout << "-1\n";
                break;

            case -2:
                cout << "-2\n";
                break;

            default:
                cout << "Other\n";
        }
    }
}

void nested()
{
    if(true)
    {
        for(int i = 0; i < 5; i++)
        {
            while(i < 2)
            {
                if(i == 1)
                {
                    switch(i)
                    {
                        case 1:
                            cout << "One\n";
                            break;
                    }
                }
                i++;
            }
        }
    }
}

void noDecision()
{
    int a = 10;
    int b = 20;
    int c = a + b;
    cout << c << endl;
}

int main()
{
    helper();
    square(5);
    cube(4);
    recursive(5);

    calculate(5);
    calculate(0);
    calculate(-1);

    nested();
    noDecision();

    return 0;
}