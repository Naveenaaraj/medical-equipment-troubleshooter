function fetchErrors() {
    const product = document.getElementById('product').value;
    axios.post('/get_errors', { product })
        .then(response => {
            const errorDropdown = document.getElementById('error');
            errorDropdown.innerHTML = '<option>Select Error</option>';
            response.data.forEach(error => {
                errorDropdown.innerHTML += `<option>${error}</option>`;
            });
        });
}

function fetchSolution() {
    const product = document.getElementById('product').value;
    const error = document.getElementById('error').value;
    axios.post('/get_solution', { product, error })
        .then(response => {
            document.getElementById('solutionBox').innerText = "Solution: " + response.data;
        });
}
