import pandas as pd     
import streamlit as st
import plotly.express as px
df = pd.read_csv('all_df.csv')
st.set_page_config(page_title='My Sales Dashboard', page_icon=':bar_chart:', layout = 'wide')
st.sidebar.header ("Please Filter Here")

select_product = st.sidebar.multiselect(
    'Select Product',
    options= df['Product'].unique(),
    default = df['Product'].unique()[:5]
)
select_month = st.sidebar.multiselect(
    'Select Month',
    options= df['Month'].unique(),
    default = df['Month'].unique()[:5]
)
select_city = st.sidebar.multiselect(
    'Select City',
    options= df['City'].unique(),
    default = df['City'].unique()[:5]
)


total_sales = df['Total'].sum()
no_of_prod = df['Product'].nunique()

l_col,r_col = st.columns(2)
with l_col:
    st.subheader('Total Sales')
    st.subheader(f'US ${total_sales}')

with r_col:
    st.subheader('Total Number of Products')
    st.subheader(f'{no_of_prod}')


df_select = df.query('Product == @select_product and Month == @select_month and City == @select_city')
a,b,c = st.columns(3)
total_sales_by_product = df_select.groupby(by=['Product'])['Total'].sum().sort_values()

fig1 = px.bar(
    total_sales_by_product,
    x= total_sales_by_product.values,
    y= total_sales_by_product.index,
    title='Total Sales by Product',
    
)
a.plotly_chart(fig1,use_container_width=True)

total_sales_by_city = df.groupby(['City'])['Total'].sum().reset_index()

fig2 = px.pie(
    total_sales_by_city,
    values='Total',
    names='City',
    title='Total Sales by City'
    
)
b.plotly_chart(fig2,use_container_width=True)

total_sales_by_month = df.groupby(['Month'])['Total'].sum().reset_index()
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
total_sales_by_month['Month'] = pd.Categorical(total_sales_by_month['Month'], categories=month_order, ordered=True)
total_sales_by_month = total_sales_by_month.sort_values('Month')

fig3 = px.line(
    total_sales_by_month,
    x='Month',
    y='Total',
    title='Total Sales by Month'
    
)
c.plotly_chart(fig3,use_container_width=True)

d,e = st.columns(2)

fig4 = px.scatter(
    df_select,
    x='QuantityOrdered',
    y='PriceEach',
    title='Total Sales by Product'
    
)
d.plotly_chart(fig4,use_container_width=True)

fig5 = px.scatter(
    df_select,
    x='PriceEach',
    y='Total',
    color='Product',
    hover_name='City',
    log_x=True,
    size_max=60,
    title='Total Sales by Product'
    
)
e.plotly_chart(fig5,use_container_width=True)
