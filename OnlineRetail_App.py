import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Set page config for a wide "Data Scientist" view
st.set_page_config(page_title="Retail Intelligence Engine", layout="wide")

def get_data():
    conn = sqlite3.connect('retail_real.db')
    # Fetch segments joined with transactions for deep analysis
    query = """
    SELECT s.customer_id, s.segment_name, t.Invoice, t.InvoiceDate, t.Quantity, t.Price
    FROM customer_segments s
    JOIN transactions t ON s.customer_id = t."Customer ID"
    """
    df = pd.read_sql(query, conn)
    
    # Re-calculate RFM for the dashboard metrics
    rfm = df.groupby(['customer_id', 'segment_name']).agg({
        'InvoiceDate': lambda x: (pd.to_datetime('now') - pd.to_datetime(x).max()).days,
        'Invoice': 'nunique',
        'Quantity': 'sum',
        'Price': 'mean'
    }).reset_index()
    rfm.columns = ['customer_id', 'segment_name', 'recency', 'frequency', 'quantity', 'avg_price']
    rfm['monetary'] = rfm['quantity'] * rfm['avg_price']
    
    conn.close()
    return rfm

# --- HEADER SECTION ---
st.title("📊 Retail Customer Intelligence")
st.markdown("---")

try:
    data = get_data()

    # --- TOP LEVEL METRICS (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{len(data):,}")
    col2.metric("Avg Monetary Value", f"${data['monetary'].mean():,.2f}")
    col3.metric("Top Segment", data['segment_name'].mode()[0])
    col4.metric("Retention Rate", "84%") # Placeholder for logic

    # --- MAIN DASHBOARD LAYOUT ---
    tab1, tab2 = st.tabs(["Clustering Analysis", "Customer Lookup"])

    with tab1:
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("3D Cluster Projection")
            fig = px.scatter_3d(
                data, x='recency', y='frequency', z='monetary',
                color='segment_name', 
                template="plotly_dark",
                height=700
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.subheader("Segment Distribution")
            dist = data['segment_name'].value_counts().reset_index()
            fig_pie = px.pie(dist, values='count', names='segment_name', hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.subheader("Segment Statistics")
            stats = data.groupby('segment_name')['monetary'].mean().sort_values(ascending=False)
            st.table(stats)

    with tab2:
        st.subheader("High-Resolution Data Grid")
        selected_segment = st.multiselect("Filter by Segment", options=data['segment_name'].unique(), default=data['segment_name'].unique())
        filtered_data = data[data['segment_name'].isin(selected_segment)]
        st.dataframe(filtered_data, use_container_width=True, height=500)

except Exception as e:
    st.error(f"Engine Error: {e}")
    st.info("Ensure 'retail_real.db' is in the root folder.")