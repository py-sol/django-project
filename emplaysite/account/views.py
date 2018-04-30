from django.shortcuts import render

from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from .models import Account, AccountRisk

def index(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello world.")

def account_details(request, account_id):
    '''
        By the view of this page, I am interpreting that this is meant for a company
        and by account we meant the customer of that particular company. 

        Given a account_id, I have printed all the details related to that account id
        and associated child account along with the account risk related to that account.
    '''
    try:
        account_risk_obj = AccountRisk.objects.filter(account_id=account_id)[0]
    except Account.DoesNotExist:
        raise Http404("Account does not exist")
    template = loader.get_template('account_details.html')

    # get the account details for printing the detials
    account_details = get_account_details(account_id)
    account_details.update({
        "account_name": account_risk_obj.account_name,
        "customer_name": account_risk_obj.customer_name,
        "account_risk": account_risk_obj.get_account_risk()
    })
    return HttpResponse(template.render(account_details, request))


def get_account_details(account_id):

    # retrive the no of child accounts for a given account_id from the account table
    child_account_count = len(Account.objects.filter(account_id=account_id))

    # count of the child account won for a given account_id from the account table
    child_account_won = len(Account.objects.filter(account_id=account_id, stage='Won'))

    # Count the number of distinct child_accounts with potential=’HP’
    high_potential_details = Account.objects.raw('''
        SELECT id, account_child_id
        FROM account_account
        WHERE potential="HP" and account_id = %s''', [account_id])
    high_potential_count = len([p.account_child_id for p in high_potential_details])
    
    print (high_potential_count)

    # Count the number of distinct child accounts with pipeline=’HP’
    high_pipeline_count = len(Account.objects.filter(account_id=account_id, pipeline='HP').distinct('account_child_id'))

    return {
        "child_account_count": child_account_count,
        "child_account_won": child_account_won,
        "high_pipeline_count": high_pipeline_count,
        "high_potential_count": high_potential_count
    }



