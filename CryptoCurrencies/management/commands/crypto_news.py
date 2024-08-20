from django.core.management.base import BaseCommand
from openai import OpenAI

from CryptoCurrencies.models import CryptoNews
from CryptoCurrencies.views import get_crypto_from_database


class Command(BaseCommand):
    def handle(self, *args, **options):
        chosen_crypto_list = get_crypto_from_database()
        client = OpenAI()
        responses_crypto_list = []
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Hey Currency assistance, you're a specialist in currency and cryptocurrencies."
                               "I want you to write me an interesting fact about the currencies I provide you with."
                               "The facts should be short and concise."
                               "They don't have to strictly relate to the  specific  currency;"
                               "they  can  be  tangential  topics."
                               "Please write st least 2 sentences about each Crypto currency. "
                               "Here  's the example structure I' m  expecting:"
                               f"{chosen_crypto_list[0]}: "
                               f"{chosen_crypto_list[1]}:  "
                               f"{chosen_crypto_list[2]} :"
                },
                {
                    "role": "user",
                    "content": f"Hey chat, can you please write down some fun facts about {chosen_crypto_list} ?"
                               f"Please write only responses without any unnecessary text."
                }
            ],
            temperature=1,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        responses_crypto_list.append(response.choices[0].message.content)
        responses_string = responses_crypto_list[0]
        responses = responses_string.split("\n\n")
        crypto_and_responses = zip(chosen_crypto_list, responses)
        crypto_and_responses_list = list(crypto_and_responses)

        for crypto, description in crypto_and_responses_list:
            crypto_name = crypto
            description = description

            existing_currency, created = CryptoNews.objects.update_or_create(
                crypto_name=crypto_name,
                defaults={
                    'crypto_name': crypto_name,
                    'description': description
                }
            )

            if created:
                self.stdout.write(f'Fun fact about {existing_currency.crypto_name} saved')
