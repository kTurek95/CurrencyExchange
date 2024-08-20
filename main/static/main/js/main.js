document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.exchange-form');
    const resultModal = document.getElementById('result-modal');
    const resultText = document.querySelector('.modal-title');
    const modalButton = document.querySelector('#modal-button')
    const modalP = document.getElementById('result-modal-p')

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data !== undefined) {
                const result = data.result
                const currencyName = data.currency_name
                const currencyRate = data.rate
                resultText.textContent = `You will receive ${result}$`;
                modalP.textContent = `The exchange rate for ${currencyName} was ${data.rate}`
                resultModal.style.display = 'block';
            } else {
                resultText.textContent = 'Wystąpił błąd podczas obliczania.';
                resultModal.style.display = 'block';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            resultText.textContent = 'Wystąpił błąd podczas wysyłania danych.';
            resultModal.style.display = 'block';
        });
    });

    modalButton.addEventListener('click', function()
    {
        resultModal.style.display = 'none'
    })
});