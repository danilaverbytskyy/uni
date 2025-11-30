#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <string>

using namespace std;

struct Card {
    int rank;
    int suit;
};

string rankToStr(int r) {
    if (r >= 2 && r <= 9) {
        string s;
        s.push_back(char('0' + r));
        return s;
    }
    if (r == 10) return "10";
    if (r == 11) return "J";
    if (r == 12) return "Q";
    if (r == 13) return "K";
    if (r == 14) return "A";
    return "?";
}

string suitToStr(int s) {
    static const char* names[] = { "C", "D", "H", "S" }; // трефы, бубны, червы, пики
    if (s < 0 || s > 3) return "?";
    return names[s];
}

string cardToStr(const Card& c) {
    return rankToStr(c.rank) + suitToStr(c.suit);
}

bool lessRank(const Card& a, const Card& b) {
    if (a.rank != b.rank) return a.rank < b.rank;
    return a.suit < b.suit;
}

bool canBeat(const Card& attack, const Card& defend, int kozMast) {
    if (attack.suit == defend.suit && defend.rank > attack.rank) return true;
    if (defend.suit == kozMast && attack.suit != kozMast) return true;
    return false;
}

struct Player {
    vector<Card> hand;
    int algo; // 1 или 2
    bool alive() const { return !hand.empty(); }
};

int partner(int idx) { return (idx + 2) % 4; }

int chooseAttackCard(const Player& p, const vector<int>& tableRanks, int kozMast) {
    vector<int> candidates;
    for (int i = 0; i < (int)p.hand.size(); ++i) {
        if (tableRanks.empty()) {
            candidates.push_back(i);
        }
        else {
            int r = p.hand[i].rank;
            for (size_t j = 0; j < tableRanks.size(); ++j) {
                if (tableRanks[j] == r) {
                    candidates.push_back(i);
                    break;
                }
            }
        }
    }
    if (candidates.empty()) return -1;

    int best = candidates[0];
    if (p.algo == 1) {
        for (size_t k = 0; k < candidates.size(); ++k) {
            int id = candidates[k];
            const Card& c = p.hand[id];
            const Card& b = p.hand[best];
            bool cKoz = (c.suit == kozMast);
            bool bKoz = (b.suit == kozMast);
            if (cKoz != bKoz) {
                if (!cKoz && bKoz) best = id;
            }
            else {
                if (lessRank(c, b)) best = id;
            }
        }
    }
    else {
        for (size_t k = 0; k < candidates.size(); ++k) {
            int id = candidates[k];
            const Card& c = p.hand[id];
            const Card& b = p.hand[best];
            bool cKoz = (c.suit == kozMast);
            bool bKoz = (b.suit == kozMast);
            if (cKoz != bKoz) {
                if (!cKoz && bKoz) best = id;
            }
            else {
                if (lessRank(b, c)) best = id;
            }
        }
    }
    return best;
}

int chooseDefenseCard(const Player& p, const Card& attackCard, int kozMast, int tableSize) {
    vector<int> beatSameSuit;
    vector<int> mozhetKozirem;

    for (int i = 0; i < (int)p.hand.size(); ++i) {
        const Card& c = p.hand[i];
        if (!canBeat(attackCard, c, kozMast)) continue;
        if (c.suit == attackCard.suit) beatSameSuit.push_back(i);
        else mozhetKozirem.push_back(i);
    }

    if (p.algo == 1) {
        if (!beatSameSuit.empty()) {
            int best = beatSameSuit[0];
            for (size_t k = 0; k < beatSameSuit.size(); ++k) {
                int id = beatSameSuit[k];
                if (lessRank(p.hand[id], p.hand[best])) best = id;
            }
            return best;
        }
        if (!mozhetKozirem.empty() && tableSize <= 2) {
            int best = mozhetKozirem[0];
            for (size_t k = 0; k < mozhetKozirem.size(); ++k) {
                int id = mozhetKozirem[k];
                if (lessRank(p.hand[id], p.hand[best])) best = id;
            }
            return best;
        }
        return -1;
    }
    else {
        if (!beatSameSuit.empty() || !mozhetKozirem.empty()) {
            int best = -1;
            for (size_t k = 0; k < beatSameSuit.size(); ++k) {
                int id = beatSameSuit[k];
                if (best == -1 || lessRank(p.hand[id], p.hand[best])) best = id;
            }
            for (size_t k = 0; k < mozhetKozirem.size(); ++k) {
                int id = mozhetKozirem[k];
                if (best == -1 || lessRank(p.hand[id], p.hand[best])) best = id;
            }
            return best;
        }
        return -1;
    }
}

