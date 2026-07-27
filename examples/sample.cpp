#include<iostream>
using namespace std;

const int MAX = 100;

int square(int x)
{
    return x * x;
}

int cube(int x)
{
    int result = x * x * x;
    return result;
}

void helper()
{
    cout << "Helper Function";
}

void recursive(int n)
{
    if(n > 0)
    {
        recursive(n - 1);
    }
}

void calculate(int a, int b)
{
    int sum = a + b;
    int unused = 50;

    if(sum > 10)
    {
        while(sum < 100)
        {
            for(int i = 0; i < 5; i++)
            {
                if(i == 2)
                {
                    helper();
                }
            }

            sum = sum + 20;
        }
    }

    square(sum);
    cube(sum);
}

void testMagic()
{
    int age = 18;
    int marks = 95;
    int arr[200];

    if(age > 60)
    {
        age = 25;
    }

    float pi = 3.14;
    double e = 2.718;

    int size = 100;

    return;
}

int main()
{
    int value = 10;
    int value2 = value;

    calculate(value, value2);

    recursive(5);

    helper();

    return 0;
}