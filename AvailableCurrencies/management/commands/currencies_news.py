from django.core.management.base import BaseCommand
from AvailableCurrencies.models import CurrencyNews

from openai import OpenAI

from AvailableCurrencies.views import get_currency_from_database


class Command(BaseCommand):
    help = 'Fetches news about currencies from API'

    def handle(self, *args, **options):
        chosen_currencies_list = get_currency_from_database()
        client = OpenAI()
        responses_currencies_list = []
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Hey Currency assistance, you're a specialist in currency and cryptocurrencies."
                               "I want you to write me an interesting fact about the currencies I provide you with."
                               "The facts should be short and concise."
                               "They don't have to strictly relate to the  specific  currency;"
                               "they  can  be  tangential  topics.Please write st least 2 "
                               "sentences about each currency. "
                               "Here  's the example structure I' m  expecting:"
                               f"{chosen_currencies_list[0]}: "
                               f"{chosen_currencies_list[1]}:  "
                               f"{chosen_currencies_list[2]} :"
                },
                {
                    "role": "user",
                    "content": f"Hey chat, can you please write down some fun facts about {chosen_currencies_list} ?"
                               f"Please write only responses without any unnecessary text."
                }
            ],
            temperature=1,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        responses_currencies_list.append(response.choices[0].message.content)
        responses_string = responses_currencies_list[0]
        responses = responses_string.split("\n\n")
        currency_and_responses = zip(chosen_currencies_list, responses)
        currency_and_responses_list = list(currency_and_responses)

        for currency_and_response in currency_and_responses_list:
            currency_code = str(currency_and_response[0]).split('-')
            currency_name = currency_code[1].strip()
            description = currency_and_response[1]

            existing_currency, created = CurrencyNews.objects.update_or_create(
                currency_name=currency_name,
                defaults={
                    'currency_code': currency_code[0],
                    'currency_name': currency_name,
                    'description': description
                })

            if created:
                self.stdout.write(f'Fun fact about {existing_currency.currency_name} saved')