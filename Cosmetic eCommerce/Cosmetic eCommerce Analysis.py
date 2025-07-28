# Libraries 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
# Dataset
data = pd.read_csv('Cosmetic Data.csv')
print(data.head())
### Creating necessary Date & Time columns
# Separating timezones and converting string into proper datetime
data['timezone'] = data['event_time'].str.rsplit(" ",n=1,expand=True)[1]
data["event_time"]= data["event_time"].str.rsplit(" ", n=1,expand = True)[0]
data["event_time"]=pd.to_datetime(data["event_time"])
# Creating date,time,hours,weekday,weeknum columns
data['date'] = data["event_time"].dt.normalize()
data["time"] = data['event_time'].dt.time
data["hours"] = data['event_time'].dt.hour
data["weekday"] = data['event_time'].dt.weekday
data['weeknum'] = data['event_time'].dt.isocalendar().week
# Adding string prefix 'week_' to 'weeknum' value Replacing numeric weekday values (0–6) with abbreviated day names 
data['weeknum'] = 'week_' + data['weeknum'].astype(str)
data['weekday'] = data['weekday'].replace({0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'})
print(data.head())
# Filtering irrelavant data by checking range and datatypes 
print(data.info())
print(data.describe())
# Calculating orders that are returned 
returned_orders = data[data['price']<0]['price'].count()
returned_orders_perc = returned_orders/(data['price'].count())
returned_orders_perc = round(returned_orders_perc * 100, 2)  
print(f"{returned_orders_perc}% of total orders were returned.")
# Null data in the dataset 
data = data[data['price'] >= 0]
perc_null = data.isnull().sum() * 100 / len(data) # Percentage of missing values in All columns
print(round(perc_null,2))
# Visualising missing values 
msno.matrix(data)
plt.show()
msno.bar(data)
plt.show()
# Data Analysis & Visualisation
# Unique values in dataset 
data.nunique()
# Creating customer purchase visualisation
data.event_type.unique()
# Data grouping for customer purchase visualisation
data_funnel = data[data['event_type'] != 'remove_from_cart'].groupby(['event_type'], as_index=False)['event_time'].count()
data_funnel.columns = ['event_type', '# events']
data_funnel.sort_values('# events', inplace=True, ascending=False)
data_funnel.reset_index(drop=True, inplace=True)
data_funnel['percent'] = data_funnel['# events'] / data_funnel['# events'].sum() * 100
print(data_funnel)
# Visualisation 
plt.figure(figsize=(8, 5))
sns.barplot(data=data_funnel, y='event_type', x='# events', hue='event_type', palette="YlOrBr", legend=False)
for index, row in data_funnel.iterrows():
    plt.text(row['# events'], index, f"{row['percent']:.2f}%", va='center')
plt.title("Customer Funnel for Purchase Journey")
plt.xlabel("Number of Events")
plt.ylabel("Event Type")
plt.tight_layout()
plt.show()
# Hourly website traffic 
datahour = data.groupby(['hours', 'weeknum'], as_index=False)['price'].count()
datahour.columns = ['hours', 'weeknum', 'price']
#Visualisation
plt.figure(figsize=(12, 6))
sns.lineplot(data=datahour, x='hours', y='price', hue='weeknum', palette="cividis")
plt.title("Customer's Hourly Website Views")
plt.xlabel("Hours")
plt.ylabel("Visitors")
plt.xticks(range(0, 24, 2))
plt.tight_layout()
plt.show()
# Daily sales, Ticket size, Number of orders 
datadate = data[data['event_type'] == 'purchase'].groupby(['date'], as_index=False)['price'].sum()
datadateh = data[data['event_type'] == 'purchase'].groupby(['date'], as_index=False)['price'].count()
datadateh['avg_ticket'] = datadate['price'] / datadateh['price']
datadate['date'] = pd.to_datetime(datadate['date'])
datadateh['date'] = pd.to_datetime(datadateh['date'])
datadate.columns = ['date', 'price']
# Visualisation 
datadate['date_str'] = datadate['date'].dt.strftime('%Y-%m-%d')
datadateh['date_str'] = datadateh['date'].dt.strftime('%Y-%m-%d')

fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# Sales & No of Purchases
sns.barplot(ax=axes[0], data=datadate, x='date_str', y='price', color='skyblue', label='Sales')
sns.lineplot(ax=axes[0], data=datadateh, x='date_str', y='price', color='coral', label='No of Purchases')
axes[0].legend()
axes[0].set_ylabel('Sales / No of Purchases')
axes[0].set_title('Daily Sales & Purchases')

# Avg Ticket Size (Fix: use date_str here too)
sns.lineplot(ax=axes[1], data=datadateh, x='date_str', y='avg_ticket', color='green', marker="o")
axes[1].set_ylabel('Avg Ticket Size')
axes[1].set_xlabel('Date')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Hourly sales in January  
datadatehour = data[data['event_type'] == 'purchase'].groupby(['date', 'hours'], as_index=False)['price'].sum()
datadatehour.columns = ['date', 'hours', 'price']
datadatehour['hours'] = datadatehour['hours'].astype(str)
datadatehour['date'] = datadatehour['date'].astype(str)
# Visualisation 
pivot_hourly = datadatehour.pivot_table(index='hours', columns='date', values='price', fill_value=0)
plt.figure(figsize=(16, 6))
sns.heatmap(pivot_hourly, cmap='cividis')
plt.title('Hourly Sales during January')
plt.xlabel('Date')
plt.ylabel('Hour')
plt.tight_layout()
plt.show()
# Hourly sales in January by weeks 
pivot_week = datahour.pivot_table(index='weeknum', columns='hours', values='price', fill_value=0)
plt.figure(figsize=(14, 6))
sns.heatmap(pivot_week, cmap='cividis')
plt.title('Hourly Sales by Week')
plt.xlabel('Hours')
plt.ylabel('Week Number')
plt.tight_layout()
plt.show()