int chooseTranslateCard(const Player& p, const Card& attackCard, int kozMast) {
    vector<int> candidates;
    for (int i = 0; i < (int)p.hand.size(); ++i) {
        const Card& c = p.hand[i];
        if (c.rank == attackCard.rank && c.suit != attackCard.suit)
            candidates.push_back(i);
    }
    if (candidates.empty()) return -1;

    if (p.algo == 1) {
        int best = candidates[0];
        for (size_t k = 0; k < candidates.size(); ++k) {
            int id = candidates[k];
            if (lessRank(p.hand[id], p.hand[best])) best = id;
        }
        return best;
    }
    else {
        int best = -1;
        for (size_t k = 0; k < candidates.size(); ++k) {
            int id = candidates[k];
            const Card& c = p.hand[id];
            if (c.rank <= 10) {
                if (best == -1 || lessRank(c, p.hand[best])) best = id;
            }
        }
        return best;
    }
}

vector<int> collectRanks(const vector<Card>& a, const vector<Card>& d) {
    vector<int> r;
    for (size_t i = 0; i < a.size(); ++i) r.push_back(a[i].rank);
    for (size_t i = 0; i < d.size(); ++i)
        if (d[i].rank != 0) r.push_back(d[i].rank);
    sort(r.begin(), r.end());
    r.erase(unique(r.begin(), r.end()), r.end());
    return r;
}

struct GameState {
    vector<Card> deck;
    vector<Card> discard;
    Player players[4];
    int kozMast;
    Card kozKarta;
};

mt19937 rngEngine((unsigned int)chrono::high_resolution_clock::now()
    .time_since_epoch().count());

Card drawCard(GameState& g) {
    Card c = g.deck.back();
    g.deck.pop_back();
    return c;
}

void deal(GameState& g) {
    g.deck.clear();
    g.discard.clear();

    for (int s = 0; s < 4; ++s)
        for (int r = 2; r <= 14; ++r)
            g.deck.push_back(Card{ r, s });

    shuffle(g.deck.begin(), g.deck.end(), rngEngine);

    g.kozKarta = g.deck.back();
    g.kozMast = g.kozKarta.suit;

    for (int i = 0; i < 4; ++i) g.players[i].hand.clear();

    const int START = 6;
    for (int round = 0; round < START; ++round) {
        for (int i = 0; i < 4; ++i) {
            g.players[i].hand.push_back(drawCard(g));
        }
    }
}

void refillHands(GameState& g, int startIdx) {
    const int TARGET = 6;
    for (int k = 0; k < 4; ++k) {
        int i = (startIdx + k) % 4;
        while ((int)g.players[i].hand.size() < TARGET && !g.deck.empty()) {
            g.players[i].hand.push_back(drawCard(g));
        }
    }
}

int chooseFirstAttacker(const GameState& g) {
    int bestPlayer = 0;
    bool inited = false;
    Card bestCard;
    for (int i = 0; i < 4; ++i) {
        for (size_t j = 0; j < g.players[i].hand.size(); ++j) {
            Card c = g.players[i].hand[j];
            if (c.suit != g.kozMast) continue;
            if (!inited || lessRank(c, bestCard)) {
                inited = true;
                bestCard = c;
                bestPlayer = i;
            }
        }
    }
    if (!inited) {
        uniform_int_distribution<int> dist(0, 3);
        return dist(rngEngine);
    }
    return bestPlayer;
}

int chooseDefenderForPair(int attacker) {
    if (attacker == 0 || attacker == 2) {
        uniform_int_distribution<int> d(0, 1);
        int x = d(rngEngine);
        return (x == 0 ? 1 : 3);
    }
    else {
        uniform_int_distribution<int> d(0, 1);
        int x = d(rngEngine);
        return (x == 0 ? 0 : 2);
    }
}

