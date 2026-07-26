#include <iostream>
using namespace std;

// Depth = 0
void test1()
{
    int a = 10;
}

// Depth = 1
void test2()
{
    if(a)
    {
        cout << "Hello";
    }
}

// Depth = 2
void test3()
{
    if(a)
    {
        while(b)
        {
            cout << "Hi";
        }
    }
}

// Depth = 3
void test4()
{
    if(a)
    {
        while(b)
        {
            for(int i=0;i<10;i++)
            {
                cout << i;
            }
        }
    }
}

// Depth = 4
void test5()
{
    if(a)
    {
        while(b)
        {
            for(int i=0;i<10;i++)
            {
                if(c)
                {
                    cout << i;
                }
            }
        }
    }
}

// Sequential blocks (Maximum depth = 2)
void test6()
{
    if(a)
    {
        while(b)
        {

        }

        for(int i=0;i<10;i++)
        {

        }
    }
}

// Separate blocks (Maximum depth = 1)
void test7()
{
    if(a)
    {

    }

    while(b)
    {

    }

    for(int i=0;i<10;i++)
    {

    }
}

// Brace on same line (Maximum depth = 3)
void test8()
{
    if(a) {
        while(b) {
            for(int i=0;i<10;i++) {
                cout<<i;
            }
        }
    }
}

// Mixed formatting (Maximum depth = 3)
void test9()
{
    if(a)

    {
        while(b)

        {
            if(c)

            {
                cout<<"Nested";
            }
        }
    }
}

// Anonymous scope (Maximum depth should remain 1)
void test10()
{
    if(a)
    {
        {
            int x = 10;
            int y = 20;
        }

        cout << "Done";
    }
}

int main()
{
    return 0;
}