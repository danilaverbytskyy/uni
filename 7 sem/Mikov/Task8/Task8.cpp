#include <iostream>
#include <vector>
#include <random>
#include <iomanip>
#include <algorithm>

using namespace std;

const int   MAX_LEVEL = 10;
const double EXP_FOR_LEVEL = 100.0;

const double START_BALANCE = 200.0;
const double START_INCOME = 40.0;
const double START_EXPENSE = 25.0;

const int ITER_PER_CYCLE = 10;
const int MAX_CYCLES = 200;

const int AUCTION_PERIOD = 5;
const int ENV_PERIOD = 7;

const double ENV_G = 5.0;
const double ENV_J = 5.0;

/* Артефакт 3:
   Эффект: текущий баланс + n% от дохода,
   Продолжительность: сначала n циклов и потом m итераций */
const double ART3_N_PERCENT = 20.0;
const int    ART3_N_CYCLES = 3;
const int    ART3_M_ITERS = 5;
const double ART3_PRICE = 30.0;

/* Артефакт 18:
   1) Обнуление расхода на протяжении n циклов.
   2) Текущий доход + n% от баланса на протяжении n итераций.
   3) (Мифический) установить предмаксимальный уровень колонии
      на протяжении n итераций (разово, не более 1 у каждой колонии). */
const int    ART18_N_CYCLES_ZERO_EXP = 3;
const int    ART18_N_ITERS_INC_BAL = 15;
const double ART18_INC_FROM_BAL_P = 10.0;
const int    ART18_N_ITERS_MYTHIC = 5;
const double ART18_PRICE = 60.0;

/* Артефакт 67:
   1) + n уровней (единоразово).
   2) Текущий расход - n% до следующего аукциона.
   3) Текущий баланс + n% от расходов до следующего аукциона. */
const int    ART67_LEVELS_PLUS = 2;
const double ART67_EXPENSE_MINUS_P = 25.0;
const double ART67_BALANCE_FROM_EXP_P = 20.0;
const double ART67_PRICE = 70.0;

/* Артефакт 92:
   1) Текущий доход x2 до следующего события среды.
   2) Текущий баланс + n% от дохода на протяжении n итераций.
   3) + n% к опыту от максимального опыта уровня до следующего аукциона. */
const double ART92_BALANCE_FROM_INC_P = 15.0;
const int    ART92_N_ITERS_BALANCE_INC = 10;
const double ART92_EXP_PLUS_P_OF_MAX = 10.0;
const double ART92_PRICE = 80.0;

/* Артефакт 98:
   1) + n единиц опыта (единоразово).
   2) Текущий баланс + n единиц условной валюты до следующего события среды. */
const double ART98_EXP_PLUS = 40.0;
const double ART98_BALANCE_PLUS = 50.0;
const double ART98_PRICE = 40.0;

enum class EffectKind {
    ZERO_EXPENSE,
    EXPENSE_MINUS_PERCENT,
    INCOME_X2,
    ADD_INCOME_PERCENT_OF_BAL,
    ADD_BALANCE_PERCENT_OF_INC,
    BALANCE_PLUS_PERCENT_OF_EXP,
    EXP_GAIN_PERCENT_OF_MAX,
    EXP_PLUS_N_ONCE,
    BALANCE_PLUS_N_ONCE,
    LEVEL_PLUS_N_ONCE,
    SET_LEVEL_PREMAX_ONCE
};

struct Effect {
    EffectKind kind;
    double value;
    int stepsLeft;
    bool removeOnAuction;
    bool removeOnEnv;
    bool appliedOnce;
};

struct Colony {
    double balance;
    double income;
    double expense;
    double exp;
    int level;
    int maxLevel;
    bool alive;
    bool win;
    bool mythicUsed;
    vector<Effect> effects;
};

void addEffect(Colony& c, EffectKind kind, double value,
    int stepsLeft, bool remAuction = false,
    bool remEnv = false, bool appliedOnce = false)
{
    c.effects.push_back({ kind, value, stepsLeft, remAuction, remEnv, appliedOnce });
}

void tickEffects(Colony& c)
{
    for (auto& e : c.effects) {
        if (e.stepsLeft > 0) e.stepsLeft--;
    }
    c.effects.erase(
        remove_if(c.effects.begin(), c.effects.end(),
            [](const Effect& e) {
                return e.stepsLeft == 0 &&
                    !e.removeOnAuction &&
                    !e.removeOnEnv;
            }),
        c.effects.end()
    );
}

void clearAuctionEffects(Colony& c)
{
    c.effects.erase(
        remove_if(c.effects.begin(), c.effects.end(),
            [](const Effect& e) { return e.removeOnAuction; }),
        c.effects.end()
    );
}

