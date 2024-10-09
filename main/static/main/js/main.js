document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.exchange-form');
    const resultModal = document.getElementById('result-modal');
    const resultText = document.querySelector('.modal-title');
    const modalButton = document.querySelector('#modal-button')
    const modalP = document.getElementById('result-modal-p')
    const currencyInfoP = document.querySelector('.about-currency-info')
    const currencyName = document.getElementById('currency-name')
    const currencyData =
        document.getElementById('currency-data').getAttribute('data-json').trim();
    const parseCurrencyData = JSON.parse(currencyData)
    const emailInput = document.querySelector('.email-input')

    if (form) {
        form.addEventListener('submit', function (event) {
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
                        resultText.textContent = 'An error occurred during the calculation.';
                        resultModal.style.display = 'block';
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    resultText.textContent = 'An error occurred while sending the data.';
                    resultModal.style.display = 'block';
                });
        });

        modalButton.addEventListener('click', function () {
            resultModal.style.display = 'none'
        })

        const convertMoney = (currencyRate) => {
            return 1 / currencyRate
        }


        for (let i=0; i<parseCurrencyData.length;i++){
            if (currencyName.value === parseCurrencyData[i].currency__code)
            {
                currencyInfoP.textContent =
                    '1.000 ' + currencyName.value + ' = ' +
                    convertMoney(parseFloat(parseCurrencyData[i].latest_rate)).toFixed(3) + ' USD'
            }
        }

        currencyName.addEventListener('change', function () {
            let selectedCurrencyName = currencyName.value;
            let selectedCurrencyRate;
            console.log(selectedCurrencyName)
            for (let i=0; i<parseCurrencyData.length; i++){
                if (selectedCurrencyName === parseCurrencyData[i].currency__code){
                    selectedCurrencyRate = parseFloat(parseCurrencyData[i].latest_rate)
                }
            }
            currencyInfoP.textContent =
                '1.000 ' + selectedCurrencyName + ' = ' +
                convertMoney(selectedCurrencyRate).toFixed(3) + ' USD';
        })
    }

    emailInput.addEventListener('keypress', function (){
        emailInput.value = ''
    })

});