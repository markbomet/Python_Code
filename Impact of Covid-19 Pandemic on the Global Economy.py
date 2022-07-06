#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


os.chdir("C:\\Users\\mbomet\\OneDrive - AAR Insurance\\Desktop\\Jupyter Notebook")


# In[5]:


data_transformed = pd.read_csv("transformed_data.csv")
raw_data = pd.read_csv("raw_data.csv")


# In[6]:


#Data Preparation

print(data_transformed.head())


# In[7]:


print(raw_data.head())


# In[8]:


#check for number of samples of each country in the data sets

data_transformed['COUNTRY'].value_counts()


# In[9]:


#number of samples for each country is not equal. Let's check the mode

data_transformed['COUNTRY'].value_counts().mode()


# In[10]:


#the mode, 294, will be used in dividing HDI, GDP & Population. 
#creating a new data set with the combined data sets

code = data_transformed["CODE"].unique().tolist()
country = data_transformed["COUNTRY"].unique().tolist()
hdi = []
tc = []
td = []
sti = []
population = data_transformed["POP"].unique().tolist()
gdp = []

for i in country:
    hdi.append((data_transformed.loc[data_transformed["COUNTRY"] == i, "HDI"]).sum()/294)
    tc.append((raw_data.loc[raw_data["location"] == i, "total_cases"]).sum())
    td.append((raw_data.loc[raw_data["location"] == i, "total_deaths"]).sum())
    sti.append((data_transformed.loc[data_transformed["COUNTRY"] == i, "STI"]).sum()/294)
    population.append((raw_data.loc[raw_data["location"] == i, "population"]).sum()/294)

combined_data = pd.DataFrame(list(zip(code, country, hdi, tc, td, sti, population)), 
                               columns = ["Country Code", "Country", "HDI", 
                                          "Total Cases", "Total Deaths", 
                                          "Stringency Index", "Population"])
print(combined_data.head())


# In[11]:


# we will sample the top 10 countries with the highest number of Covid-19 cases to assess the impact of Covid-19 before and during 
data = combined_data.sort_values(by=["Total Cases"], ascending=False)
print(data.head())


# In[12]:


#selecting only the Top 10

data = data.head(10)
print(data)


# In[13]:


#Adding two columns: (GDP per capita before Covid-19, GDP per capita during Covid-19) The GDP per Capita data has been manually collected 

data["GDP Before Covid"] = [65279.53, 8897.49, 2100.75, 
                            11497.65, 7027.61, 9946.03, 
                            29564.74, 6001.40, 6424.98, 42354.41]
data["GDP During Covid"] = [63543.58, 6796.84, 1900.71, 
                            10126.72, 6126.87, 8346.70, 
                            27057.16, 5090.72, 5332.77, 40284.64]
print(data)


# In[14]:


#Analysis of spread of Covid-19 in these countries

figure = px.bar(data, y='Total Cases', x='Country',title="Countries with Highest Covid Cases")
figure.show()


# In[15]:


#Check for deaths per country

figure = px.bar(data, y='Total Deaths', x='Country',title="Countries with Highest Deaths")
figure.show()


# In[16]:


#Comparison for number of deaths against cases

fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["Total Cases"],
    name='Total Cases',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["Total Deaths"],
    name='Total Deaths',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()


# #Impact of Covid-19 on HDI.This is a summary measure of average achievement in key dimensions of human development: a long and healthy life, being knowledgeable and have a decent standard of living
# 
# fig = px.bar(data, x='Country', y='Total Cases',
#              hover_data=['Population', 'Total Deaths'], 
#              color='HDI', height=400, 
#              title="Human Development Index during Covid-19")
# fig.show()
# 

# In[17]:


#Comparison of GDP per capita before and during the spread of Covid-19 

fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["GDP Before Covid"],
    name='GDP Per Capita Before Covid-19',
    marker_color='red'
))
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["GDP During Covid"],
    name='GDP Per Capita During Covid-19',
    marker_color='blue'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()

##CONCLUSION
#From the chart above, It is clear that Covid-19 has resulted in a drop in GDP of all the  top 10 countries sampled with the highest number of cases.
# In[ ]:




