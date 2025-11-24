#include <iostream>
using namespace std;

extern "C" char* setlocale(int, const char*);

double dabs(double x) { return (x < 0.0) ? -x : x; }

struct Params {
    double a0, a1, a2;
    double k;         
    double dt;         
    double tStop;      // время моделирования
    double tauMax;     // верхняя граница для τ
};

double goal(double /*t*/) { return 1.0; }

bool simulate_is_stable(double tau, const Params& p) {
    int N = (int)(p.tStop / p.dt + 0.5);
    if (N < 3) N = 3;

    int delaySteps = (int)(tau / p.dt + 0.5);
    double* x = new double[N + 1];
    for (int i = 0; i <= N; ++i) x[i] = 0.0;

    const double dt = p.dt;
    const double c2 = p.a2 / (dt * dt);
    const double c1 = p.a1 / dt;
    const double den = c2 + c1 + p.a0;

    double xm1 = 0.0;
    double xm2 = 0.0;
    const double BLOWUP = 1e6;

    for (int i = 0; i <= N; ++i) {
        int j = i - delaySteps;
        double x_delay = (j >= 0) ? x[j] : 0.0;

        double u = p.k * (goal(i * dt) - x_delay);

        double xi = (u - ((-2.0 * c2 - c1) * xm1) - (c2 * xm2)) / den;

        if (xi != xi || dabs(xi) > BLOWUP) { // nan/overflow -> неустойчиво
            delete[] x;
            return false;
        }

        xm2 = xm1;
        xm1 = xi;
        x[i] = xi;
    }

    // проверим, что к концу держимся около цели и без явной раскачки
    int tail = N / 5; if (tail < 10) tail = 10; if (tail > N) tail = N;
    double mean = 0.0;
    for (int i = N - tail + 1; i <= N; ++i) mean += x[i];
    mean /= (tail > 0 ? tail : 1);

    double var = 0.0;
    for (int i = N - tail + 1; i <= N; ++i) {
        double d = x[i] - mean;
        var += d * d;
    }
    if (tail > 0) var /= tail;

    bool ok = (dabs(x[N] - 1.0) < 0.05) && (var < 1e-3);
    delete[] x;
    return ok;
}

double find_tau_critical(const Params& p) {
    if (!simulate_is_stable(0.0, p)) return 0.0;
    if (simulate_is_stable(p.tauMax, p)) return p.tauMax;

    double L = 0.0, R = p.tauMax;
    for (int it = 0; it < 45; ++it) {
        double M = 0.5 * (L + R);
        if (simulate_is_stable(M, p)) L = M; else R = M;
    }
    return L;
}

int main() {
    setlocale(0, "rus");

    Params p;
    p.a0 = 1.0; p.a1 = 2.5; p.a2 = 0.3;
    p.k = 1.0;  p.dt = 0.01; p.tStop = 50.0; p.tauMax = 10.0;

    cout << "Уравнение: a2*x'' + a1*x' + a0*x = u,  u = k*(1 - x(t - tau))\n\n";
    cout << "Введите a0 a1 a2 k: ";
    cin >> p.a0 >> p.a1 >> p.a2 >> p.k;
    cout << "Введите dt, T_stop, tau_max: ";
    cin >> p.dt >> p.tStop >> p.tauMax;

    double tauCrit = find_tau_critical(p);

    cout << "\nКритическое tau ~= " << tauCrit << "\n";
    cout << "Проверка: устойчиво при tau=0     -> "
        << (simulate_is_stable(0.0, p) ? "да" : "нет") << "\n";
    cout << "           устойчиво при tau=tauMax -> "
        << (simulate_is_stable(p.tauMax, p) ? "да" : "нет") << "\n";

    return 0;
}
