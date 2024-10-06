from django import forms

class InvestmentForm(forms.Form):
    INVESTMENT_CHOICES = [
        ('sip', 'SIP (Systematic Investment Plan)'),
        ('lump_sum_equity', 'Lump Sum Investment in Equity'),
        ('lump_sum_diversified', 'Lump Sum Investment with Diversified Portfolio'),
    ]

    RISK_PROFILE_CHOICES = [
        ('conservative', 'Conservative'),
        ('moderate', 'Moderate'),
        ('aggressive', 'Aggressive'),
    ]

    age = forms.IntegerField(label='Age', min_value=0)
    income = forms.DecimalField(label='Monthly Income', min_value=0)
    risk_profile = forms.ChoiceField(label='Risk Profile', choices=RISK_PROFILE_CHOICES)
    time_horizon = forms.IntegerField(label='Time Horizon (in years)', min_value=1)
    investment_type = forms.ChoiceField(label='Investment Type', choices=INVESTMENT_CHOICES)
    amount = forms.DecimalField(label='Investment Amount', min_value=0)
