# Assignment 6

This is web programming and data analysis assignment in subject IN3110 fall 2021.

## Dependencies

The code was developed and tested using Python 3.8.1 and ran on macOS Big Sur 11.5.2.

In order to run please be sure to have Pandas installed:
# conda
```
conda install pandas
```
or
# or PyPI
```
pip install pandas```

As well as Altair:

```
pip install altair vega_datasets
```
or
```
conda install -c conda-forge altair vega_datasets
```
And Altair viewer

```pip install altair_viewer```

In case that instalation doesn't work try instaling using
``` python3 -m pip install <library>```

## Missing functionality

Tasks 6.4(not mandatory), 6.5, 6.6 and 6.7. are not implemented. This is purely because I had to prioritize other subjects. I find this assignment really interesting and useful and I am definitely going to revise the tasks at a later occasion.

Worth mentioning here is that I use somewhat old data set. Its from 16. November. 
My code does not download the code online. Data set file is contained within the assignment folder.


## Task 6.1

Reading data from the csv file and generating a labled plot of Daily new confirmed Covid-19 cases
pre million people by date.
By default, start argument is "2020-05-10" (I dont know why).
End argument is by default last date entry in the data set (2021-11-16).

run the script with:

```
python3 webvisualization_plots.py
```

## Task 6.2/6.3

Generating an interactive web page where a visitor is able to pick a country (please do not pick more than 5), start and end date and get an updated "Daily new confirmed Covid-19 cases
pre million people by date" plot displayed on the web page.

run the script with:

```
uvicorn webvisualization:app --debug

```
then open a browser and paste ```http://localhost:8000/```into a search field.

After this, a web page with the initial graph should be loaded. The initial graph is showing 6 countries with the highest new Covid-19 cases on the last date of the dataset(16.11.2021). It should be possible to choose one or more countries as well as start and end date and by clicking on the "refresh" button the graph is updated with relevant information to user-specified criteria.
Choosing dates after 16.11.2021 and before 01.03.2020. is disabled.



