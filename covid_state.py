#!/usr/bin/env python
########################################################
# Example script to plot state-level COVID-19 stats    #
# for Oklahoma using data from The New York Times &    #
# The COVID Tracking Project                           #
#                                                      #
# you will need to obtain data from:                   #
# https://github.com/nytimes/covid-19-data.git         #
# https://covidtracking.com/api/v1/states/ok/daily.csv #
# -- you can replace ok with your state of choice      #
########################################################
import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import datetime, matplotlib

# set state
state = "Oklahoma"
short = "ok"

# get today's date for "updated" info
today = datetime.date.today()

# formatting settings for dates on x-axis
months = mdates.WeekdayLocator(mdates.MO,interval=2) 
datfmt = mdates.DateFormatter('%b %d')

# create figure for cases
fig1 = pl.figure(figsize=(10,5))
ax1  = fig1.add_subplot(111)

# create figure for testing
fig2 = pl.figure(figsize=(10,5))
ax2  = fig2.add_subplot(111)
ax3  = ax2.twinx()

# create figure for deaths and hospitalizations
fig3 = pl.figure(figsize=(10,5))
ax4  = fig3.add_subplot(111)
ax5  = ax4.twinx()

# read data files into pandas dataframes
df1  = pd.read_csv("covid-19-data/us-states.csv", header=0)
df2 =  pd.read_csv("covid-tracking/%s.csv"%short, header=0)

###################
# New Daily Cases #
###################

# get data associated with state
where = df1.loc[df1['state'] == state]

# get dates and re-format
dates = where['date'].to_numpy()
dates = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in dates]

# get all cases
cases_all = where['cases'].to_numpy()    

# convert to daily new cases
cases_new      = np.zeros(cases_all.shape)
cases_new[0]   = cases_all[0]
cases_new[1::] = cases_all[1::]-cases_all[:-1]

# compute 7-day rolling average
cases_avg = np.convolve(cases_new, np.ones((7,))/7, mode='valid')

# plot new cases
ax1.bar(dates,cases_new,color='k',alpha=0.3,label="new cases",) 
ax1.plot(dates[6::],cases_avg,lw=3,label="7-day rolling average")

# modifications to axis of new cases
start = datetime.datetime.strptime('2020-04-13', '%Y-%m-%d')
ax1.set_xlim(start,dates[-1])
ax1.xaxis.set_major_locator(months)
ax1.xaxis.set_major_formatter(datfmt)
for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
for tick in ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1], labels[::-1],loc='upper left')
ax1.set_title('%s: Daily New COVID-19 Cases'%state,fontsize=16)
text = 'data source: https://github.com/nytimes/covid-19-data'
ax1.annotate(text, xy=(1, 1), xytext=(-171, -11), fontsize=6,
             xycoords='axes fraction', textcoords='offset points',
             bbox=dict(facecolor='white', ec = 'lightgray', alpha=0.8,boxstyle='round'))

# adjust and save figure
fig1.tight_layout()
fig1.savefig('covid_cases_%s.png'%short,dpi=300)

##########################
# Testing and Positivity #
##########################

# get dates and re-format
dates = df2['date'].to_numpy().astype('str')
dates = [datetime.datetime.strptime(date, '%Y%m%d').date() for date in dates][::-1]

# get total positive and negative tests
tests_pos = df2['positive'].to_numpy()[::-1]
tests_neg = df2['negative'].to_numpy()[::-1]
tests_all = tests_pos + tests_neg

# convert to daily new total tests
tests_new      = np.zeros(tests_all.shape)
tests_new[0]   = tests_all[0]
tests_new[1::] = tests_all[1::]-tests_all[:-1]

# convert to daily new positive tests
positive_new      = np.zeros(tests_pos.shape)
positive_new[0]   = tests_pos[0]
positive_new[1::] = tests_pos[1::]-tests_pos[:-1]

# convert to daily new negative tests
negative_new      = np.zeros(tests_neg.shape)
negative_new[0]   = tests_neg[0]
negative_new[1::] = tests_neg[1::]-tests_neg[:-1]

