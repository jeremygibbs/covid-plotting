# Overview
I like to make charts for fun. This repository contains some example Python scripts to plot COVID-19 data. The scripts require Matplotlib, Numpy, and Pandas, plus the data files listed below. If you encounter a probelm, [get in touch][6].

# Worldwide Data
The [covid_world.py][1] file plots daily confirmed cases and deaths across the world. The script requires data from [Our World in Data][2].

# Statewide Data
The [covid_state.py][1] file plots daily confirmed cases, tests/positivity, and hospitalizations/deaths for Oklahoma. It can be modified for any state. The script requires data from [The New York Times][3] and [The COVID Tracking Project][4]. The latter should be placed in a foilder called 'covid-tracking'.

# License 
This template is free source code. It comes without any warranty, to the extent permitted by applicable law. You can redistribute it and/or modify it under the terms of the Do What The Fuck You Want To Public License, Version 2, as published by Sam Hocevar. See [http://www.wtfpl.net][5] for more details.

[1]: [covid_world.py]
[2]: https://github.com/owid/covid-19-data
[3]: https://github.com/nytimes/covid-19-data.git
[4]: https://covidtracking.com/api/v1/states/ok/daily.csv
[5]: http://www.wtfpl.net
[6]: mailto:jeremy.gibbs@noaa.gov
