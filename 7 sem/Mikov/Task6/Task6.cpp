#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <ctime>
#include <clocale>

using namespace std;

const double PI = 3.14159265358979323846;

enum class State {
    Healthy,
    Infected,
    Zombie,
    Recovered
};

struct Agent {
    double x, y;     
    double dir;       
    double alpha;    
    double rh;        

    State state;

    int moveTimeLeft;   
    int incubTimeLeft;  
};

const int FIELD_SIZE = 100;      
const double VH = 1.0;           
const double RUN_MULT = 1.25;     
const double INF_SPEED = 0.9;     
const double ZOMBIE_SPEED = 0.85; 

const double RH_DEFAULT = 10.0;  
const double ALPHA_MIN_DEG = 90.0;
const double ALPHA_MAX_DEG = 150.0;

const int TMOVE_MIN = 5;
const int TMOVE_MAX = 20;

const int TINC_MIN = 20;
const int TINC_MAX = 50;

const int T_INIT = 50;          

const int T_MAX = 5000;

const double P_ZOMBIE_TO_RECOVERED = 0.01;  
const double P_RECOVERED_TO_ZOMBIE = 0.25;  

double degToRad(double a) { return a * PI / 180.0; }

double normAngle(double a) {
    while (a > PI) a -= 2 * PI;
    while (a < -PI) a += 2 * PI;
    return a;
}

struct RNG {
    mt19937 gen;
    uniform_real_distribution<double> uni01;

    RNG() : gen((unsigned)time(nullptr)), uni01(0.0, 1.0) {}

    double rand01() { return uni01(gen); }

    double randDouble(double a, double b) {
        uniform_real_distribution<double> d(a, b);
        return d(gen);
    }

    int randInt(int a, int b) { 
        uniform_int_distribution<int> d(a, b);
        return d(gen);
    }
};

bool inSector(const Agent& observer, const Agent& target,
    double angle, double radius) {
    double dx = target.x - observer.x;
    double dy = target.y - observer.y;
    double dist2 = dx * dx + dy * dy;
    if (dist2 > radius * radius) return false;

    double angToTarget = atan2(dy, dx);
    double diff = normAngle(angToTarget - observer.dir);
    return fabs(diff) <= angle / 2.0;
}

double sideOf(const Agent& observer, const Agent& target) {
    double vx = cos(observer.dir);
    double vy = sin(observer.dir);
    double dx = target.x - observer.x;
    double dy = target.y - observer.y;
    return vx * dy - vy * dx;
}

void bounceFromWalls(Agent& a) {
    bool bounced = false;
    if (a.x < 0.0) {
        a.x = -a.x;
        a.dir = PI - a.dir;
        bounced = true;
    }
    if (a.x > FIELD_SIZE) {
        a.x = 2 * FIELD_SIZE - a.x;
        a.dir = PI - a.dir;
        bounced = true;
    }
    if (a.y < 0.0) {
        a.y = -a.y;
        a.dir = -a.dir;
        bounced = true;
    }
    if (a.y > FIELD_SIZE) {
        a.y = 2 * FIELD_SIZE - a.y;
        a.dir = -a.dir;
        bounced = true;
    }
    if (bounced) a.dir = normAngle(a.dir);
}

void initAgents(vector<Agent>& agents, int n, RNG& rng) {
    agents.clear();
    agents.resize(n);

    for (int i = 0; i < n; ++i) {
        Agent& a = agents[i];
        a.x = rng.randDouble(0.0, FIELD_SIZE);
        a.y = rng.randDouble(0.0, FIELD_SIZE);
        a.dir = rng.randDouble(-PI, PI);
        a.alpha = degToRad(rng.randDouble(ALPHA_MIN_DEG, ALPHA_MAX_DEG));
        a.rh = RH_DEFAULT;
        a.state = State::Healthy;
        a.moveTimeLeft = rng.randInt(TMOVE_MIN, TMOVE_MAX);
        a.incubTimeLeft = 0;
    }
}

