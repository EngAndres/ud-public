async function callMessage() {
    try {
        const response = await fetch('http://localhost/hello_ud');
        const data = await response.text();
        document.getElementById('result').textContent = data;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function callWebService() {
    try {
        const response = await fetch('http://localhost/data');
        const data = await response.json();
        
        let table = '<table>';
        table += '<tr><th>ID</th><th>Name</th><th>Description</th></tr>';
        
        data.forEach(item => {
            table += `<tr><td>${item.id}</td><td>${item.name}</td><td>${item.description}</td></tr>`;
        });
        
        table += '</table>';
        
        document.getElementById('result').innerHTML = table;
    } catch (error) {
        console.error('Error:', error);
    }
}