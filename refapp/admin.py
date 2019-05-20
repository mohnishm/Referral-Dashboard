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
            path('campaign/', self.admin_view(self.campaign_view), name="campaign-view"),
            path('campaign/add', self.admin_view(self.campaign_add), name="campaign-add"),
            path('campaign/edit/<int:pk>', self.admin_view(self.campaign_update), name="campaign-update"),
            # path('campaign/delete/<int:pk>', self.admin_view(self.campaign_delete), name="campaign-delete"),
        ]
        return my_urls + urls

    def campaign_view(self, request):
        if request.method == 'GET':
            r = requests.get("https://example.com")
            data = r.json()
            print(data)
            return TemplateResponse(request, "admin/campaign.html", {"data":data})


    def campaign_add(self, request):
        form = CampaignForm()
        RuleFormSet = formset_factory(RuleForm)
        MilestoneFormSet = formset_factory(MilestoneRulesForm)
        if request.method == 'POST':
            # import ipdb; ipdb.set_trace()
            form = CampaignForm(request.POST)
            rule_formset = RuleFormSet(request.POST, prefix='rules')
            milestone_formset = MilestoneFormSet(request.POST, prefix='milestones')
            if form.is_valid() and rule_formset.is_valid() and milestone_formset.is_valid():
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
                    import ipdb; ipdb.set_trace()
                    print(rule_formset.cleaned_data)
                    print(milestone_formset.cleaned_data)
                    print (dat)
                    res = requests.post("https://example.com", data=json.dumps(dat), headers={'content-type': 'application/json'})
                    if res.status_code == 201 or res.status_code == 200:
                        # import ipdb; ipdb.set_trace()
                        messages.success(request, 'Success!')
                        return redirect("admin:campaign-view")
                    else:
                        messages.error(request, 'Submission Failed.')
                        return redirect("admin:campaign-add")
        else:
            rule_formset = RuleFormSet(prefix="rules")
            milestone_formset = MilestoneFormSet(prefix="milestones")
        return TemplateResponse(request, "admin/campaign_add.html", {"form":form, "rule_formset": rule_formset, "milestone_formset": milestone_formset})

    @staticmethod
    def datetime_to_epoch(datetime_str):

        datetime_object = datetime.strptime(str(datetime_str.strftime('%d/%m/%Y %H:%M')), '%d/%m/%Y %H:%M')
        timestamp = datetime_object.timestamp()
        return timestamp

    def campaign_update(self, request, pk):
        if request.method == 'GET':
            res = requests.get("https://example.com")
            data = res.json()
            # print (data)
            for dt in data:
                if dt["campaignId"] == pk:
                    RuleFormSet = formset_factory(RuleForm, extra=len(dt["eventRules"])-1)
                    MilestoneFormSet = formset_factory(MilestoneRulesForm, extra=len(dt["milestoneRules"])-1)
                    # print(data)
                    dat = {
                    "referreeCredits": dt["referreeCredits"],
                    "referrerCredits": dt["referrerCredits"],
                    "maxReferreeCredits": dt["maxReferreeCredits"],
                    "maxReferrerCredits": dt["maxReferrerCredits"],
                    "message": dt["message"],
                    "kramerTemplateId": dt["kramerTemplateId"],
                    }
                    print(dt["eventRules"])
                    form = CampaignUpdateForm(initial=dat)
                    rule_formset = RuleFormSet(initial= [{'eventName':x["eventName"], 'operator':x["operator"], 'value':x["value"]} for x in dt["eventRules"]],prefix='rules')
                    milestone_formset = MilestoneFormSet(initial= [{'operator':x["operator"], 'value':x["value"], 'referrerCredits':x["referrerCredits"]} for x in dt["milestoneRules"]], prefix='milestones')
                    return render(request, "admin/campaign_update.html", {'form': form,  "rule_formset": rule_formset, "milestone_formset": milestone_formset})
        
        elif request.method == 'POST':
            form = CampaignUpdateForm(request.POST)
            RuleFormSet = formset_factory(RuleForm)
            MilestoneFormSet = formset_factory(MilestoneRulesForm)
            rule_formset = RuleFormSet(request.POST, prefix='rules')
            milestone_formset = MilestoneFormSet(request.POST, prefix='milestones')
            if form.is_valid() and rule_formset.is_valid() and milestone_formset.is_valid():
                dat = {}
                dat["referreeCredits"] = form.cleaned_data["referreeCredits"]
                dat["referrerCredits"] = form.cleaned_data["referrerCredits"]
                dat["maxReferreeCredits"] = form.cleaned_data["maxReferreeCredits"]
                dat["maxReferrerCredits"] = form.cleaned_data["maxReferrerCredits"]
                dat["message"] = form.cleaned_data["message"]
                dat["kramerTemplateId"] = form.cleaned_data["kramerTemplateId"]
                arrRules = rule_formset.cleaned_data
                arrMilestoneRules = milestone_formset.cleaned_data
                dat["eventRules"] = arrRules
                dat["milestoneRules"] = arrMilestoneRules
                # import ipdb; ipdb.set_trace()
                res = requests.put("https://example.com/{id}".format(id=pk), data=json.dumps(dat), headers={'content-type': 'application/json'})
                if res.status_code == 201 or res.status_code == 200:
                    messages.success(request, 'Update Success!')
                    return redirect("admin:campaign-view")
                else:
                    messages.error(request, 'Update Failed!')
                    return redirect("admin:campaign-update")

    # def campaign_delete(self, request, pk):
    #     if request.method == 'POST':
    #         r = requests.delete("https://referralservice-staging-http.internal.cleartax.co/v0/campaigns")
    #     return redirect("admin:campaign")
   
    
admin_site = MyAdminSite()