# compute 7-day rolling averages
tests_avg    = np.convolve(tests_new,     np.ones((7,))/7, mode='valid')
positive_avg = np.convolve(positive_new , np.ones((7,))/7, mode='valid')
negative_avg = np.convolve(negative_new , np.ones((7,))/7, mode='valid')
pos_rate_avg = positive_avg / tests_avg * 100

# plot tests and positivity rate
ax2.bar(dates,tests_new,color='k',alpha=0.3,label="total tests")
ax3.plot(dates[6::],pos_rate_avg,lw=3,label="percent positive")

# modifications to axes of new tests and positivity
start = datetime.datetime.strptime('2020-04-13', '%Y-%m-%d')
ax2.set_xlim(start,dates[-1])
ax3.set_xlim(start,dates[-1])
ax2.set_ylim(ymin=0)
ax3.set_ylim(0,10)
ax2.xaxis.set_major_locator(months)
ax2.xaxis.set_major_formatter(datfmt)
ax3.xaxis.set_major_locator(months)
ax3.xaxis.set_major_formatter(datfmt)
ax3.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.tick_params(axis='y', colors="#B2B2B2")
ax3.tick_params(axis='y', colors="#1f77b4",labelsize=16)
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
for tick in ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax3.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax2.set_title('%s: COVID-19 Testing and Positivity Rate (7-day rolling average)'%state,fontsize=16)
text = 'data source: https://covidtracking.com'
ax2.annotate(text, xy=(1, 1), xytext=(-123, -11), fontsize=6,
            xycoords='axes fraction', textcoords='offset points',
            bbox=dict(facecolor='white', ec = 'lightgray', alpha=0.8,boxstyle='round'))

# adjust and save figure
fig2.tight_layout()
fig2.savefig('covid_tests_%s.png'%short,dpi=300)

###############################
# Hospitalizations and Deaths #
###############################

# get all hospitalizations
hospital_all = df2['hospitalizedCurrently'].to_numpy()[::-1]

# compute 7-day rolling average
hospital_avg = np.convolve(hospital_all, np.ones((7,))/7, mode='valid')

# get all deaths
deaths_all = df2['death'].to_numpy()[::-1]

# convert to new deaths
deaths_new      = np.zeros(deaths_all.shape)
deaths_new[0]   = deaths_all[0]
deaths_new[1::] = deaths_all[1::]-deaths_all[:-1]

# compute 7-day rolling average
deaths_avg = np.convolve(deaths_new, np.ones((7,))/7, mode='valid')

# plot hospitalizations and deaths
ax4.bar(dates[6::],hospital_avg,label="hospitalizations",color='k',alpha=0.3)
ax5.plot(dates[6::],deaths_avg,lw=3,label="deaths")

# modifications to axis of new tests and positivity
start = datetime.datetime.strptime('2020-04-13', '%Y-%m-%d')
ax4.set_xlim(start,dates[-1])
ax5.set_xlim(start,dates[-1])
ax4.xaxis.set_major_locator(months)
ax4.xaxis.set_major_formatter(datfmt)
ax5.xaxis.set_major_locator(months)
ax5.xaxis.set_major_formatter(datfmt)
ax4.tick_params(axis='y', colors="#B2B2B2")
ax5.tick_params(axis='y', colors="#1f77b4",labelsize=16)
for tick in ax4.xaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
for tick in ax4.yaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
lines1, labels1 = ax4.get_legend_handles_labels()
lines2, labels2 = ax5.get_legend_handles_labels()
ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper center')
ax4.set_title('%s: COVID-19 Deaths and Hospitalizations (7-day rolling average)'%state,fontsize=16)
text = 'data source: https://covidtracking.com'
ax4.annotate(text, xy=(1, 1), xytext=(-123, -11), fontsize=6,
             xycoords='axes fraction', textcoords='offset points',
             bbox=dict(facecolor='white', ec = 'lightgray', alpha=0.8,boxstyle='round'))

# adjust and save figure
fig3.tight_layout()
fig3.savefig('covid_hosp_death_%s.png'%short,dpi=300)
