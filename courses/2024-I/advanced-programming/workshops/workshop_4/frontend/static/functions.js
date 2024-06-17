let URL_BASE = "http://localhost:8080"

async function callMessage() {
    try {
        const response = await fetch(URL_BASE + '/hello_ud');
        const data = await response.text();
        document.getElementById('result').textContent = data;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function callTable() {
    try {
        const response = await fetch(URL_BASE + '/products');
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

async function addProduct() {
    let form = "<form id='form_product'>";
    form += "<label for='txtName' id='lblName'>Name:</label>";
    form += "<input type='text' id='txtName'><br>";
    form += "<label for='txtDescription' id='lblDescription'>Description:</label>";
    form += "<textarea id='txtDescription' rows='3'></textarea><br>";
    form += "<button type='button' onclick='createProduct()'>Send to DB</button>";
    form += "</form>"

    document.getElementById('result').innerHTML = form;
}

async function createProduct() {
    let data = {
        name: document.getElementById('txtName').value,
        description: document.getElementById('txtDescription').value
    }
    console.log(data)
    
    let url_post = URL_BASE + '/products/add'

    try {
        const response = await fetch(url_post, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:5500',
                "Access-Control-Allow-Methods": "POST"
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        document.getElementById('result').textContent = result.message;
    } catch (error) {
        console.error('Error:', error);
    }
}