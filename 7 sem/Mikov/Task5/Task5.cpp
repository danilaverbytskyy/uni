#include <iostream>
using namespace std;

const int MAXM = 200;  
const int MAXE = 2000;  
const int MAXN = 100;   
const int MAXF = 2000;  
const int MAXEVENTS = 100000;
const double INF = 1e100;

int M, E;
double workMod[MAXM + 1];
int indegInit[MAXM + 1];

int succHead[MAXM + 1], succTo[MAXE + 5], succNext[MAXE + 5], succCnt = 0;
int predHead[MAXM + 1], predTo[MAXE + 5], predNext[MAXE + 5], predCnt = 0;

void addEdgeApp(int u, int v) {
    ++succCnt; succTo[succCnt] = v; succNext[succCnt] = succHead[u]; succHead[u] = succCnt;
    ++predCnt; predTo[predCnt] = u; predNext[predCnt] = predHead[v]; predHead[v] = predCnt;
    indegInit[v]++;
}

int N, F;
double speedAg[MAXN + 1];
double distAg[MAXN + 1][MAXN + 1]; 

double agentFree[MAXN + 1];     
int assignedAgent[MAXM + 1];    
double startTimeM[MAXM + 1], finishTimeM[MAXM + 1];
int remainingPred[MAXM + 1], doneMod[MAXM + 1];

int qArr[MAXM + 5], qL, qR;

int readyHeap[MAXM + 5], readySz = 0;
bool readyIn[MAXM + 1];

bool readyLess(int a, int b) { 
    return workMod[a] < workMod[b];
}
void readySwap(int i, int j) {
    int t = readyHeap[i]; readyHeap[i] = readyHeap[j]; readyHeap[j] = t;
}
void readyPush(int x) {
    if (readyIn[x]) return;
    readyIn[x] = true;
    readyHeap[++readySz] = x;
    int i = readySz;
    while (i > 1) {
        int p = i >> 1;
        if (!readyLess(readyHeap[p], readyHeap[i])) break;
        readySwap(p, i); i = p;
    }
}
int readyTop() { return readySz ? readyHeap[1] : -1; }
void readyPop() {
    if (!readySz) return;
    readyIn[readyHeap[1]] = false;
    readyHeap[1] = readyHeap[readySz--];
    int i = 1;
    while (true) {
        int l = i << 1, r = l + 1, best = i;
        if (l <= readySz && readyLess(readyHeap[best], readyHeap[l])) best = l;
        if (r <= readySz && readyLess(readyHeap[best], readyHeap[r])) best = r;
        if (best == i) break;
        readySwap(i, best); i = best;
    }
}

struct Event { double t; int mod; int ag; };
Event evHeap[MAXEVENTS + 5]; int evSz = 0;
bool evLess(int i, int j) { return evHeap[i].t < evHeap[j].t; } 
void evSwap(int i, int j) { Event t = evHeap[i]; evHeap[i] = evHeap[j]; evHeap[j] = t; }
void evPush(double t, int m, int a) {
    if (evSz + 1 > MAXEVENTS) return;
    evHeap[++evSz] = { t,m,a };
    int i = evSz;
    while (i > 1) {
        int p = i >> 1;
        if (!evLess(i, p)) break;
        evSwap(i, p); i = p;
    }
}
Event evTop() { return evHeap[1]; }
void evPop() {
    if (!evSz) return;
    evHeap[1] = evHeap[evSz--];
    int i = 1;
    while (true) {
        int l = i << 1, r = l + 1, best = i;
        if (l <= evSz && evLess(l, best)) best = l;
        if (r <= evSz && evLess(r, best)) best = r;
        if (best == i) break;
        evSwap(i, best); i = best;
    }
}

unsigned long long seedLCG = 42ULL;
double rnd01() {
    seedLCG = seedLCG * 6364136223846793005ULL + 1ULL;
    unsigned long long x = (seedLCG >> 11) & ((1ULL << 53) - 1);
    return x / (double)(1ULL << 53);
}

double commTime(int aFrom, int aTo) {
    if (aFrom == aTo) return 0.0;
    double d = distAg[aFrom][aTo];
    if (d > 1e90) return 1e9;
    return d;
}
double durationOnAgent(int mod, int ag) {
    double s = speedAg[ag];
    if (s <= 0) s = 1e-9;
    return workMod[mod] / s;
}
double earliestStart(int mod, int ag) {
    double est = agentFree[ag];

    for (int e = predHead[mod]; e; e = predNext[e]) {
        int u = predTo[e];
        if (!doneMod[u]) continue;
        int agU = assignedAgent[u];
        double readyAt = finishTimeM[u] + commTime(agU, ag);
        if (readyAt > est) est = readyAt;
    }
    return est;
}
int bestAgentFor(int mod, int avoidAg) {
    double best = INF; int bestA = 1;
    for (int a = 1; a <= N; ++a) {
        if (a == avoidAg) continue;
        double st = earliestStart(mod, a);
        double fn = st + durationOnAgent(mod, a);
        if (fn < best) { best = fn; bestA = a; }
    }
    return bestA;
}
int argMinAgentFree() {
    int best = 1;
    for (int a = 2; a <= N; ++a) if (agentFree[a] < agentFree[best]) best = a;
    return best;
}

