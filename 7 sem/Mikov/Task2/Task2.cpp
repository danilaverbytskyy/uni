#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <random>
#include <algorithm>

using namespace std;

class Agent {
public:
    int id;
    set<int> target_patents;
    set<int> current_patents;
    int iterations;
    int communication_rounds;
    int patents_per_agent;

    Agent(int _id, int _patents_per_agent) : id(_id), iterations(0), communication_rounds(0), patents_per_agent(_patents_per_agent) {}

    bool has_collected_all() const {
        for (int patent : target_patents) {
            if (current_patents.find(patent) == current_patents.end()) {
                return false;
            }
        }
        return true;
    }

    int get_needed_patent() const {
        for (int patent : target_patents) {
            if (current_patents.find(patent) == current_patents.end()) {
                return patent;
            }
        }
        return -1;
    }

    int get_offered_patent(const Agent& other) const {
        for (int patent : other.target_patents) {
            if (other.current_patents.find(patent) == other.current_patents.end() &&
                current_patents.find(patent) != current_patents.end()) {
                return patent;
            }
        }
        return -1;
    }
};

class Simulation {
private:
    vector<Agent> agents;
    mt19937 rng;

public:
    Simulation(int num_agents, int total_patents) : rng(random_device{}()) {
        // Генерация случайного размера целевого набора для каждого агента (5-10)
        uniform_int_distribution<int> size_dist(5, 10);

        for (int i = 0; i < num_agents; ++i) {
            int patents_per_agent = size_dist(rng);
            agents.emplace_back(i, patents_per_agent);
        }

        cout << "Размеры целевых наборов агентов:\n";
        for (const auto& agent : agents) {
            cout << "Агент " << agent.id << ": " << agent.patents_per_agent << " патентов\n";
        }
        cout << endl;

        vector<int> all_patents(total_patents);
        for (int i = 0; i < total_patents; ++i) {
            all_patents[i] = i;
        }
        shuffle(all_patents.begin(), all_patents.end(), rng);

        int patent_index = 0;
        for (auto& agent : agents) {
            for (int j = 0; j < agent.patents_per_agent; ++j) {
                if (patent_index >= total_patents) {
                    patent_index = 0;
                    shuffle(all_patents.begin(), all_patents.end(), rng);
                }
                agent.target_patents.insert(all_patents[patent_index++]);
            }
        }

        set<int> all_target_patents;
        for (const auto& agent : agents) {
            all_target_patents.insert(agent.target_patents.begin(), agent.target_patents.end());
        }

        vector<int> pool(all_target_patents.begin(), all_target_patents.end());
        shuffle(pool.begin(), pool.end(), rng);

        int patents_per_agent_initial = max(1, (int)pool.size() / num_agents);
        int extra_patents = pool.size() % num_agents;

        patent_index = 0;
        for (auto& agent : agents) {
            int patents_to_give = patents_per_agent_initial + (extra_patents-- > 0 ? 1 : 0);
            for (int j = 0; j < patents_to_give && patent_index < pool.size(); ++j) {
                agent.current_patents.insert(pool[patent_index++]);
            }

            if (agent.current_patents.empty() && !pool.empty()) {
                agent.current_patents.insert(pool[0]);
            }
        }
    }

    void run() {
        uniform_int_distribution<int> agent_dist(0, agents.size() - 1);
        bool all_collected = false;
        int global_iteration = 0;

        cout << "Начало моделирования...\n";

        while (!all_collected) {
            all_collected = true;
            global_iteration++;

            for (auto& agent : agents) {
                if (agent.has_collected_all()) continue;

                all_collected = false;
                agent.iterations++;

                int other_id = agent_dist(rng);
                while (other_id == agent.id) {
                    other_id = agent_dist(rng);
                }

                Agent& other = agents[other_id];
                agent.communication_rounds++;
                other.communication_rounds++;

                int needed_patent = agent.get_needed_patent();
                if (needed_patent == -1) continue;

                if (other.current_patents.find(needed_patent) != other.current_patents.end()) {
                    if (other.has_collected_all()) {
                        agent.current_patents.insert(needed_patent);
                    }
                    else {
                        int offered_patent = agent.get_offered_patent(other);
                        if (offered_patent != -1) {
                            agent.current_patents.insert(needed_patent);
                            other.current_patents.insert(offered_patent);
                            agent.current_patents.erase(offered_patent);
                        }
                    }
                }
            }

            if (global_iteration > 10000) {
                cout << "Превышено максимальное количество итераций!\n";
                break;
            }
        }

        cout << "Моделирование завершено за " << global_iteration << " глобальных итераций\n\n";
    }

    void print_results() {
        cout << "Результаты моделирования:\n";
        cout << "Агент | Целевых патентов | Итераций | Раундов коммуникации\n";

        for (const auto& agent : agents) {
            cout << agent.id << "     | "
                << agent.target_patents.size() << "               | "
                << agent.iterations << "        | "
                << agent.communication_rounds << "\n";
        }
    }
};

int main() {
    setlocale(LC_ALL, "rus");

    int num_agents, total_patents;

    cout << "Введите количество агентов: ";
    cin >> num_agents;

    cout << "Введите общее количество патентов: ";
    cin >> total_patents;

    if (num_agents <= 0 || total_patents <= 0) {
        cout << "Ошибка: количество агентов и патентов должно быть положительным числом\n";
        return 1;
    }

    Simulation sim(num_agents, total_patents);
    sim.run();
    sim.print_results();

    return 0;
}