void clearEnvEffects(Colony& c)
{
    c.effects.erase(
        remove_if(c.effects.begin(), c.effects.end(),
            [](const Effect& e) { return e.removeOnEnv; }),
        c.effects.end()
    );
}

void updateColonyAtCycleStart(Colony& c)
{
    if (!c.alive || c.win) return;

    double effIncome = c.income;
    double effExpense = c.expense;

    for (auto& e : c.effects) {
        switch (e.kind) {
        case EffectKind::ZERO_EXPENSE:
            effExpense = 0.0;
            break;
        case EffectKind::EXPENSE_MINUS_PERCENT:
            effExpense *= (1.0 - e.value);
            break;
        case EffectKind::INCOME_X2:
            effIncome *= 2.0;
            break;
        case EffectKind::ADD_INCOME_PERCENT_OF_BAL:
            effIncome += c.balance * e.value;
            break;
        default:
            break;
        }
    }

    double extraBalance = 0.0;
    double extraExp = 0.0;

    for (auto& e : c.effects) {
        switch (e.kind) {
        case EffectKind::ADD_BALANCE_PERCENT_OF_INC:
            extraBalance += effIncome * e.value;
            break;
        case EffectKind::BALANCE_PLUS_PERCENT_OF_EXP:
            extraBalance += effExpense * e.value;
            break;
        case EffectKind::EXP_GAIN_PERCENT_OF_MAX:
            extraExp += EXP_FOR_LEVEL * e.value;
            break;
        case EffectKind::EXP_PLUS_N_ONCE:
            if (!e.appliedOnce) {
                extraExp += e.value;
                e.appliedOnce = true;
            }
            break;
        case EffectKind::BALANCE_PLUS_N_ONCE:
            if (!e.appliedOnce) {
                extraBalance += e.value;
                e.appliedOnce = true;
            }
            break;
        case EffectKind::LEVEL_PLUS_N_ONCE:
            if (!e.appliedOnce) {
                c.level += (int)(e.value + 0.5);
                if (c.level > c.maxLevel) c.level = c.maxLevel;
                e.appliedOnce = true;
            }
            break;
        case EffectKind::SET_LEVEL_PREMAX_ONCE:
            if (!e.appliedOnce && !c.mythicUsed) {
                c.level = max(c.level, c.maxLevel - 1);
                c.mythicUsed = true;
                e.appliedOnce = true;
            }
            break;
        default:
            break;
        }
    }

    double prevBalance = c.balance;
    c.balance += effIncome - effExpense + extraBalance;

    c.exp += (c.balance - prevBalance) + extraExp;
    if (c.exp < 0.0) c.exp = 0.0;

    while (c.exp >= EXP_FOR_LEVEL && c.level < c.maxLevel) {
        c.exp -= EXP_FOR_LEVEL;
        c.level++;
    }

    if (c.balance < 0.0) c.alive = false;
    if (c.level >= c.maxLevel) c.win = true;
}

/* Артефакт 3 */
void applyArtifact3(Colony& c)
{
    int steps = ART3_N_CYCLES * ITER_PER_CYCLE + ART3_M_ITERS;
    addEffect(c,
        EffectKind::ADD_BALANCE_PERCENT_OF_INC,
        ART3_N_PERCENT / 100.0,
        steps);
}

/* Артефакт 18 */
void applyArtifact18(Colony& c)
{
    addEffect(c,
        EffectKind::ZERO_EXPENSE,
        0.0,
        ART18_N_CYCLES_ZERO_EXP * ITER_PER_CYCLE);

    addEffect(c,
        EffectKind::ADD_INCOME_PERCENT_OF_BAL,
        ART18_INC_FROM_BAL_P / 100.0,
        ART18_N_ITERS_INC_BAL);

    addEffect(c,
        EffectKind::SET_LEVEL_PREMAX_ONCE,
        0.0,
        ART18_N_ITERS_MYTHIC);
}

/* Артефакт 67 */
void applyArtifact67(Colony& c)
{
    addEffect(c,
        EffectKind::LEVEL_PLUS_N_ONCE,
        ART67_LEVELS_PLUS,
        1);

    addEffect(c,
        EffectKind::EXPENSE_MINUS_PERCENT,
        ART67_EXPENSE_MINUS_P / 100.0,
        -1,
        true,
        false);

    addEffect(c,
        EffectKind::BALANCE_PLUS_PERCENT_OF_EXP,
        ART67_BALANCE_FROM_EXP_P / 100.0,
        -1,
        true,
        false);
}

