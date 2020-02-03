# you'll first check to see how many times "Protective Frisk" was the only search type.
# Count the 'search_type' values
print(ri['search_type'].value_counts())
# Check if 'search_type' contains the string 'Protective Frisk'
ri['frisk'] = ri.search_type.str.contains('Protective Frisk', na=False)
# Check the data type of 'frisk'
print(ri.frisk.dtype)
# Take the sum of 'frisk'
print(ri.frisk.sum())
 #Are males frisked more often than females, perhaps because police officers consider them to be higher risk?
 # Create a DataFrame of stops in which a search was conducted
searched = ri[ri.search_conducted == True]
# Calculate the overall frisk rate by taking the mean of 'frisk'
print(searched.frisk.mean())
# Calculate the frisk rate for each gender
print(searched.groupby('driver_gender').frisk.mean())
'''Interesting! The frisk rate is higher for males than for females, 
though we can't conclude that this difference is caused by the driver's gender.'''
#Does time of day affect arrest rate?
#Calculating the hourly arrest rate
# Calculate the overall arrest rate
print(ri.is_arrested.mean())
# Calculate the hourly arrest rate
print(ri.groupby(ri.index.hour).is_arrested.mean())
# Save the hourly arrest rate
hourly_arrest_rate = ri.groupby(ri.index.hour).is_arrested.mean()
# Import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
# Create a line plot of 'hourly_arrest_rate'
hourly_arrest_rate.plot()
# Add the xlabel, ylabel, and title
plt.xlabel('Hour')
plt.ylabel('Arrest Rate')
plt.title('Arrest Rate by Time of Day')
#Wow! The arrest rate has a significant spike overnight, and then dips in the early morning hours.
#Are drug-related stops on the rise?
#Plotting drug-related stops
# Calculate the annual rate of drug-related stops
print(ri.drugs_related_stop.resample('A').mean())
# Save the annual rate of drug-related stops
annual_drug_rate = ri.drugs_related_stop.resample('A').mean()
# Create a line plot of 'annual_drug_rate'
annual_drug_rate.plot()
# Display the plot
plt.show()
#Interesting! The rate of drug-related stops nearly doubled over the course of 10 years.Why might that be the case?
'''You might hypothesize that the rate of vehicle searches was also increasing, 
which would have led to an increase in drug-related stops even if more drivers were not carrying drugs.'''
# Calculate and save the annual search rate
annual_search_rate = ri.search_conducted.resample('A').mean()
# Concatenate 'annual_drug_rate' and 'annual_search_rate'
annual = pd.concat([annual_drug_rate,annual_search_rate], axis='columns')
# Create subplots from 'annual'
annual.plot(subplots=True)
# Display the subplots
plt.show()
'''Wow! The rate of drug-related stops increased even though the search rate decreased, disproving our hypothesis.'''
# Create a frequency table of districts and violations
print(pd.crosstab(ri.district,ri.violation))
# Save the frequency table as 'all_zones'
all_zones = pd.crosstab(ri.district,ri.violation)
# Select rows 'Zone K1' through 'Zone K3'
print(all_zones.loc['Zone K1':'Zone K3'])
# Save the smaller table as 'k_zones'
k_zones = all_zones.loc['Zone K1':'Zone K3']
#How do the zones compare in terms of what violations are caught by police?
#you've created a frequency table focused on the "K" zones, you'll visualize 
#the data to help you compare what violations are being caught in each zone.
# Create a bar plot of 'k_zones'
k_zones.plot(kind='bar')
# Display the plot
plt.show()
#In the traffic stops dataset, the stop_duration column tells you approximately how long the driver was detained by the officer.
#Unfortunately, the durations are stored as strings, such as '0-15 Min'. How can you make this data easier to analyze?
# Print the unique values in 'stop_duration'
print(ri.stop_duration.unique())
# Create a dictionary that maps strings to integers
mapping = {'0-15 Min':8,'16-30 Min':23,'30+ Min':45}
# Convert the 'stop_duration' strings to integers using the 'mapping'
ri['stop_minutes'] = ri.stop_duration.map(mapping)
# Print the unique values in 'stop_minutes'
print(ri.stop_minutes.unique())
# Create a stacked bar plot of 'k_zones'
k_zones.plot(kind='bar',stacked=True)
# Display the plot
plt.show()
#Interesting! The vast majority of traffic stops in Zone K1 are for speeding, and Zones K2 and K3 are 
#remarkably similar to one another in terms of violations.
#If you were stopped for a particular violation, how long might you expect to be detained?
# Calculate the mean 'stop_minutes' for each value in 'violation_raw'
print(ri.groupby('violation_raw').stop_minutes.mean())
# Save the resulting Series as 'stop_length'
stop_length = ri.groupby('violation_raw').stop_minutes.mean()
# Sort 'stop_length' by its values and create a horizontal bar plot
stop_length.sort_values().plot(kind='barh')
# Display the plot
plt.show()

