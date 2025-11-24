#include <iostream>
#include <queue>
#include <vector>
#include <algorithm>
#include <random>
#include <iomanip>

using namespace std;


enum EventType { ARRIVAL, DEPARTURE };


struct Event {
    double time;        
    EventType type;     
    int agent_id;       // ID агента (для DEPARTURE)
    double service_time; // Время обслуживания (для ARRIVAL)

    bool operator>(const Event& other) const {
        return time > other.time;
    }
};

class Agent {
public:
    int id;                 
    double current_load;    
    queue<double> q;        
    int served_count;       
    double total_time;      

    Agent(int id) : id(id), current_load(0), served_count(0), total_time(0) {}

    void add_client(double service_time) {
        q.push(service_time);
        current_load += service_time;
    }

    void finish_current_client() {
        if (q.empty()) return;
        double service_time = q.front();
        q.pop();
        current_load -= service_time;
        served_count++;
        total_time += service_time;
    }

    bool is_free() const {
        return q.empty();
    }
};

double generate_inter_arrival_time() {
    static random_device rd;
    static mt19937 gen(rd());
    static exponential_distribution<> dist(1.0); 
    return dist(gen);
}

double generate_service_time() {
    static random_device rd;
    static mt19937 gen(rd());
    static uniform_real_distribution<> dist(1.0, 10.0);
    return dist(gen);
}

int main() {
    setlocale(LC_ALL, "Rus");
    int n, m;
    cout << "Введите количество агентов (n): ";
    cin >> n;
    cout << "Введите количество клиентов (m): ";
    cin >> m;

    vector<Agent> agents;
    for (int i = 0; i < n; i++) {
        agents.emplace_back(i);
    }

    priority_queue<Event, vector<Event>, greater<Event>> event_queue;
    int generated_clients = 0;
    int total_served = 0;
    double current_time = 0;

    double first_arrival_time = generate_inter_arrival_time();
    double first_service_time = generate_service_time();
    event_queue.push({ first_arrival_time, ARRIVAL, -1, first_service_time });
    generated_clients++;

    while (total_served < m) {
        Event e = event_queue.top();
        event_queue.pop();
        current_time = e.time;

        if (e.type == ARRIVAL) {
            int selected_agent_id = 0;
            double min_load = agents[0].current_load;
            for (int i = 1; i < n; i++) {
                if (agents[i].current_load < min_load) {
                    min_load = agents[i].current_load;
                    selected_agent_id = i;
                }
                else if (agents[i].current_load == min_load && i < selected_agent_id) {
                    selected_agent_id = i;
                }
            }

            agents[selected_agent_id].add_client(e.service_time);

            if (agents[selected_agent_id].q.size() == 1) {
                event_queue.push({ current_time + e.service_time, DEPARTURE, selected_agent_id, 0 });
            }

            if (generated_clients < m) {
                double next_arrival_time = current_time + generate_inter_arrival_time();
                double next_service_time = generate_service_time();
                event_queue.push({ next_arrival_time, ARRIVAL, -1, next_service_time });
                generated_clients++;
            }
        }
        else {
            agents[e.agent_id].finish_current_client();
            total_served++;

            if (!agents[e.agent_id].q.empty()) {
                double next_service_time = agents[e.agent_id].q.front();
                event_queue.push({ current_time + next_service_time, DEPARTURE, e.agent_id, 0 });
            }
        }
    }

    vector<Agent> report_agents = agents;
    sort(report_agents.begin(), report_agents.end(), [](const Agent& a, const Agent& b) {
        if (a.served_count == b.served_count) {
            return a.total_time < b.total_time;
        }
        return a.served_count > b.served_count;
        });

    cout << "\nРезультаты работы системы:\n";
    for (const auto& agent : report_agents) {
        cout << "Agent" << agent.id << ": " << agent.served_count
            << " clients, " << fixed << setprecision(2) << agent.total_time << " time\n";
    }

    return 0;
}