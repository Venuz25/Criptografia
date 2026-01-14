#include <iostream>
#include <cmath>
#include <tuple>
#include <cstdlib>
#include <ctime>

using namespace std;
#define noPruebas 5

tuple<int,int,int> extendedEuclid(int a, int b){
    int a0 = a, b0 = b;
    int t0 = 0, t = 1;
    int s0 = 1, s = 0;
    int q = floor(a0/b0);
    int r = a0 - (q*b0);
    
    while(r > 0){
        int temp = t0 - (q*t);
        t0 = t;
        t = temp;

        temp = s0 - (q*s);
        s0 = s;
        s = temp;

        a0 = b0;
        b0 = r;
        
        q = floor(a0/b0);
        r = a0 - (q*b0);
    }
    r = b0;

    return make_tuple(r,s,t);
}

/* int main() {
    srand(time(0));

    cout << "Algoritmo Extendido de Euclides - Pruebas con numeros aleatorios\n" << endl;

    for(int i = 1; i <= noPruebas; i++) {
        int a = rand() % 100 + 1;
        int b = rand() % 100 + 1;

        int r, s, t;
        tie(r, s, t) = extendedEuclid(a, b);

        cout << "Prueba " << i << ": a = " << a << ", b = " << b << endl;
        cout << "r = " << r << ", s = " << s << ", t = " << t << endl;
        cout << "gcd(" << a << ", " << b << ") = " << r << endl;
        cout << r << " = (" << s << ")*" << a << " + (" << t << ")*" << b << endl;
        cout << "--------------------------------------" << endl;
    }
    return 0;

} */

int main() {
    int a, b;
    
    cout << "Algoritmo Extendido de Euclides" << endl;
    cout << "Ingresa a: ";
    cin >> a;
    cout << "Ingresa b: ";
    cin >> b;

    int r, s, t;
    tie(r, s, t) = extendedEuclid(a, b);

    cout << "\nr = " << r << ", s = " << s << ", t = " << t << endl;
    cout << "gcd(" << a << ", " << b << ") = " << r << endl;
    cout << r << " = (" << s << ")" << a << " + (" << t << ")" << b << endl;

    return 0;
}

