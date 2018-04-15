from django.db import models

from django.db import models

class Account(models.Model):
    '''
        account class which will store the account related data
    '''
    account_id = models.IntegerField(default=0)
    account_child_id = models.IntegerField(default=0)
    potential = models.CharField(max_length=250)
    pipeline = models.CharField(max_length=250)
    stage = models.CharField(max_length=250)

    # return the readable obejct representation
    def __str__(self):
        return str(self.account_id)


class AccountRisk(models.Model):
    '''
        measure the risk related to the account
    '''
    account_id = models.IntegerField(default=0)
    account_name = models.CharField(max_length=250)
    customer_name = models.CharField(max_length=250)
    account_risk = models.TextField()

    # return the readable obejct representation
    def __str__(self):
        return str(self.account_id) + " " + self.account_name

    # return the account details in the desired format
    def get_account_risk(self):
        risk_details = self.account_risk.split("@")
        return risk_details