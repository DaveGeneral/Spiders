# Web Spider by Python

In this repository, I try to use some wonderful python libraries and framework to achieve tricky web crawlers. 



## Quick Start

### Set Environment 

1. Activate a virtualenv using python3 

```sh		
$ virtualenv env3 /usr/local/bin/python3
```

2. Install the requirements

```sh
$ pip install -r requirements.txt
```

3. Notes: Make sure you have installed mongodb in your system


## Use no framework (Douban, Baozou and IMDB)

### Create user and MySql database
````sh

$ cd Spider_Projects/template
$ cat pre.sql
```

follow the steps in this document to create the corresonding user, password and database

### Run the script and compare

#### Douban(Normal and multi_threads)

``` sh
$ cd Spider_Projects/douban
$ time python douban.py
$ time python douban_mthread.py
```




## Use framework Scrapy (Stackoverflow)




