import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Payment Analytics Dashboard", layout="wide")

# Title
st.title("Payment Analytics Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("realistic_payment_data.csv", parse_dates=['timestamp'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
methods = st.sidebar.multiselect("Payment Methods", options=df['method'].dropna().unique(), default=df['method'].dropna().unique())
banks = st.sidebar.multiselect("Banks", options=df['bank'].dropna().unique(), default=df['bank'].dropna().unique())
wallets = st.sidebar.multiselect("Wallets", options=df['wallet'].dropna().unique(), default=df['wallet'].dropna().unique())
status_filter = st.sidebar.multiselect("Status", options=df['status'].unique(), default=df['status'].unique())

# Apply filters
filtered_df = df[
    (df['method'].isin(methods)) &
    ((df['bank'].isin(banks)) | df['bank'].isna()) &
    ((df['wallet'].isin(wallets)) | df['wallet'].isna()) &
    (df['status'].isin(status_filter))
]

st.subheader("Transactions Overview")
st.dataframe(filtered_df)

# Charts
st.subheader("Payment Method Distribution")
method_counts = filtered_df['method'].value_counts().reset_index()
method_counts.columns = ['method', 'count']
fig1 = px.bar(method_counts, x='method', y='count', title="Payment Methods", width=700, height=400)
st.plotly_chart(fig1)

st.subheader("Bank Distribution")
bank_counts = filtered_df['bank'].dropna().value_counts().reset_index()
bank_counts.columns = ['bank', 'count']
fig2 = px.bar(bank_counts, x='bank', y='count', title="Banks Used", width=700, height=400)
st.plotly_chart(fig2)

st.subheader("Wallet Distribution")
wallet_counts = filtered_df['wallet'].dropna().value_counts().reset_index()
wallet_counts.columns = ['wallet', 'count']
fig3 = px.bar(wallet_counts, x='wallet', y='count', title="Wallets Used", width=700, height=400)
st.plotly_chart(fig3)

st.subheader("Transaction Status")
status_counts = filtered_df['status'].value_counts().reset_index()
status_counts.columns = ['status', 'count']
fig4 = px.pie(status_counts, names='status', values='count', title="Transaction Status")
st.plotly_chart(fig4)

st.subheader("Failure Reasons")
error_counts = filtered_df['error_reason'].dropna().value_counts().reset_index()
if not error_counts.empty:
    error_counts.columns = ['error_reason', 'count']
    fig5 = px.bar(error_counts, x='error_reason', y='count', title="Failure Reasons", width=700, height=400)
    st.plotly_chart(fig5)
else:
    st.write("No failed transactions in selected filters.")

st.subheader("Transaction Amount Over Time")
fig6 = px.line(filtered_df, x='timestamp', y='amount', color='status', title="Amount Trends Over Time", width=900, height=500)
st.plotly_chart(fig6)