int playRound(GameState& g, int& attackerIdx, int& defenderIdx) {
    vector<Card> attackCards;
    vector<Card> defendCards;

    bool firstIteration = true;
    int pairAttack = (attackerIdx == 0 || attackerIdx == 2) ? 0 : 1;
    int pairDefend = 1 - pairAttack;

    while (true) {
        vector<int> tableRanks = collectRanks(attackCards, defendCards);
        int aId = chooseAttackCard(g.players[attackerIdx], tableRanks, g.kozMast);
        if (aId == -1) {
            for (size_t i = 0; i < attackCards.size(); ++i) g.discard.push_back(attackCards[i]);
            for (size_t i = 0; i < defendCards.size(); ++i)
                if (defendCards[i].rank != 0) g.discard.push_back(defendCards[i]);
            return pairDefend;
        }
        Card aCard = g.players[attackerIdx].hand[aId];
        g.players[attackerIdx].hand.erase(g.players[attackerIdx].hand.begin() + aId);
        attackCards.push_back(aCard);
        defendCards.push_back(Card{ 0, 0 });

        if (firstIteration) {
            int tId = chooseTranslateCard(g.players[defenderIdx], aCard, g.kozMast);
            if (tId != -1 && g.players[partner(attackerIdx)].alive()) {
                Card tCard = g.players[defenderIdx].hand[tId];
                g.players[defenderIdx].hand.erase(g.players[defenderIdx].hand.begin() + tId);
                attackCards.push_back(tCard);
                defendCards.push_back(Card{ 0,0 });

                int oldAtt = attackerIdx;
                int oldDef = defenderIdx;
                attackerIdx = partner(oldDef);
                defenderIdx = partner(oldAtt);

                pairAttack = (attackerIdx == 0 || attackerIdx == 2) ? 0 : 1;
                pairDefend = 1 - pairAttack;
            }
            firstIteration = false;
        }

        bool defenderTakes = false;
        for (size_t i = 0; i < attackCards.size(); ++i) {
            if (defendCards[i].rank != 0) continue;
            int dId = chooseDefenseCard(
                g.players[defenderIdx], attackCards[i], g.kozMast,
                (int)attackCards.size());
            if (dId == -1) {
                defenderTakes = true;
                break;
            }
            Card dCard = g.players[defenderIdx].hand[dId];
            g.players[defenderIdx].hand.erase(
                g.players[defenderIdx].hand.begin() + dId);
            defendCards[i] = dCard;
        }

        if (defenderTakes) {
            for (size_t i = 0; i < attackCards.size(); ++i)
                g.players[defenderIdx].hand.push_back(attackCards[i]);
            for (size_t i = 0; i < defendCards.size(); ++i)
                if (defendCards[i].rank != 0)
                    g.players[defenderIdx].hand.push_back(defendCards[i]);
            attackCards.clear();
            defendCards.clear();
            return pairAttack;
        }

        while (true) {
            tableRanks = collectRanks(attackCards, defendCards);
            int maxExtra = (int)g.players[defenderIdx].hand.size()
                - (int)attackCards.size();
            if (maxExtra <= 0) goto finish_round_success_def;

            bool added = false;
            int attackers[2] = { attackerIdx, partner(attackerIdx) };
            for (int k = 0; k < 2; ++k) {
                int pid = attackers[k];
                if (!g.players[pid].alive()) continue;
                int idx = chooseAttackCard(g.players[pid], tableRanks, g.kozMast);
                if (idx == -1) continue;
                Card c = g.players[pid].hand[idx];
                bool okRank = false;
                for (size_t t = 0; t < tableRanks.size(); ++t)
                    if (tableRanks[t] == c.rank) { okRank = true; break; }
                if (!okRank) continue;
                g.players[pid].hand.erase(g.players[pid].hand.begin() + idx);
                attackCards.push_back(c);
                defendCards.push_back(Card{ 0,0 });
                added = true;
                break;
            }
            if (!added) {
                goto finish_round_success_def;
            }

            bool localDefenderTakes = false;
            for (size_t i = 0; i < attackCards.size(); ++i) {
                if (defendCards[i].rank != 0) continue;
                int dId = chooseDefenseCard(
                    g.players[defenderIdx], attackCards[i], g.kozMast,
                    (int)attackCards.size());
                if (dId == -1) { localDefenderTakes = true; break; }
                Card dCard = g.players[defenderIdx].hand[dId];
                g.players[defenderIdx].hand.erase(
                    g.players[defenderIdx].hand.begin() + dId);
                defendCards[i] = dCard;
            }
            if (localDefenderTakes) {
                for (size_t i = 0; i < attackCards.size(); ++i)
                    g.players[defenderIdx].hand.push_back(attackCards[i]);
                for (size_t i = 0; i < defendCards.size(); ++i)
                    if (defendCards[i].rank != 0)
                        g.players[defenderIdx].hand.push_back(defendCards[i]);
                attackCards.clear();
                defendCards.clear();
                return pairAttack;
            }
        }

    finish_round_success_def:
        for (size_t i = 0; i < attackCards.size(); ++i) g.discard.push_back(attackCards[i]);
        for (size_t i = 0; i < defendCards.size(); ++i)
            if (defendCards[i].rank != 0) g.discard.push_back(defendCards[i]);
        attackCards.clear();
        defendCards.clear();
        return pairDefend;
    }
}

