#!/usr/bin/env python
#########################################
# Example script to plot worldwide      #
# covid-19 cases and deaths from        #
# Our World in Data (OWID)              #
#                                       #
# you will need to obtain data from     #
# https://github.com/owid/covid-19-data #
#########################################
import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import datetime, matplotlib

# get today's date for "updated" info
today = datetime.date.today()

# create a list of countries to highlight
highlight = ['United States','Brazil','Qatar','United Kingdom','Canada','Italy','Australia','Finland']

# formatting settings for dates on x-axis
months = mdates.WeekdayLocator(matplotlib.dates.MO) 
datfmt = mdates.DateFormatter('%b %d')

# create figure
fig = pl.figure(figsize=(10,12))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

# read data file into pandas dataframe
df = pd.read_csv("covid-19-data/public/data/owid-covid-data.csv", header=0)

# create list of unique countries and get count
countries = df['location'].unique()
n_country = len(countries)

# loop through each country
for c in range(n_country):

    # get key for current country
    country = countries[c]

    # get data associated with current country
    where = df.loc[df['location'] == country]

    # get dates and re-format
    dates = where['date'].to_numpy()
    dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in dates]
    
    # get new cases, compute the 7-day rolling average, mask nans
    new_cases = where['new_cases_per_million'].to_numpy()
    new_cases = np.convolve(new_cases, np.ones((7,))/7, mode='valid')
    new_cases = np.ma.array(new_cases, mask=np.isnan(new_cases),fill_value=-999).filled()

    # get new deaths, compute the 7-day rolling average, mask nans
    new_death = where['new_deaths_per_million'].to_numpy()
    new_death = np.convolve(new_death, np.ones((7,))/7, mode='valid')
    new_death = np.ma.array(new_death, mask=np.isnan(new_death), fill_value=-999).filled()
    
    # find index where new cases first equals 1/million and deaths first equals 0.1/million
    start_cases = np.ma.argmax(new_cases>=1)
    start_death = np.ma.argmax(new_death>=0.1)

    # use color and more prominent lines for highlighted countries
    if country in highlight:
        
        # plot new cases and add a label at the end of the line
        ax1.plot(new_cases[start_cases::], lw=2,zorder=100)
        ax1.annotate(s=country,xy=(len(new_cases[start_cases::]),new_cases[start_cases::][-1]), xytext=(1,0), textcoords='offset points', va='center')
        
        # plot new deaths and add a label at the end of the line
        ax2.plot(new_death[start_death::], lw=2,zorder=100)
        ax2.annotate(s=country,xy=(len(new_death[start_death::]),new_death[start_death::][-1]), xytext=(1,0), textcoords='offset points', va='center')
    # use less prominent lines for other countries 
    else:
        
        # plot new cases
        ax1.plot(new_cases[start_cases::],color='lightgray', lw=0.5)

        # plot new deaths
        ax2.plot(new_death[start_death::],color='lightgray', lw=0.5)    

# modifications to axis of new cases
locmin = mtick.LogLocator(base=10.0, subs=np.arange(2, 10) * .1,numticks=100)
ax1.set_yscale('symlog')
ax1.yaxis.set_minor_locator(locmin)
ax1.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax1.yaxis.set_major_formatter(mtick.ScalarFormatter())
ax1.set_xlim(0,125)
ax1.set_ylim(0,1000)
for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(14) 
for tick in ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_xlabel('Days since total confirmed cases reached 1 per million',fontsize=14)
ax1.set_title('Daily new confirmed COVID-19 cases per million people (7-day rolling average)',fontsize=14,loc='center')
ax1.annotate("chart by:@jeremy_gibbs\nupdated: %d/%d"%(today.month,today.day), xy=(1, 0), xytext=(-80, 20), fontsize=6,
              xycoords='axes fraction', textcoords='offset points',
              bbox=dict(facecolor='white', ec = 'None', alpha=0.8,boxstyle='round'))

# modifications to axis of new cases
locmin = mtick.LogLocator(base=10.0, subs=np.arange(2, 10) * .1,numticks=100)
ax2.set_yscale('symlog',linthreshy=0.1)
ax2.yaxis.set_minor_locator(locmin)
ax2.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax2.yaxis.set_major_formatter(mtick.ScalarFormatter())
ax2.set_xlim(0,125)
ax2.set_ylim(0,100)
ax2.set_yticks([1E-1,1E0,1E1,1E2])
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize(14) 
for tick in ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)
ax2.set_xlabel('Days since total confirmed deaths reached 0.1 per million',fontsize=14)
ax2.set_title('Daily new confirmed COVID-19 deaths per million people (7-day rolling average)',fontsize=14,loc='center')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.annotate("chart by:@jeremy_gibbs\nupdated: %d/%d"%(today.month,today.day), xy=(1, 0), xytext=(-80, 50), fontsize=6,
              xycoords='axes fraction', textcoords='offset points',
              bbox=dict(facecolor='white', ec = 'None', alpha=0.8,boxstyle='round'))

# adjust and save figure
fig.tight_layout()
fig.subplots_adjust(hspace=0.3)
pl.savefig('covid_world.png',dpi=300)