# New dataset to see whether weather conditions has an impact over police activity

# Verification whether its a reliable source
'''Nice job! The temperature data looks good so far: the TAVG values are in 
between TMIN and TMAX, and the measurements and ranges seem reasonable.'''
# Create a 'TDIFF' column that represents temperature difference
weather['TDIFF']=weather.TMAX-weather.TMIN
# Describe the 'TDIFF' column
print(weather.TDIFF.describe())
# Create a histogram with 20 bins to visualize 'TDIFF'
weather['TDIFF'].plot(kind='hist',bins=20)
# Display the plot
plt.show()
'''Great work! The TDIFF column has no negative values and its distribution is approximately normal, 
both of which are signs that the data is trustworthy.'''
# Copy 'WT01' through 'WT22' to a new DataFrame
WT = weather.loc[:,'WT01':'WT22']
# Calculate the sum of each row in 'WT'
weather['bad_conditions'] = WT.sum(axis='columns')
# Replace missing values in 'bad_conditions' with '0'
weather['bad_conditions'] = weather.bad_conditions.fillna(0).astype('int')
# Create a histogram to visualize 'bad_conditions'
weather.bad_conditions.plot(kind='hist')
# Display the plot
plt.show()
'''Excellent work! It looks like many days didn't have any bad weather conditions, and only a small portion of days had more than 
four bad weather conditions.'''
'''In the previous exercise, you counted the number of bad weather conditions each day.
In this exercise, you'll use the counts to create a rating system for the weather.'''
# Count the unique values in 'bad_conditions' and sort the index
print(weather.bad_conditions.value_counts().sort_index())
# Create a dictionary that maps integers to strings
mapping = {0:'good', 1:'bad', 2:'bad', 3:'bad',4:'bad',5:'worse',6:'worse',7:'worse',8:'worse',9:'worse'}
# Convert the 'bad_conditions' integers to strings using the 'mapping'
weather['rating'] = weather.bad_conditions.map(mapping)
# Count the unique values in 'rating'
print(weather.rating.value_counts())
'''Nice job! This rating system should make the weather condition data easier to understand.'''
'''Since the rating column only has a few possible values, you'll change its data type 
to category in order to store the data more efficiently.'''
# Create a list of weather ratings in logical order
cats=['good','bad','worse']
# Change the data type of 'rating' to category
weather['rating'] = weather.rating.astype('category', ordered=True, categories=cats)
# Examine the head of 'rating'
print(weather.rating.head())
'''In this exercise, you'll prepare the traffic stop and weather rating DataFrames so that they're ready to be merged:'''
# Reset the index of 'ri'
ri.reset_index(inplace=True)
# Examine the head of 'ri'
print(ri.head())
# Create a DataFrame from the 'DATE' and 'rating' columns
weather_rating = weather.loc[:,['DATE','rating']]
# Examine the head of 'weather_rating'
print(weather_rating.head())
# Examine the shape of 'ri'
print(ri.shape)
# Merge 'ri' and 'weather_rating' using a left join
ri_weather = pd.merge(left=ri, right=weather_rating, left_on='stop_date', right_on='DATE', how='left')
# Examine the shape of 'ri_weather'
print(ri_weather.shape)
# Set 'stop_datetime' as the index of 'ri_weather'
ri_weather.set_index('stop_datetime', inplace=True)
# Does weather affect the arrest rate?
'''Do police officers arrest drivers more often when the weather is bad? Find out below!'''
# Calculate the overall arrest rate
print(ri_weather.is_arrested.mean())
# Calculate the arrest rate for each 'rating'
print(ri_weather.groupby('rating').is_arrested.mean())
# Calculate the arrest rate for each 'violation' and 'rating'
print(ri_weather.groupby(['violation','rating']).is_arrested.mean())
'''Wow! The arrest rate increases as the weather gets worse, and that trend persists across many of the violation types. 
This doesn't prove a causal link, but it's quite an interesting result!'''
# Save the output of the groupby operation from the last exercise
arrest_rate = ri_weather.groupby(['violation', 'rating']).is_arrested.mean()
# Print the 'arrest_rate' Series
print(arrest_rate)
# Print the arrest rate for moving violations in bad weather
print(arrest_rate.loc['Moving violation','bad'])
# Print the arrest rates for speeding violations in all three weather conditions
print(arrest_rate.loc['Speeding'])
# Unstack the 'arrest_rate' Series into a DataFrame
print(arrest_rate.unstack())
# Create the same DataFrame using a pivot table
print(ri_weather.pivot_table(index='violation', columns='rating', values='is_arrested'))
'''Excellent work! In the future, when you need to create a DataFrame like this, 
you can choose whichever method makes the most sense to you.'''
