from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.shortcuts import render, HttpResponse, redirect
from django.urls import path
from .forms import CampaignForm, RuleForm, MilestoneRulesForm, CampaignUpdateForm
import requests
from datetime import datetime
import json
from django.forms import formset_factory

# Register your models here.

class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()
        my_urls = [
            path('campaign_pg1/', self.admin_view(self.campaign_view_pg1), name="campaign-pg1"),
            path('campaign_pg2/', self.admin_view(self.campaign_view_pg2), name="campaign-pg2"),
            path('campaign/add', self.admin_view(self.campaign_add), name="campaign-add"),
            path('campaign/edit', self.admin_view(self.campaign_update), name="campaign-update"),
            # path('campaign/delete/<int:pk>', self.admin_view(self.campaign_delete), name="campaign-delete"),

            # path('campaign/<int:pk>', self.admin_view(self.campaign_update), name="campaign-update"),
        ]
        return my_urls + urls

    def campaign_view_pg1(self, request):
        if request.method == 'GET':
            r = requests.get("https://referralservice-staging-http.internal.cleartax.co/v0/campaigns")
            data = r.json()
            print(data)
            return TemplateResponse(request, "admin/campaign_1.html", {"data":data})

    def campaign_view_pg2(self, request):
        if request.method == 'GET':
            r = requests.get("https://referralservice-staging-http.internal.cleartax.co/v0/campaigns")
            data = r.json()
            print(data)
            return TemplateResponse(request, "admin/campaign_2.html", {"data":data})

    def campaign_add(self, request):
        form = CampaignForm()
        RuleFormSet = formset_factory(RuleForm)
        MilestoneFormSet = formset_factory(MilestoneRulesForm)
        if request.method == 'POST':
            # import ipdb; ipdb.set_trace()
            form = CampaignForm(request.POST)
            rule_formset = RuleFormSet(request.POST)
            milestone_formset = MilestoneFormSet(request.POST)
            if form.is_valid() and rule_formset.is_valid() and milestone_formset.is_valid():
                # import ipdb; ipdb.set_trace()
                # <QueryDict: {'csrfmiddlewaretoken': ['q9Ox6KtEWUxIFXm305KhGRlHcliXtIgc6AjjqjkhG7p791tKvILMXZh8yZdWJWSW'], 'consumer': ['FILING'], 'startDate': ['05/04/2019 16:28'], 'endDate': ['06/04/2019 16:28'], 'referreeCredits': ['50'], 'referrerCredits': ['50'], 'maxReferreeCredits': ['50'], 'maxReferrerCredits': ['50'], 'message': ['Hello'], 'kramerTemplateId': ['kt01'], 'paymentMode': ['PAYTM'], 'form-TOTAL_FORMS': ['1', '1'], 'form-INITIAL_FORMS': ['0', '0'], 'form-MIN_NUM_FORMS': ['0', '0'], 'form-MAX_NUM_FORMS': ['1000', '1000'], 'form-0-eventName': ['string'], 'form-0-operator': ['EQUAL'], 'form-0-value': ['0'], 'form-0-moperator': ['EQUAL'], 'form-0-mvalue': ['0'], 'form-0-mreferrerCredits': ['50']}>
                dat = {}
                dat["consumer"] = form.cleaned_data["consumer"]
                dat["startDate"] = self.datetime_to_epoch(form.cleaned_data["startDate"])
                dat["endDate"] = self.datetime_to_epoch(form.cleaned_data["endDate"])
                dat["referreeCredits"] = form.cleaned_data["referreeCredits"]
                dat["referrerCredits"] = form.cleaned_data["referrerCredits"]
                dat["maxReferreeCredits"] = form.cleaned_data["maxReferreeCredits"]
                dat["maxReferrerCredits"] = form.cleaned_data["maxReferrerCredits"]
                dat["message"] = form.cleaned_data["message"]
                dat["kramerTemplateId"] = form.cleaned_data["kramerTemplateId"]
                dat["paymentMode"] = form.cleaned_data["paymentMode"]
                arrRules = rule_formset.cleaned_data
                arrMilestoneRules = milestone_formset.cleaned_data
                dat["eventRules"] = arrRules
                dat["milestoneRules"] = arrMilestoneRules
                for rule in rule_formset:
                    print(rule.cleaned_data)
                res = requests.post("https://referralservice-staging-http.internal.cleartax.co/v0/campaigns", data=request.POST)
                if res.status_code == 201 or res.status_code == 200:
                    messages.success(request, 'Success!')
                    return redirect("admin:campaign-pg1")
                else:
                    messages.error(request, 'Submission Failed.')
        else:
            rule_formset = RuleFormSet()
            milestone_formset = MilestoneFormSet()
            return TemplateResponse(request, "admin/campaign_add.html", {"form":form, "rule_formset": rule_formset, "milestone_formset": milestone_formset})

    @staticmethod
    def datetime_to_epoch(datetime_str):

        datetime_object = datetime.strptime(str(datetime_str.strftime('%d/%m/%Y %H:%M')), '%d/%m/%Y %H:%M')
        timestamp = datetime_object.timestamp()
        return timestamp

    def campaign_update(self, request):
        import ipdb; ipdb.set_trace()

        if request.method == 'GET':
            res = requests.get("https://referralservice-staging-http.internal.cleartax.co/v0/campaigns")
            data = res.json()
            # print(data)
            form = CampaignUpdateForm(initial=data)
            return render(request, "admin/campaign_update.html", {'form': form})
        
        elif request.method == 'POST':
            form = CampaignUpdateForm(request.POST)
            if form.is_valid():
                res = requests.put("https://referralservice-staging-http.internal.cleartax.co/v0/campaigns", data=request.POST)
                if res.status_code == 200:
                    messages.success(request, 'Update Success!')
                    return redirect("admin:campaign")
                else:
                    messages.error(request, 'Update Failed.')

    # def campaign_delete(self, request, pk):
    #     if request.method == 'POST':
    #         r = requests.delete("https://referralservice-staging-http.internal.cleartax.co/v0/campaigns")
    #     return redirect("admin:campaign")
   
    
admin_site = MyAdminSite()