function sendCommand(command) {
    fetch('/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'command=' + command,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggleButton');
    const statusElement = document.getElementById('status');

    toggleButton.addEventListener('change', function() {
        const status = this.checked ? 'ON' : 'OFF';
        statusElement.innerText = 'Auto: ' + status;

        // Send a POST request when the toggle button is toggled
        sendPostRequest(this.checked);
    });

    function sendPostRequest(isOn) {
        const url = '/mode';  // Replace with the actual endpoint URL
        const data = { isOn: isOn };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Handle any additional logic after successful POST
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle errors
        });
    }
});