bool isDAG() {
    int indeg[MAXM + 1];
    for (int i = 1; i <= M; ++i) indeg[i] = indegInit[i];
    qL = qR = 0;
    for (int i = 1; i <= M; ++i) if (indeg[i] == 0) qArr[qR++] = i;
    int seen = 0;
    while (qL < qR) {
        int u = qArr[qL++]; ++seen;
        for (int e = succHead[u]; e; e = succNext[e]) {
            int v = succTo[e];
            indeg[v]--;
            if (indeg[v] == 0) qArr[qR++] = v;
        }
    }
    return seen == M;
}

void floyd() {
    for (int i = 1; i <= N; ++i) {
        for (int j = 1; j <= N; ++j) {
            if (i == j) distAg[i][j] = 0.0;
            else if (distAg[i][j] < 0) distAg[i][j] = INF;
        }
    }
    for (int k = 1; k <= N; ++k)
        for (int i = 1; i <= N; ++i)
            for (int j = 1; j <= N; ++j) {
                double nd = distAg[i][k] + distAg[k][j];
                if (nd < distAg[i][j]) distAg[i][j] = nd;
            }
}

void tryScheduleReady() {
    while (readySz > 0) {
        int freeAg = argMinAgentFree();
        int i = readyTop();

        int best = bestAgentFor(i, -1);
        double bestFin = earliestStart(i, best) + durationOnAgent(i, best);
        double freeFin = earliestStart(i, freeAg) + durationOnAgent(i, freeAg);
        int a = (freeFin < bestFin) ? freeAg : best;

        readyPop();
        double st = earliestStart(i, a);
        double fn = st + durationOnAgent(i, a);
        assignedAgent[i] = a; startTimeM[i] = st; finishTimeM[i] = fn;
        agentFree[a] = fn;
        evPush(fn, i, a);
    }
}

double runSim(double p_fail, bool verbose) {
    if (!isDAG()) {
        if (verbose) cout << "Граф приложения не DAG. Завершение.\n";
        return -1.0;
    }
    floyd();

    for (int i = 1; i <= M; ++i) {
        assignedAgent[i] = -1; startTimeM[i] = finishTimeM[i] = 0.0;
        remainingPred[i] = indegInit[i]; doneMod[i] = 0; readyIn[i] = false;
    }
    for (int a = 1; a <= N; ++a) agentFree[a] = 0.0;
    readySz = 0; evSz = 0;

    for (int i = 1; i <= M; ++i) if (indegInit[i] == 0) readyPush(i);
    tryScheduleReady();

    double T = 0.0; int finished = 0;
    while (evSz > 0) {
        Event ev = evTop(); evPop();
        T = ev.t; int i = ev.mod, a = ev.ag;

        double r = rnd01();
        if (r < p_fail) {
            int newA = bestAgentFor(i, a);
            double st = agentFree[newA];
            double c = commTime(a, newA);
            if (T + c > st) st = T + c;
            double fn = st + durationOnAgent(i, newA);
            assignedAgent[i] = newA; startTimeM[i] = st; finishTimeM[i] = fn;
            agentFree[newA] = fn;
            evPush(fn, i, newA);
            if (verbose) {
                cout << "[FAIL] LP " << i << " на " << a
                    << " перенесён на " << newA
                    << " t=" << T << " -> рестарт " << st << " финиш " << fn << "\n";
            }
            continue;
        }

        doneMod[i] = 1; ++finished;
        if (verbose) {
            cout << "[DONE] LP " << i << " на " << a
                << " старт=" << startTimeM[i]
                << " финиш=" << finishTimeM[i] << "\n";
        }

        for (int e = succHead[i]; e; e = succNext[e]) {
            int v = succTo[e];
            remainingPred[v]--;
            if (remainingPred[v] == 0) readyPush(v);
        }
        tryScheduleReady();
    }

    if (verbose) {
        cout << "=== Общее время выполнения: " << T << "\n";
    }
    return T;
}

