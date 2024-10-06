from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import InvestmentForm
from .forms import TaxCalculatorForm
from decimal import Decimal


# Home page view
def home(request):
    return render(request, 'index.html')

# Create your views here.
def index(request):
  return render(request, 'index.html')
  #return HttpResponse("This is AP and u r on homepage")

def about(request):
  return render(request, 'about.html')

def services(request):
  return render(request, 'services.html')

def contact(request):
  return render(request, 'contact.html')

# Investment logic
def investment_plan(request):
    form = InvestmentForm(request.POST or None)
    if form.is_valid():
        age = form.cleaned_data['age']
        income = form.cleaned_data['income']
        risk_profile = form.cleaned_data['risk_profile']
        time_horizon = form.cleaned_data['time_horizon']
        investment_type = form.cleaned_data['investment_type']
        amount = form.cleaned_data['amount']

        # Determine asset allocation based on investment type and risk profile
        allocation, recommendations = adjust_allocation_based_on_risk(investment_type, risk_profile)
        total_future_value = calculate_future_value(amount, 12, time_horizon, investment_type)

        # Calculate future values for each asset type
        future_values = {}
        for asset, percentage in allocation.items():
            asset_amount = (percentage * total_future_value) / 100
            future_values[asset] = asset_amount

        # Prepare data for chart
        chart_data = {
            'labels': list(allocation.keys()),
            'data': list(allocation.values()),
        }

        return render(request, 'investment_result.html', {
            'form': form,
            'allocation': allocation,
            'future_values': future_values,
            'total_future_value': total_future_value,
            'investment_type': investment_type,
            'time_horizon': time_horizon,
            'risk_profile': risk_profile,
            'recommendations': recommendations,
            'chart_data': chart_data,
        })

    return render(request, 'investment_form.html', {'form': form})
from decimal import Decimal

def calculate_future_value(amount, interest_rate, duration, investment_type):
    annual_rate = Decimal(interest_rate) / Decimal(100)  # Ensure Decimal type
    if investment_type == 'sip':
        monthly_rate = annual_rate / Decimal(12)
        months = duration * 12
        # Future value for SIP using the formula
        future_value = amount * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    else:  # lump sum
        # Future value for Lump Sum using the formula
        future_value = amount * ((1 + annual_rate) ** duration)
    return future_value


# Function to adjust allocation and provide recommendations based on risk profile
def adjust_allocation_based_on_risk(investment_type, risk_profile):
    allocations = {
        'sip': {
            'conservative': {'large_cap': 60, 'etf': 40},
            'moderate': {'large_cap': 40, 'midcap': 30, 'etf': 30},
            'aggressive': {'midcap': 30, 'small_cap': 40, 'etf': 30},
        },
        'lump_sum_equity': {
            'conservative': {'large_cap': 60, 'etf': 40},
            'moderate': {'large_cap': 40, 'midcap': 30, 'etf': 30},
            'aggressive': {'midcap': 30, 'small_cap': 40, 'etf': 30},
        },
        'lump_sum_diversified': {
            'conservative': {'stocks': 20, 'bonds': 50, 'gold': 20, 'etfs': 10},
            'moderate': {'stocks': 40, 'bonds': 30, 'gold': 20, 'etfs': 10},
            'aggressive': {'stocks': 60, 'bonds': 20, 'gold': 10, 'etfs': 10},
        },
    }

    recommendations = {
        'sip': {
            'conservative': ['Large Cap Funds', 'Nifty Bees ETF'],
            'moderate': ['Large Cap Funds', 'Mid Cap Funds', 'Junior Bees ETF'],
            'aggressive': ['Mid Cap Funds', 'Small Cap Funds', 'BSE 500 ETF'],
        },
        'lump_sum_equity': {
            'conservative': ['Large Cap Funds', 'Nifty Bees ETF'],
            'moderate': ['Large Cap Funds', 'Mid Cap Funds', 'Junior Bees ETF'],
            'aggressive': ['Mid Cap Funds', 'Small Cap Funds', 'BSE 500 ETF'],
        },
        'lump_sum_diversified': {
            'conservative': ['Gold Bees ETF', 'Bond Funds'],
            'moderate': ['Bond Funds', 'Gold ETFs'],
            'aggressive': ['Gold ETFs', 'Equity ETFs'],
        },
    }

    return allocations[investment_type][risk_profile], recommendations[investment_type][risk_profile]

