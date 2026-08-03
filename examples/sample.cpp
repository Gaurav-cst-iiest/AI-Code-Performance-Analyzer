#include<iostream>
using namespace std;

int main()
{
    int a = 10;
    int b = 20;

    a = a + b;
    b++;

    a = a + b;
    b++;

    if(a>b)
    {
        cout<<a;
    }

    if(a>b)
    {
        cout<<b;
    }

    return 0;
}