from flask import Flask, render_template, request
import rdflib


app = Flask(__name__, template_folder='templates')


graph = rdflib.Graph()
graph.parse("medic4.owl", format="xml")


namespaces = {"ex": "http://www.semanticweb.org/user1/ontologies/2025/8/med#"}


def get_all_drugs():
    qres = graph.query(
        """
        PREFIX ex: <http://www.semanticweb.org/user1/ontologies/2025/8/med#>
        SELECT ?drugName ?manufacturer ?form
        WHERE {
            ?drug a ex:Лекарство ;
                  ex:Название_лекарства ?drugName ;
                  ex:Производитель ?manufacturer ;
                  ex:ФормаВыпуска ?form .
        }
        ORDER BY ASC(?drugName)
        """,
        initNs=namespaces
    )

    drugs = []
    for row in qres:
        drugs.append({
            "drugName": str(row["drugName"]),
            "manufacturer": str(row["manufacturer"]),
            "form": str(row["form"])
        })
    return drugs

# Выборка всех клинических испытаний, связанных с лекарствами и заболеваниями
def get_clinical_trials():
    qres = graph.query(
        """
        PREFIX ex: <http://www.semanticweb.org/user1/ontologies/2025/8/med#>
       SELECT ?nazzab ?nazlek ?eff ?bez ?dan
	    WHERE { ?rez ex:Исследовалась ?zab.
		?zab ex:НазваниеЗаболевания ?nazzab.
		?rez ex:Исследовалось ?lek.
		?lek ex:Название_лекарства ?nazlek.
		?rez ex:ПоказательЭффективности ?eff.
		?rez ex:ПоказательБезопасности ?bez.
		?rez ex:ИсточникДанных ?dan.}
        """,
        initNs=namespaces
    )

    trials = []
    for row in qres:
        trials.append({
            "nazzab": str(row["nazzab"]),
            "nazlek": str(row["nazlek"]),
            "eff": str(row["eff"]),
            "bez": str(row["bez"]),
            "dan": str(row["dan"])
        })
    return trials




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/drugs', methods=['POST'])
def display_drugs():
    drugs = get_all_drugs()
    return render_template('drugs.html', drugs=drugs)


@app.route('/clinical_trials', methods=['POST'])
def display_clinical_trials():
    clinical_trials = get_clinical_trials()
    return render_template('clinical_trials.html', clinical_trials=clinical_trials)

if __name__ == '__main__':
    app.run(debug=True)