bool readInput() {
    if (!(cin >> M >> E)) return false;
    for (int i = 1; i <= M; ++i) {
        succHead[i] = predHead[i] = 0; indegInit[i] = 0;
    }
    succCnt = predCnt = 0;

    for (int i = 1; i <= M; ++i) cin >> workMod[i];
    for (int k = 0; k < E; ++k) { int u, v; cin >> u >> v; addEdgeApp(u, v); }

    cin >> N >> F;
    for (int i = 1; i <= N; ++i) cin >> speedAg[i];
    for (int i = 1; i <= N; ++i)
        for (int j = 1; j <= N; ++j) distAg[i][j] = (i == j) ? 0.0 : INF;

    for (int k = 0; k < F; ++k) {
        int a, b; double lat; cin >> a >> b >> lat;
        if (lat < distAg[a][b]) { distAg[a][b] = lat; distAg[b][a] = lat; }
    }
    return true;
}

void loadTest1() {
    M = 6; E = 6;
    for (int i = 1; i <= M; ++i) { succHead[i] = predHead[i] = 0; indegInit[i] = 0; }
    succCnt = predCnt = 0;
    workMod[1] = 8; workMod[2] = 6; workMod[3] = 5; workMod[4] = 3; workMod[5] = 2; workMod[6] = 4;
    addEdgeApp(1, 3); addEdgeApp(2, 3);
    addEdgeApp(3, 4); addEdgeApp(3, 5);
    addEdgeApp(4, 6); addEdgeApp(5, 6);

    N = 3; speedAg[1] = 1.0; speedAg[2] = 1.2; speedAg[3] = 0.8;
    for (int i = 1; i <= N; ++i) for (int j = 1; j <= N; ++j) distAg[i][j] = (i == j) ? 0.0 : INF;
    distAg[1][2] = distAg[2][1] = 0.5;
    distAg[2][3] = distAg[3][2] = 0.7;
    distAg[1][3] = distAg[3][1] = 1.0;
}
void loadTest2() {
    M = 8; E = 8;
    for (int i = 1; i <= M; ++i) { succHead[i] = predHead[i] = 0; indegInit[i] = 0; }
    succCnt = predCnt = 0;
    double w[9] = { 0,4,7,3,6,2,5,8,4 };
    for (int i = 1; i <= 8; ++i) workMod[i] = w[i];
    addEdgeApp(1, 3); addEdgeApp(2, 3); addEdgeApp(2, 4);
    addEdgeApp(3, 5); addEdgeApp(4, 6); addEdgeApp(5, 7); addEdgeApp(6, 7);
    addEdgeApp(7, 8);

    N = 4; speedAg[1] = 1.5; speedAg[2] = 1.0; speedAg[3] = 1.2; speedAg[4] = 0.9;
    for (int i = 1; i <= N; ++i) for (int j = 1; j <= N; ++j) distAg[i][j] = (i == j) ? 0.0 : INF;
    distAg[1][2] = distAg[2][1] = 0.3; distAg[2][3] = distAg[3][2] = 0.4;
    distAg[3][4] = distAg[4][3] = 0.6; distAg[1][4] = distAg[4][1] = 1.2;
}
void loadTest3() {
    M = 7; E = 6;
    for (int i = 1; i <= M; ++i) { succHead[i] = predHead[i] = 0; indegInit[i] = 0; }
    succCnt = predCnt = 0;
    double w[8] = { 0,10,9,8,7,6,5,4 };
    for (int i = 1; i <= 7; ++i) workMod[i] = w[i];
    addEdgeApp(1, 4); addEdgeApp(2, 4); addEdgeApp(3, 5);
    addEdgeApp(4, 6); addEdgeApp(5, 6); addEdgeApp(6, 7);

    N = 5; speedAg[1] = 2.2; speedAg[2] = 1.0; speedAg[3] = 0.9; speedAg[4] = 1.1; speedAg[5] = 0.8;
    for (int i = 1; i <= N; ++i) for (int j = 1; j <= N; ++j) distAg[i][j] = (i == j) ? 0.0 : INF;
    distAg[1][2] = distAg[2][1] = 0.2; distAg[2][3] = distAg[3][2] = 0.5;
    distAg[3][4] = distAg[4][3] = 0.5; distAg[4][5] = distAg[5][4] = 0.5; distAg[1][5] = distAg[5][1] = 1.0;
}

int main() {
    setlocale(LC_ALL, "rus");

    if (readInput()) {
        seedLCG = 42ULL;
        runSim(0.05, true);
        return 0;
    }

    cout << "### Тест 1\n";
    loadTest1(); seedLCG = 12345ULL; runSim(0.05, true); cout << "\n";
    cout << "### Тест 2\n";
    loadTest2(); seedLCG = 67890ULL; runSim(0.05, true); cout << "\n";
    cout << "### Тест 3\n";
    loadTest3(); seedLCG = 424242ULL; runSim(0.05, true); cout << "\n";
    return 0;
}
