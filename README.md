# Overview
I like to make charts for fun. This repository contains some example Python scripts to plot COVID-19 data, such as in this figure. The scripts require Matplotlib, Numpy, and Pandas, plus the data files listed below. If you encounter a probelm, [get in touch][7].

![Image of pyburgers logo](https://gibbs.science/img/covid_world.png)

# Worldwide Data
The [covid_world.py][1] file plots daily confirmed cases and deaths across the world. The script requires data from [Our World in Data][2].

# Statewide Data
The [covid_state.py][2] file plots daily confirmed cases, tests/positivity, and hospitalizations/deaths for Oklahoma. It can be modified for any state. The script requires data from [The New York Times][4] and [The COVID Tracking Project][5]. The latter should be placed in a foilder called 'covid-tracking'.

# License 
This template is free source code. It comes without any warranty, to the extent permitted by applicable law. You can redistribute it and/or modify it under the terms of the Do What The Fuck You Want To Public License, Version 2, as published by Sam Hocevar. See [http://www.wtfpl.net][6] for more details.

[1]: covid_world.py
[2]: covid_state.py
[3]: https://github.com/owid/covid-19-data
[4]: https://github.com/nytimes/covid-19-data.git
[5]: https://covidtracking.com/api/v1/states/ok/daily.csv
[6]: http://www.wtfpl.net
[7]: mailto:jeremy.gibbs@noaa.gov
