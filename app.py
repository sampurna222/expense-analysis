import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="Expense Analysis", layout="wide")
st.title("💳 Monthly Expense Analysis Dashboard")

# Initialize session state - store by month
if 'monthly_data' not in st.session_state:
    st.session_state.monthly_data = {}

# Helper function to get month key
def get_month_key(month, year):
    return f"{year}-{month:02d}"

# Manual Entry Section with Monthly Tracking
st.subheader("📊 Monthly Income, Budget & Expenses Tracker")

col1, col2 = st.columns([1, 1])

with col1:
    selected_month = st.selectbox("Select Month", range(1, 13), format_func=lambda x: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][x-1])

with col2:
    selected_year = st.number_input("Year", value=2026, min_value=2020, max_value=2030)

month_key = get_month_key(selected_month, selected_year)

# Initialize month data if not exists
if month_key not in st.session_state.monthly_data:
    st.session_state.monthly_data[month_key] = {
        'income': 0,
        'budget': 0,
        'expenses': 0,
        'expenses_by_category': {}
    }

month_data = st.session_state.monthly_data[month_key]

st.divider()

tab1, tab2 = st.tabs(["Add Income", "Add Expenses"])

with tab1:
    st.write(f"### 💵 Add Income for {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][selected_month-1]} {selected_year}")
    col1, col2 = st.columns(2)
    
    with col1:
        income_amount = st.number_input("Enter Income Amount", min_value=0.0, step=100.0, key=f"income_{month_key}")
        if st.button("Add Income", key=f"btn_income_{month_key}"):
            if income_amount > 0:
                st.session_state.monthly_data[month_key]['income'] += income_amount
                st.success(f"✅ Added Income: ${income_amount:,.2f}")
                st.rerun()
    
    with col2:
        budget_amount = st.number_input("Set Monthly Budget", min_value=0.0, step=100.0, key=f"budget_{month_key}")
        if st.button("Set Budget", key=f"btn_budget_{month_key}"):
            if budget_amount > 0:
                st.session_state.monthly_data[month_key]['budget'] = budget_amount
                st.success(f"✅ Budget Set: ${budget_amount:,.2f}")
                st.rerun()

with tab2:
    st.write(f"### 💸 Add Expense for {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][selected_month-1]} {selected_year}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        expense_category = st.selectbox("Category", [
            "Food & Dining",
            "Transport",
            "Shopping",
            "Entertainment",
            "Utilities",
            "Healthcare",
            "Education",
            "Other"
        ], key=f"cat_{month_key}")
    
    with col2:
        expense_amount = st.number_input("Amount", min_value=0.0, step=10.0, key=f"expense_{month_key}")
    
    with col3:
        if st.button("Add Expense", key=f"btn_expense_{month_key}"):
            if expense_amount > 0:
                st.session_state.monthly_data[month_key]['expenses'] += expense_amount
                if expense_category not in st.session_state.monthly_data[month_key]['expenses_by_category']:
                    st.session_state.monthly_data[month_key]['expenses_by_category'][expense_category] = 0
                st.session_state.monthly_data[month_key]['expenses_by_category'][expense_category] += expense_amount
                st.success(f"✅ Added {expense_category}: ${expense_amount:,.2f}")
                st.rerun()

st.divider()

# Financial Summary for Selected Month
st.subheader(f"📈 Financial Summary - {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][selected_month-1]} {selected_year}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Income", f"${month_data['income']:,.2f}")

with col2:
    st.metric("📉 Expenses", f"${month_data['expenses']:,.2f}")

with col3:
    savings = month_data['income'] - month_data['expenses']
    st.metric("💳 Savings", f"${savings:,.2f}")

with col4:
    if month_data['budget'] > 0:
        remaining = month_data['budget'] - month_data['expenses']
        st.metric("📊 Remaining Budget", f"${remaining:,.2f}")

st.divider()