int playGameOnce() {
    GameState g;
    g.players[0].algo = 1;
    g.players[2].algo = 1;
    g.players[1].algo = 2;
    g.players[3].algo = 2;

    deal(g);

    int attacker = chooseFirstAttacker(g);
    int defender = chooseDefenderForPair(attacker);

    int lastLeadInPair[2] = { 0, 1 };

    const int MAX_ROUNDS = 200;
    for (int round = 0; round < MAX_ROUNDS; ++round) {
        bool pair0Done = !g.players[0].alive() && !g.players[2].alive();
        bool pair1Done = !g.players[1].alive() && !g.players[3].alive();
        if (pair0Done && pair1Done) return -1;
        if (pair0Done) return 0;
        if (pair1Done) return 1;

        if (!g.players[attacker].alive()) attacker = partner(attacker);
        if (!g.players[attacker].alive()) {
            int pairAtt = (attacker == 0 || attacker == 2) ? 0 : 1;
            return pairAtt;
        }

        if (!g.players[defender].alive()) defender = partner(defender);
        if (!g.players[defender].alive()) {
            int pairDef = (defender == 0 || defender == 2) ? 0 : 1;
            return pairDef;
        }

        int winnerPair = playRound(g, attacker, defender);
        refillHands(g, attacker);
        int pairWin = winnerPair;

        if (pairWin == 0) {
            int a = lastLeadInPair[0];
            attacker = (a == 0 ? 2 : 0);
            lastLeadInPair[0] = attacker;
        }
        else {
            int a = lastLeadInPair[1];
            attacker = (a == 1 ? 3 : 1);
            lastLeadInPair[1] = attacker;
        }

        vector<int> candDef;
        for (int i = 0; i < 4; ++i) {
            bool samePairAsAtt = ((i == 0 || i == 2) == (attacker == 0 || attacker == 2));
            if (samePairAsAtt) continue;
            if (!g.players[i].alive()) continue;
            candDef.push_back(i);
        }
        if (candDef.empty()) {
            return (attacker == 0 || attacker == 2) ? 0 : 1;
        }
        uniform_int_distribution<int> d(0, (int)candDef.size() - 1);
        int pos = d(rngEngine);
        defender = candDef[pos];
    }
    return -1;
}

int main() {
    setlocale(LC_ALL, "rus");
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int experiments = 1000;
    int winsPair0 = 0;
    int winsPair1 = 0;
    int draws = 0;

    for (int i = 0; i < experiments; ++i) {
        int res = playGameOnce();
        if (res == 0) ++winsPair0;
        else if (res == 1) ++winsPair1;
        else ++draws;
    }

    cout << "Результаты моделирования " << experiments << " партий\n";
    cout << "Пара 1 (игроки 1 и 3, алгоритм 1) победила: " << winsPair0 << " раз(а)\n";
    cout << "Пара 2 (игроки 2 и 4, алгоритм 2) победила: " << winsPair1 << " раз(а)\n";
    cout << "Ничьих: " << draws << "\n";

    return 0;
}