int step(vector<Agent>& agents, int t, RNG& rng) {
    int n = (int)agents.size();

    vector<double> speed(n, VH);

    for (int i = 0; i < n; ++i) {
        Agent& a = agents[i];
        if (a.state != State::Healthy) continue;

        bool hasLeftZombie = false;
        bool hasRightZombie = false;

        for (int j = 0; j < n; ++j) {
            if (i == j) continue;
            Agent& b = agents[j];
            if (b.state != State::Zombie) continue;

            if (inSector(a, b, a.alpha, a.rh)) {
                double s = sideOf(a, b);
                if (s > 0) hasLeftZombie = true;
                else if (s < 0) hasRightZombie = true;
            }
        }

        if (hasLeftZombie || hasRightZombie) {
            if (hasLeftZombie && !hasRightZombie) {
                a.dir -= a.alpha / 2.0;
            }
            else if (!hasLeftZombie && hasRightZombie) {
                a.dir += a.alpha / 2.0;
            }
            else {
                a.dir += PI;
            }
            a.dir = normAngle(a.dir);
            speed[i] = VH * RUN_MULT;
        }
        else {
            speed[i] = VH;
        }
    }

    for (int i = 0; i < n; ++i) {
        Agent& a = agents[i];
        if (a.state == State::Infected) {
            speed[i] = VH * INF_SPEED;
        }
    }

    for (int i = 0; i < n; ++i) {
        Agent& a = agents[i];
        if (a.state == State::Recovered) {
            speed[i] = VH;
        }
    }

    for (int i = 0; i < n; ++i) {
        Agent& a = agents[i];
        if (a.state != State::Zombie) continue;

        double zombieAngle = a.alpha * 0.75;
        double zombieRadius = a.rh * 1.1;

        double bestDist2 = 1e100;
        bool hasTarget = false;
        double bestAngle = a.dir;

        for (int j = 0; j < n; ++j) {
            if (i == j) continue;
            Agent& b = agents[j];
            if (b.state != State::Healthy) continue;

            if (!inSector(a, b, zombieAngle, zombieRadius)) continue;

            double dx = b.x - a.x;
            double dy = b.y - a.y;
            double d2 = dx * dx + dy * dy;
            if (d2 < bestDist2) {
                bestDist2 = d2;
                bestAngle = atan2(dy, dx);
                hasTarget = true;
            }
        }

        if (hasTarget) {
            a.dir = normAngle(bestAngle);
        }
        speed[i] = VH * ZOMBIE_SPEED;
    }

    for (int i = 0; i < n; ++i) {
        Agent& a = agents[i];

        if (a.moveTimeLeft <= 0) {
            a.dir = rng.randDouble(-PI, PI);
            a.moveTimeLeft = rng.randInt(TMOVE_MIN, TMOVE_MAX);
        }

        double v = speed[i];
        double dx = v * cos(a.dir);
        double dy = v * sin(a.dir);
        a.x += dx;
        a.y += dy;

        bounceFromWalls(a);

        a.moveTimeLeft--;

        if (a.state == State::Infected && a.incubTimeLeft > 0) {
            a.incubTimeLeft--;
        }
    }

    for (int i = 0; i < n; ++i) {
        Agent& z = agents[i];
        if (z.state != State::Zombie) continue;

        double zombieAngle = z.alpha * 0.75;
        double zombieRadius = z.rh * 1.1;

        double actionAngle = zombieAngle * 0.93;   
        double actionRadius = zombieRadius * 0.93; 

        for (int j = 0; j < n; ++j) {
            if (i == j) continue;
            Agent& b = agents[j];

            if (!inSector(z, b, actionAngle, actionRadius)) continue;

            if (b.state == State::Healthy) {
                b.state = State::Infected;
                b.incubTimeLeft = rng.randInt(TINC_MIN, TINC_MAX);
            }
            else if (b.state == State::Recovered) {
                if (rng.rand01() < P_RECOVERED_TO_ZOMBIE) {
                    b.state = State::Zombie;
                    b.incubTimeLeft = 0;
                }
            }
        }
    }

    for (int i = 0; i < n; ++i) {
        Agent& a = agents[i];
        if (a.state == State::Infected && a.incubTimeLeft <= 0) {
            a.state = State::Zombie;
        }
    }

    for (int i = 0; i < n; ++i) {
        Agent& a = agents[i];
        if (a.state == State::Zombie) {
            if (rng.rand01() < P_ZOMBIE_TO_RECOVERED) {
                a.state = State::Recovered;
            }
        }
    }

    int healthyCount = 0;
    for (int i = 0; i < n; ++i) {
        if (agents[i].state == State::Healthy) healthyCount++;
    }
    return healthyCount;
}

int runExperiment(int n, int m, RNG& rng) {
    vector<Agent> agents;
    initAgents(agents, n, rng);

    int t = 0;

    for (; t < T_INIT; ++t) {
        step(agents, t, rng);
    }

    if (m > n) m = n;
    vector<int> idx(n);
    for (int i = 0; i < n; ++i) idx[i] = i;

    for (int i = 0; i < n; ++i) {
        int j = rng.randInt(i, n - 1);
        swap(idx[i], idx[j]);
    }

    for (int i = 0; i < m; ++i) {
        Agent& a = agents[idx[i]];
        a.state = State::Infected;
        a.incubTimeLeft = rng.randInt(TINC_MIN, TINC_MAX);
    }

    int healthyCount = 0;
    for (; t < T_MAX; ++t) {
        healthyCount = step(agents, t, rng);
        if (healthyCount == 0) break;
    }

    return t;
}

int main() {
    setlocale(LC_ALL, "Russian");

    RNG rng;

    int configs;
    cout << "Введите количество конфигураций (наборов n и m): ";
    if (!(cin >> configs)) return 0;

    const int EXPERIMENTS = 1000; 

    for (int c = 0; c < configs; ++c) {
        int n, m;
        cout << "\nКонфигурация " << (c + 1) << ":\n";
        cout << "  n (число агентов): ";
        cin >> n;
        cout << "  m (число первично заражённых): ";
        cin >> m;

        long long sumT = 0;
        for (int k = 0; k < EXPERIMENTS; ++k) {
            int t = runExperiment(n, m, rng);
            sumT += t;
        }
        double avgT = (double)sumT / EXPERIMENTS;

        cout << "Среднее время обращения всей популяции в зомби (n="
            << n << ", m=" << m << ") = " << avgT << " шагов" << endl;
    }

    return 0;
}
