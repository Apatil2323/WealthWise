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


# for tax feature this is code

class TaxCalculatorForm(forms.Form):
    income = forms.DecimalField(label='Annual Income', max_digits=10, decimal_places=2)
    standard_deduction = forms.DecimalField(label='Standard Deduction', max_digits=10, decimal_places=2, required=False)
    investments = forms.DecimalField(label='Investments (e.g., 80C, etc.)', max_digits=10, decimal_places=2, required=False)

    def clean(self):
        cleaned_data = super().clean()
        income = cleaned_data.get("income")
        standard_deduction = cleaned_data.get("standard_deduction") or 0
        investments = cleaned_data.get("investments") or 0

        if income is not None and (standard_deduction < 0 or investments < 0):
            raise forms.ValidationError("Deductions and investments cannot be negative.")
