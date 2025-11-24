#include <iostream>
#include <vector>
#include <random>
#include <cmath>
#include <algorithm>
#include <map>

using namespace std;

random_device rd;
mt19937 gen(rd());

struct Point {
    double x, y;
    Point(double x = 0, double y = 0) : x(x), y(y) {}

    double distanceTo(const Point& other) const {
        return sqrt(pow(x - other.x, 2) + pow(y - other.y, 2));
    }
};

struct Square {
    int id;
    Point center;
    double size;

    Square(int id, Point center, double size) : id(id), center(center), size(size) {}
};

class Court {
public:
    double width, height;

    Court(double w = 10.0, double h = 20.0) : width(w), height(h) {}

    bool isInCourt(const Point& p) const {
        return p.x >= 0 && p.x <= width && p.y >= 0 && p.y <= height;
    }

    bool isOut(const Point& p) const {
        return !isInCourt(p);
    }
};

class Player {
public:
    Point position;
    double radius;
    double maxMove;

    Player(double r, double l) : radius(r), maxMove(l) {}

    void moveTo(const Point& target) {
        double dist = position.distanceTo(target);
        if (dist <= maxMove) {
            position = target;
        }
        else {
            double ratio = maxMove / dist;
            position.x = position.x + (target.x - position.x) * ratio;
            position.y = position.y + (target.y - position.y) * ratio;
        }
    }

    bool canReach(const Point& ball) const {
        return position.distanceTo(ball) <= radius;
    }
};

class Agent : public Player {
private:
    vector<Square> squares;
    int squareCount;

public:
    Agent(double r, double l, int n) : Player(2 * r, l), squareCount(n) {
        createSquares();
    }

    void createSquares() {
        squares.clear();
        int perRow = sqrt(squareCount);
        double size = 5.0 / perRow;

        for (int i = 0; i < squareCount; i++) {
            int row = i / perRow;
            int col = i % perRow;
            double x = col * size + size / 2;
            double y = row * size + size / 2;
            squares.push_back(Square(i, Point(x, y), size));
        }
    }

    int chooseSquare(const Point& dummyPos) {
        int bestSquare = 0;
        double maxDistance = 0;

        for (const auto& square : squares) {
            double dist = dummyPos.distanceTo(square.center);
            if (dist > maxDistance) {
                maxDistance = dist;
                bestSquare = square.id;
            }
        }
        return bestSquare;
    }

    Point getTargetWithError(int squareId) {
        uniform_real_distribution<> rand(0.0, 1.0);

        if (rand(gen) <= 0.95) {
            // Возвращаем центр квадрата
            return squares[squareId].center;
        }

        // Ошибка - случайное смещение
        uniform_real_distribution<> offset(-squares[squareId].size, squares[squareId].size);
        Point target = squares[squareId].center;
        target.x += offset(gen);
        target.y += offset(gen);

        return target;
    }
};

class Dummy : public Player {
public:
    Dummy(double r, double l) : Player(r, l) {}

    Point hitBall() {
        uniform_real_distribution<> xRand(0.0, 5.0);
        uniform_real_distribution<> yRand(10.0, 20.0);  // Исправленный диапазон
        return Point(xRand(gen), yRand(gen));
    }
};

class MatchSimulator {
private:
    Court court;
    Agent agent;
    Dummy dummy;

public:
    MatchSimulator(double r, double l, int n)
        : agent(r, l, n), dummy(r, l) {

        agent.position = Point(2.5, 18.0);
        dummy.position = Point(2.5, 2.0);
    }

    bool playRally(bool agentServes) {
        bool agentTurn = agentServes;
        Point ballPosition = agentServes ? agent.position : dummy.position;
        int shotCount = 0;
        const int maxShots = 10;

        while (shotCount < maxShots) {
            shotCount++;

            if (agentTurn) {
                int squareId = agent.chooseSquare(dummy.position);
                Point target = agent.getTargetWithError(squareId);

                if (court.isOut(target)) {
                    return false;
                }

                ballPosition = target;

                dummy.moveTo(ballPosition);
                if (!dummy.canReach(ballPosition)) {
                    return true;
                }

                ballPosition = dummy.hitBall();
                agentTurn = false;
            }
            else {
                agent.moveTo(ballPosition);
                if (!agent.canReach(ballPosition)) {
                    return false;
                }

                int squareId = agent.chooseSquare(dummy.position);
                Point target = agent.getTargetWithError(squareId);

                if (court.isOut(target)) {
                    return false;
                }

                ballPosition = target;
                agentTurn = true;
            }
        }
        return true;
    }

    bool playGame() {
        int agentScore = 0;
        int dummyScore = 0;
        bool agentServes = true;
        const int maxPoints = 20;

        for (int i = 0; i < maxPoints && agentScore < 4 && dummyScore < 4; i++) {
            bool agentWon = playRally(agentServes);

            if (agentWon) {
                agentScore++;
            }
            else {
                dummyScore++;
            }

            if (agentScore >= 4 && agentScore - dummyScore >= 2) {
                return true;
            }
            if (dummyScore >= 4 && dummyScore - agentScore >= 2) {
                return false;
            }

            agentServes = !agentServes;
        }
        return agentScore > dummyScore;
    }

    bool playMatch() {
        int agentWins = 0;
        int dummyWins = 0;

        for (int i = 0; i < 6; i++) {
            if (playGame()) {
                agentWins++;
            }
            else {
                dummyWins++;
            }

            if (agentWins >= 2) return true;
            if (dummyWins >= 2) return false;
        }
        return agentWins > dummyWins;
    }
};

void runExperiments() {
    vector<double> r_values = { 0.5, 1.0, 1.5, 2.0 };
    vector<double> l_values = { 0.5, 1.0, 1.5, 2.0 };
    vector<int> n_values = { 4, 9, 16, 25 };

    const int matchesPerConfig = 50;

    cout << "Результаты:" << endl;
    cout << "r\tl\tn\tВероятность победы" << endl;

    double fixed_l = 1.0;
    for (double r : r_values) {
        for (int n : n_values) {
            int wins = 0;
            for (int i = 0; i < matchesPerConfig; i++) {
                MatchSimulator simulator(r, fixed_l, n);
                if (simulator.playMatch()) {
                    wins++;
                }
            }
            double winRate = (double)wins / matchesPerConfig;
            cout << r << "\t" << fixed_l << "\t" << n << "\t" << winRate << endl;
        }
    }
}

int main() {
    setlocale(LC_ALL, "rus");
    runExperiments();
    return 0;
}