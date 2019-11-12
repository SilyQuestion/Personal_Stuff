/*
Fibonacci Sequence iterative in linear time.
*/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#define MAX_N 93    // We can't go beyond that! 


int main(void)
{
    uint64_t a[2] = {0, 1};

    printf( "N°[0] = %" PRIu64 "\n"
            "N°[1] = %" PRIu64 "\n",
            a[0], a[1]);

    for (size_t i = 0; i < MAX_N - 1; ++i) {
        uint64_t j = i & 1;
        a[j] += a[j ^ 1];
        printf("N°[%" PRIu64 "] = %" PRIu64 "\n", i + 2, a[j]);
    }

    return EXIT_SUCCESS;
}
