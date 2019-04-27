import clearbit
from django.conf import settings
from pyhunter import PyHunter


def check_email(email):
    # Check the deliverability of a given email adress by emailhunter.co
    hunter = PyHunter(settings.EMAILHUNTER_API_KEY)
    hunter_result = hunter.email_verifier(email)

    if hunter_result and 'result' in hunter_result:
        return hunter_result['result']
    else:
        return 'unchecked'


def enrich_data(email):
    # Get additional data for email from Clearbit
    # As enrichment API restricted to 50 requests, I commented this code

    # clearbit.key = settings.CLEARBIT_API_KEY
    # lookup = clearbit.Enrichment.find(email=email, stream=True)

    # if lookup != None and 'person' in lookup:
    #     return lookup['person']
    # else:
    #     return {}

    return {}
