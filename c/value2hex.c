#include "stdio.h"
#include "unistd.h"

struct test
{
    int a;
    float b;
};


typedef struct test tt;


void fuck_you(void)
{
    printf("fuck you!.\n");
}


int main(int argc, char * argv[])
{
    float val = 5678.90;
    int a;
    struct test t1;
    t1.a = 1234;
    t1.b = 5678.9;
    printf("%d, %f\n", t1.a, t1.b);
    printf("This is company mode\n");
    struct timeval tv1;
    FILE f1;
    printf("0x%x\n", (unsigned int)&val);
    printf("hello\n");
    printf("mask is %d\n", 0x20 ^ 0xff);
    printf("function funck_xinlingchao address is 0x%x.\n", (unsigned int)fuck_you);
    if(fuck_you){
        printf("real fuck you!.\n");
    }
    return 0;
}