/* Артефакт 92 */
void applyArtifact92(Colony& c)
{
    addEffect(c,
        EffectKind::INCOME_X2,
        0.0,
        -1,
        false,
        true);

    addEffect(c,
        EffectKind::ADD_BALANCE_PERCENT_OF_INC,
        ART92_BALANCE_FROM_INC_P / 100.0,
        ART92_N_ITERS_BALANCE_INC);

    addEffect(c,
        EffectKind::EXP_GAIN_PERCENT_OF_MAX,
        ART92_EXP_PLUS_P_OF_MAX / 100.0,
        -1,
        true,
        false);
}

/* Артефакт 98 */
void applyArtifact98(Colony& c)
{
    addEffect(c,
        EffectKind::EXP_PLUS_N_ONCE,
        ART98_EXP_PLUS,
        1);

    addEffect(c,
        EffectKind::BALANCE_PLUS_N_ONCE,
        ART98_BALANCE_PLUS,
        -1,
        false,
        true);
}

bool decideToBuy(const Colony& c, double price)
{
    double reserve = 2.0 * c.expense;
    return c.balance - price > reserve;
}

void runAuction(Colony& c, mt19937& rng)
{
    clearAuctionEffects(c);

    uniform_int_distribution<int> artDist(0, 4);
    int idx = artDist(rng);

    int artifactId;
    double price;

    if (idx == 0) { artifactId = 3;  price = ART3_PRICE; }
    else if (idx == 1) { artifactId = 18; price = ART18_PRICE; }
    else if (idx == 2) { artifactId = 67; price = ART67_PRICE; }
    else if (idx == 3) { artifactId = 92; price = ART92_PRICE; }
    else { artifactId = 98; price = ART98_PRICE; }

    if (!decideToBuy(c, price) || c.balance < price) return;

    c.balance -= price;

    if (artifactId == 3)  applyArtifact3(c);
    else if (artifactId == 18) applyArtifact18(c);
    else if (artifactId == 67) applyArtifact67(c);
    else if (artifactId == 92) applyArtifact92(c);
    else if (artifactId == 98) applyArtifact98(c);
}

void runEnvironmentEvent(Colony& c, mt19937& rng)
{
    clearEnvEffects(c);

    uniform_real_distribution<double> prob(0.0, 1.0);
    double p = prob(rng);

    if (p < 0.5) {
        c.income -= ENV_G;
        c.expense += ENV_J;
    }
    else {
        c.income += ENV_G;
        c.expense -= ENV_J;
        if (c.expense < 0.0) c.expense = 0.0;
    }
}

struct RunResult {
    bool win;
    int lifeCycles;
};

RunResult simulateOneRun(mt19937& rng)
{
    Colony c;
    c.balance = START_BALANCE;
    c.income = START_INCOME;
    c.expense = START_EXPENSE;
    c.exp = 0.0;
    c.level = 1;
    c.maxLevel = MAX_LEVEL;
    c.alive = true;
    c.win = false;
    c.mythicUsed = false;
    c.effects.clear();

    int livedCycles = 0;

    for (int cycle = 0;
        cycle < MAX_CYCLES && c.alive && !c.win;
        ++cycle)
    {
        if (cycle > 0 && cycle % AUCTION_PERIOD == 0)
            runAuction(c, rng);

        if (cycle > 0 && cycle % ENV_PERIOD == 0)
            runEnvironmentEvent(c, rng);

        for (int it = 0; it < ITER_PER_CYCLE; ++it) {
            if (it == 0) {
                updateColonyAtCycleStart(c);
                if (!c.alive || c.win) break;
                livedCycles++;
            }
            tickEffects(c);
        }
    }

    return { c.win, livedCycles };
}

int main()
{
    setlocale(LC_ALL, "Russian");

    int experiments;
    cout << "Введите количество экспериментов: ";
    cin >> experiments;

    mt19937 rng(42);

    int wins = 0;
    int loses = 0;
    vector<int> lifeHist(MAX_CYCLES + 1, 0);

    for (int i = 0; i < experiments; ++i) {
        RunResult r = simulateOneRun(rng);
        if (r.win) wins++;
        else       loses++;

        if (r.lifeCycles >= 0 && r.lifeCycles <= MAX_CYCLES)
            lifeHist[r.lifeCycles]++;
    }

    cout << "\nРезультаты моделирования\n";
    cout << "Экспериментов: " << experiments << "\n";
    cout << "Победы: " << wins
        << " (P = " << fixed << setprecision(3)
        << (double)wins / experiments << ")\n";
    cout << "Поражения: " << loses
        << " (P = " << fixed << setprecision(3)
        << (double)loses / experiments << ")\n\n";

    cout << "Распределение времени жизни колонии (в циклах):\n";
    cout << "cycles\tprobability\n";
    for (int c = 1; c <= MAX_CYCLES; ++c) {
        if (lifeHist[c] == 0) continue;
        double p = (double)lifeHist[c] / experiments;
        cout << c << "\t" << fixed << setprecision(4) << p << "\n";
    }

    return 0;
}
