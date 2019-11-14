/*
This was inspired to solve the following problem,
I skipped the test cases part here, since I don't need it anymore.
Input
Standard input begins with an integer T=1,
the number of test cases (this is not a typo, there is always exactly one test case).
Each test case consists of two polynomials.
A polynomial is given by an integer 1≤n≤131071 indicating the degree of the polynomial,
followed by a sequence of integers a0,a1,…,an, where ai is the coefficient of xi in the polynomial.
All coefficients will fit in a signed 32-bit integer.
NB! The input and output files for this problem are quite large,
which means that you have to be a bit careful about I/O efficiency.
Output
For each test case, output the product of the two polynomials,
in the same format as in the input (including the degree). 
All coefficients in the result will fit in a signed 32-bit integer.
*/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <math.h>

#define N 262144    // Max dimension according to the problem
#ifndef M_PI        // Check if M_PI is defined
    #define M_PI 3.14159265358979323846 
#endif

// Complex.h is a bit slow, so we're gonna use our own implementation to save some time
typedef struct {
    double Re;
    double Im;
} cmplx;

// We need this to round the results of the FFT/IFFT
static int32_t my_round(double x)
{
    if(x >= 0) {
        return (int32_t)(x + 0.5);
    }
    else {
        return(int32_t)(x - 0.5);
    }
}

// Helper function to assign a value to a complex number
static cmplx c_assign(double re, double im)
{
    cmplx res;

    res.Re = re;
    res.Im = im;

    return res;
}

// Complex exp
static cmplx c_exp(cmplx z)
{
    double r, x, y;

    x = z.Re;
    y = z.Im;
    r = exp(x);

    return c_assign(r * cos(y), r * sin(y));
}

// Complex product 
static cmplx c_prod(cmplx x, cmplx y)
{
    return c_assign(x.Re * y.Re - x.Im * y.Im, x.Re * y.Im + x.Im * y.Re);
}

// Complex sum
static cmplx c_sum(cmplx x, cmplx y)
{
    return c_assign(x.Re + y.Re, x.Im + y.Im);
}

// Complex subtraction, this does not commute so be careful
static cmplx c_sub(cmplx x, cmplx y)
{
    return c_assign(x.Re - y.Re, x.Im - y.Im);
}

// Round to the next power of 2 
static uint32_t next_2_pow(uint32_t v) 
{
    v--;
    v |= v >> 1;
    v |= v >> 2;
    v |= v >> 4;
    v |= v >> 8;
    v |= v >> 16;
    v++;

    return v;
}


static void check_alloc(const void *p)
{
    if(p == NULL) {
        puts("Error with memory allocation...");    // Mission aborted
        exit(EXIT_FAILURE); 
    }
}

static void in_array(cmplx *v, uint32_t n)
{
    for(uint32_t i = 0; i < n; ++i) {
        double tmp;
        scanf("%lf", &tmp);
        v[i] = c_assign(tmp, 0);
    }
}

// Cooley-Tukey FFT, arg is needed to perform IFFT without additional code
static void _fft
(cmplx *vec, cmplx *out, uint32_t n, uint32_t step, double arg)
{
    if (step < n) {
        _fft(out, vec, n, step * 2, arg);
        _fft(out + step, vec + step, n, step * 2, arg); 
        for (size_t i = 0; i < n; i += step * 2) {
            cmplx z = c_assign(0, arg * i / n);
            cmplx t = c_prod(c_exp(z), out[i + step]);
            vec[i / 2] = c_sum(out[i], t);
            vec[(i + n)/2] = c_sub(out[i], t); 
        }
    }
}

 static void fft(cmplx *vec, uint32_t n, double arg)
{
    cmplx *out = malloc(n * sizeof(cmplx));
    check_alloc(vec);

	for (uint32_t i = 0; i < n; i++) {
        out[i] = vec[i];
    }

	_fft(vec, out, n, 1, arg);

    free(out);
}

static void ifft(cmplx *vec, uint32_t n, double arg)
{
    cmplx *out = malloc(n * sizeof(cmplx));
    uint32_t i;
    
    check_alloc(vec);
    
    for (i = 0; i < n; i++) {
        out[i] = vec[i];
    }

    _fft(vec, out, n, 1, arg);
    // We divide the result of the FFT by 1/n, we do this by multiplying to 1/n
    for(i = 0; i < n; ++i) {
        cmplx tmp = c_assign(1.0/n, 0);
        vec[i] = c_prod(vec[i], tmp);
    }

    free(out);
}

// Since we need to round to the next power of 2, 
// n is the unrounded dimension of the vector,
// while real_degree is the degree of the polynomial
static void show(cmplx *vec, uint32_t n, uint32_t real_degree) 
{   
    printf("Degree of the polynomial multiplication: %" PRIu32 "\n", real_degree);
    for (uint32_t i = 0; i < n; i++) {
        printf("%" PRId32 " ", my_round(vec[i].Re));
    }
    
    puts("");
}

static void point_prod(cmplx *r, cmplx *a, cmplx *b, uint32_t n)
{
    for(uint32_t i = 0; i < n; ++i) {
        r[i] = c_prod(a[i], b[i]);
    }
}

// Global variables but they were good to solve the exercise,
// since I didn't want to deal with too many mallocs and reallocs
static cmplx p1[N];
static cmplx p2[N];
static cmplx res[N];

int main(void)
{
    uint32_t n1, n2, rounded_n_res;
    puts("Enter the degree of the 1st polynomial");
    scanf("%u", &n1);
    n1 += 1;    // If degree is 4 we have 5 coefficients
    puts("Enter the coefficients of 1st polynomial");
    in_array(p1, n1);

    puts("Enter the degree of the 2nd polynomial");
    scanf("%u", &n2);
    n2 += 1;    // If degree is 4 we have 5 coefficients
    puts("Enter the coefficients of 2nd polynomial");
    in_array(p2, n2);

    rounded_n_res = next_2_pow(n1 + n2);
    fft(p1, rounded_n_res, -M_PI);
    fft(p2, rounded_n_res, -M_PI);

    point_prod(res, p1, p2, rounded_n_res);
    ifft(res, rounded_n_res, M_PI);         // We change the sign of the argument
    //  n1 + n2 -2 is the degree of the polynomial
    //  n1 + n2 - 1 is the unrounded dimension of res
    show(res, n1 + n2 - 1, n1 + n2 - 2); 

    return EXIT_SUCCESS;
}
