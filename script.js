fetch('http://127.0.0.1:8000/orcamentos/?format=json')
    .then(results => results.json())
    .then(console.log)