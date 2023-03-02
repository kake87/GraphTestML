from flask import Flask, request, render_template
from neo4j import GraphDatabase


app = Flask(__name__)
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', '31337'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        first_name1 = request.form.get('first_name1')
        last_name1 = request.form.get('last_name1')
        middle_name1 = request.form.get('middle_name1')

        first_name2 = request.form.get('first_name2')
        last_name2 = request.form.get('last_name2')
        middle_name2 = request.form.get('middle_name2')

        person1 = f'{first_name1} {last_name1} {middle_name1}'
        person2 = f'{first_name2} {last_name2} {middle_name2}'

        with driver.session() as session:
            session.run(
                "MERGE (p1:Person {name: '" + person1 + "'}) MERGE (p2:Person {name: '" + person2 + "'}) MERGE (p1)-[:CONNECTED]->(p2)")
            query = session.run('MATCH (p1:Person)-[:CONNECTED]-(p2:Person) RETURN p1, p2 as JSON')
            print(query.values)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()