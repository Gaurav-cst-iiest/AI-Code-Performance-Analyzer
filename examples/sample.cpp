#include <iostream>
using namespace std;

int add(int a, int b)
{
    return a + b;
}

void display() {
    cout << "Hello" << endl;
}

int factorial(int n)
{
    if (n <= 1)
        return 1;
    return n * factorial(n - 1);
}

void longFunction()
{
    int a = 0;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    a++;
    cout << a << endl;
}

int main()
{
    cout << add(5, 6) << endl;
    display();
    cout << factorial(5) << endl;
    longFunction();
    return 0;
}