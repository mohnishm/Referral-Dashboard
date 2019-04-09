from django import forms


class CampaignForm(forms.Form):
    consumer = forms.CharField(label="Consumer", max_length=200)
    startDate = forms.DateTimeField(label="Start Date",
        input_formats=['%d/%m/%Y %H:%M'])
    endDate = forms.DateTimeField(label="End Date",
        input_formats=['%d/%m/%Y %H:%M'])
    referreeCredits = forms.IntegerField(label="Referree Credits")
    referrerCredits = forms.IntegerField(label="Referrer Credits")
    maxReferreeCredits = forms.IntegerField(label="Max Referree Credits")
    maxReferrerCredits = forms.IntegerField(label="Max Referrer Credits")
    message = forms.CharField(label="Message", max_length=200)
    kramerTemplateId = forms.CharField(label="Kramer Template ID", max_length=200)
    paymentMode = forms.ChoiceField(label="Payment Mode", choices=[("PAYTM","PAYTM")])

class RuleForm(forms.Form):
    eventName = forms.CharField(label="Event Name", max_length=200)
    operator = forms.ChoiceField(label="Operator", choices=[("EQUAL","EQUAL"), ("EVERY","EVERY")])
    value = forms.IntegerField(label="Value")

class MilestoneRulesForm(forms.Form):
    operator = forms.ChoiceField(label="Operator", choices=[("EQUAL","EQUAL"), ("EVERY","EVERY")])
    value = forms.IntegerField(label="Value")
    referrerCredits = forms.IntegerField(label="Referrer Credits")

class CampaignUpdateForm(forms.Form):
    campaignId = forms.IntegerField()
    referreeCredits = forms.IntegerField()
    referrerCredits = forms.IntegerField()
    maxReferreeCredits = forms.IntegerField()
    maxReferrerCredits = forms.IntegerField()
    message = forms.CharField(max_length=200)
    kramerTemplateId = forms.CharField(max_length=200)
    eventName = forms.CharField(max_length=200)
    operator = forms.CharField(max_length=200)
    value = forms.IntegerField()
    mOperator = forms.CharField(max_length=200)
    mValue = forms.IntegerField()
    mReferrerCredits = forms.IntegerField()
    