# Budget Analysis & Insights
if month_data['budget'] > 0:
    st.subheader("🎯 Budget Analysis & Insights")
    
    spent_percentage = (month_data['expenses'] / month_data['budget'] * 100) if month_data['budget'] > 0 else 0
    remaining_budget = month_data['budget'] - month_data['expenses']
    
    # Progress bar
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(min(spent_percentage / 100, 1.0))
    with col2:
        st.write(f"{spent_percentage:.1f}%")
    
    # Insights
    if spent_percentage > 100:
        st.error(f"⚠️ OVERSPENT! You exceeded your budget by ${abs(remaining_budget):,.2f}")
    elif spent_percentage > 80:
        st.warning(f"⚡ Caution! You've spent {spent_percentage:.1f}% of your budget. Only ${remaining_budget:,.2f} left!")
    else:
        st.success(f"✅ Good! You have ${remaining_budget:,.2f} ({100-spent_percentage:.1f}%) of your budget remaining")
    
    # Category breakdown
    if month_data['expenses_by_category']:
        st.write("### Expenses by Category")
        
        cat_df = pd.DataFrame([
            {"Category": cat, "Amount": amt}
            for cat, amt in sorted(month_data['expenses_by_category'].items(), 
                                 key=lambda x: x[1], reverse=True)
        ])
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(cat_df["Category"], cat_df["Amount"], color="steelblue")
            ax.set_xlabel("Amount ($)")
            ax.set_title(f"Spending by Category - {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][selected_month-1]}")
            st.pyplot(fig)
        
        with col2:
            # Find overspent categories
            st.write("### Category Insights")
            for cat, amt in sorted(month_data['expenses_by_category'].items(), 
                                 key=lambda x: x[1], reverse=True):
                pct = (amt / month_data['expenses'] * 100) if month_data['expenses'] > 0 else 0
                st.write(f"• **{cat}**: ${amt:,.2f} ({pct:.1f}%)")
                
                # Highlight highest spending
                if pct > 30:
                    st.write(f"  ⚠️ This is your highest expense category!")

st.divider()

# Monthly Report
st.subheader("📊 Monthly Report Overview")

report_data = []
for key in sorted(st.session_state.monthly_data.keys()):
    year, month = key.split('-')
    data = st.session_state.monthly_data[key]
    month_name = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][int(month)-1]
    
    report_data.append({
        "Month": f"{month_name} {year}",
        "Income": f"${data['income']:,.2f}",
        "Budget": f"${data['budget']:,.2f}",
        "Expenses": f"${data['expenses']:,.2f}",
        "Savings": f"${data['income'] - data['expenses']:,.2f}"
    })

if report_data:
    report_df = pd.DataFrame(report_data)
    st.dataframe(report_df, use_container_width=True)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Income vs Expenses over months
        months_list = sorted(st.session_state.monthly_data.keys())
        incomes = [st.session_state.monthly_data[k]['income'] for k in months_list]
        expenses = [st.session_state.monthly_data[k]['expenses'] for k in months_list]
        month_labels = [k.split('-')[1] for k in months_list]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        x = np.arange(len(month_labels))
        width = 0.35
        ax.bar(x - width/2, incomes, width, label='Income', color='green', alpha=0.7)
        ax.bar(x + width/2, expenses, width, label='Expenses', color='red', alpha=0.7)
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Income vs Expenses by Month')
        ax.set_xticks(x)
        ax.set_xticklabels(month_labels)
        ax.legend()
        st.pyplot(fig)
    
    with col2:
        # Savings trend
        savings = [st.session_state.monthly_data[k]['income'] - st.session_state.monthly_data[k]['expenses'] for k in months_list]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(month_labels, savings, marker='o', color='blue', linewidth=2, markersize=8)
        ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax.set_xlabel('Month')
        ax.set_ylabel('Savings ($)')
        ax.set_title('Monthly Savings Trend')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

st.divider()

# Clear Data Button
if st.button("🔄 Reset All Data"):
    st.session_state.monthly_data = {}
    st.success("✅ All data cleared!")
    st.rerun()
