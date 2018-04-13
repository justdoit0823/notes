
%module example

%inline %{
extern double sin(double x);
extern int strcmp(const char *, const char *);
%}
#define STATUS 50
#define VERSION "1.1"