# Sample growth rates for asset classes
ASSET_GROWTH_RATES = {
    'stocks': 0.12,    # 8% annual growth
    'bonds': 0.05,     # 4% annual growth
    'gold': 0.03,      # 3% annual growth
    'etfs': 0.10,      # 6% annual growth
}


#functions for tax feature
def calculate_old_regime_tax(taxable_income):
    # Ensure that all calculations use Decimal types
    basic_exemption_limit = Decimal('250000')
    lower_limit = Decimal('500000')
    upper_limit = Decimal('1000000')
    
    # Calculate tax based on the old regime slabs
    if taxable_income <= basic_exemption_limit:
        return Decimal('0')  # No tax
    elif taxable_income <= lower_limit:
        tax = (taxable_income - basic_exemption_limit) * Decimal('0.05')
    elif taxable_income <= upper_limit:
        tax = (lower_limit - basic_exemption_limit) * Decimal('0.05') + (taxable_income - lower_limit) * Decimal('0.2')
    else:
        tax = (lower_limit - basic_exemption_limit) * Decimal('0.05') + (upper_limit - lower_limit) * Decimal('0.2') + (taxable_income - upper_limit) * Decimal('0.3')

    return tax



def calculate_new_regime_tax(taxable_income):
    # Ensure that all calculations use Decimal types
    basic_exemption_limit = Decimal('250000')
    first_slab_limit = Decimal('500000')
    second_slab_limit = Decimal('750000')
    third_slab_limit = Decimal('1000000')

    # Calculate tax based on the new regime slabs
    if taxable_income <= basic_exemption_limit:
        return Decimal('0')  # No tax
    elif taxable_income <= first_slab_limit:
        tax = (taxable_income - basic_exemption_limit) * Decimal('0.05')
    elif taxable_income <= second_slab_limit:
        tax = (first_slab_limit - basic_exemption_limit) * Decimal('0.05') + (taxable_income - first_slab_limit) * Decimal('0.1')
    elif taxable_income <= third_slab_limit:
        tax = (first_slab_limit - basic_exemption_limit) * Decimal('0.05') + \
              (second_slab_limit - first_slab_limit) * Decimal('0.1') + \
              (taxable_income - second_slab_limit) * Decimal('0.15')
    else:
        tax = (first_slab_limit - basic_exemption_limit) * Decimal('0.05') + \
              (second_slab_limit - first_slab_limit) * Decimal('0.1') + \
              (third_slab_limit - second_slab_limit) * Decimal('0.15') + \
              (taxable_income - third_slab_limit) * Decimal('0.3')

    return tax

def tax_calculator(request):
    result = None
    form = TaxCalculatorForm(request.POST or None)

    if form.is_valid():
        income = form.cleaned_data['income']
        standard_deduction = form.cleaned_data['standard_deduction'] or 0
        investments = form.cleaned_data['investments'] or 0

        # Calculate taxable income
        taxable_income = income - standard_deduction - investments

        # Calculate tax for both regimes
        old_regime_tax = calculate_old_regime_tax(taxable_income)
        new_regime_tax = calculate_new_regime_tax(taxable_income)

        # Prepare the result to display
        result = {
            'taxable_income': taxable_income,
            'income': income,
            'standard_deduction': standard_deduction,
            'investments': investments,
            'old_regime_tax': old_regime_tax,
            'new_regime_tax': new_regime_tax,
        }

    return render(request, 'tax_calculator.html', {'form': form, 'result': result})
