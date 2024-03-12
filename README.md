# Currency Exchange app

The Currency Exchange App is an intuitive and powerful tool
designed for those interested in the dynamic world of currency and cryptocurrency trading.
This web application offers a comprehensive suite of features
tailored to provide users with up-to-date financial information and interactive tools for currency analysis.


## Features
1. #### Currency and Cryptocurrency Rates:
   - Stay informed with the latest exchange rates for a wide range of currencies and cryptocurrencies, updated in real-time.
2. #### Rate Comparison:
   - Compare the current day's currency rates with the previous day, easily identifying which currencies have increased or decreased in value and by how much.
3. #### Five-Day Trend Analysis:
   - Explore detailed charts showcasing the five-day trend for any selected currency. This feature provides a quick glimpse into the currency's recent performance and market movements.
4. #### Cryptocurrency Insights:
   - Explore the world of cryptocurrencies with a feature that provides basic information about various digital currencies.
5. #### Wallet Functionality:
   - Create a personal wallet in the app, starting with an initial balance of 100 units of your chosen currency. Manage your funds, check account balances, and view transaction histories. The ability to conduct transaction


## Installation

1. #### Ensure Python 3.x is Installed:<br>
    Make sure you have Python 3.x installed on your system. You can check your Python version by running **python --version** in your terminal.
2. #### Clone the Repository:<br>
    Clone this repository to your local machine using the command:
   - git clone https://github.com/kTurek95/CurrencyExchange.git
3. #### Create and Activate a Virtual Environment:<br>
    Navigate to the project directory and create a virtual environment:
   - python -m venv venv

    Activate the virtual environment:
   - On macOS:
       - source venv/bin/activate
   - On Windows:
       - venv\scripts\activate
4. #### Setup Environment Variables:<br>
    Copy the **.env.example** file to a new file named **.env**:
   - cp .env.example .env
   Edit the **.env** file and add the required values. **DJANGO_SECRET_KEY** is necessary to run the script.
5. #### Install Dependencies:<br>
    Install the required packages using:
   - pip install -r requirements.txt
6. #### Database Migrations:<br>
    Perform database migrations with:
   - python manage.py makemigrations wallet
   - python manage.py migrate
7. #### Create a Superuser Account:<br>
    To access all functionalities, create a superuser account:
   - python manage.py createsuperuser
8. #### Load Initial Data:<br>
    Load the initial dataset into the database:
   - python manage.py loaddata AvailableCurrency.json CurrencyExchangeRate.json CryptoTokenCurrency.json CryptoTokenRate.json


## Important Note on Data Updates
This application relies on daily data updates for full functionality.
The fixtures included in the repository are historical and may not reflect the most recent data.
As a result, some features may not work as intended with the provided fixtures.


## Updating Data for Full Functionality
To experience the full functionality of the application, you may need to update the data in the database.
This can be done in one of the following ways:
1. **Manual Update**:
   - For detailed instructions, see the 'Manual Data Update for Full Functionality' section below.
2. **Visit the Live Application**:
   - For the most up-to-date experience, visit the live version of the application at https://django-app-currency-exchange-b5c4edfc43c0.herokuapp.com/.

Please note that without up-to-date data, some features may not function as expected.


## Manual Data Update for Full Functionality
To ensure full functionality of certain features,
such as 'Currency Rate Comparison' and currency detail access in the 'Available Currencies' section,
follow these manual update steps:

1. **Update the 'Currency Rate Comparison' Feature:**<br>
In the **AvailableCurrencies** application, locate the **compare_previous_day_rate** function in the **views.py** module. Make the following changes:

    - Change **today = date.today()** to **today = '2024-03-09'**
    Replace **yesterday_date = today - timedelta(days=1)** with **yesterday_date = '2024-03-08'**
    
    This will set the comparison dates to specific values, enabling the feature to function with the existing data.
2. **Enable Currency Detail Access in 'Available Currencies':**<br>
In the same **views.py** module, within the **currencies_details** function, comment out the following lines:

    - **five_days_ago = datetime.now() - timedelta(days=5)**
    - **api_date_updated__gt=five_days_ago**

   By doing this, you will bypass the time constraint and allow access to currency details with the current dataset.

Please note, these steps are required due to the nature of the data updating daily, and the provided fixtures containing historical data.

## Running the Application

After completing the installation and setup steps, you can start the application by running the following command in your terminal:<br>
- python manage.py runserver<br>

This will start the Django development server, and you should be able to access the application by navigating to http://127.0.0.1:8000/ in your web browser.


## Support

If you encounter any issues with my software, please reach out to me:

Email: k.turek1995@gmail.com


## Dependencies

- django
- django-extensions
- django-grappelli
- django-heroku
- django-import-export
- django-tinymce
- matplotlib
- Pillow
- python-dotenv
- tqdm
- neverbounce-sdk


## License

This project is licensed under the MIT License - 
[![Licencja MIT](https://img.shields.io/badge/Licencja-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
