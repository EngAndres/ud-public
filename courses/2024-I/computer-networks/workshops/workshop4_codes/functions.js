function callPython() {
    fetch('http://193.168.100.201/healthcheck')
        .then(response => response.text())
        .then(data => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerText = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function callJavaScript() {
    fetch('http://193.168.100.202/healthcheck')
        .then(response => response.text())
        .then(data => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerText = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}