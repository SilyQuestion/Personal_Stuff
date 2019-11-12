/* Random N numbers without repetition in a given range [1, SUP]*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define SUP 99
#define N 10

int main(void)
{
    int array[SUP];
    time_t t;

    srand((unsigned)time(&t));
    for(int i = 0; i < SUP; ++i) {
        array[i] = i + 1;
    }

    for(int a_size = SUP; a_size > SUP - N; --a_size) {
        int k = rand() % a_size;
        printf("%2d\n", array[k]);
        array[k] = array[a_size - 1];
    }

    return EXIT_SUCCESS;
}

