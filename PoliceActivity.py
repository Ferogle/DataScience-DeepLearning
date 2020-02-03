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
