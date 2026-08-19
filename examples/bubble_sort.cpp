#include <iostream>
using namespace std;

// Bubble sort — a classic O(n^2) algorithm with a nested loop.
// Space is O(n) because of the array.

void bubbleSort(int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main()
{
    int data[5];
    return 0;
}
