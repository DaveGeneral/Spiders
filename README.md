# Web Spider by Python

In this repository, I try to use some wonderful python libraries and framework to achieve tricky web crawlers. Using requests and beautifulsoup, I crawled three different server - douban, baozou and imdb. Meanwhile, I used scrapy framework to crawl stackoverflow most voted and frequently asked questions.
<br><br>

## I. Environment settings

##### 1. Activate a virtualenv using python3

```sh
$ virtualenv env3 -p /usr/local/bin/python3
```

##### 2. Activate the environment

```sh
$ source env3/bin/source
```

##### 3. Install the required libraries

```sh
$ pip install -r requirements.txt
```

##### 4. Notes: Make sure you have installed mongodb in your system

<br>

## II. Without framework

#### 1. Create user and Mysql database

````sh
$ cd Spider_Projects/template
$ cat pre.sql
```

Follow the steps in this document to create the corresonding user, password and database
<br>
#### 2. Run the script and compare

Here we use different models to make comparision based on cpu use, runtime etc.

##### Douban

``` sh
$ cd Spider_Projects/douban

# Douban top 250 movies
$ time python douban.py  # 1.62s user 0.23s system 8% cpu 21.560 total
$ time python douban_mthread.py  # 2.64s user 0.76s system 81% cpu 4.154 total
```


##### Baozou

``` sh
$ cd Spider_Projects/baozon

# Baozou 100 page gifs
$ time python baozou.py  # 24.04s user 9.27s system 5% cpu 10:07.52 total
$ time python baozou_mprocess.py  # 30.62s user 10.82s system 40% cpu 1:41.19 total
```

##### IMDB

``` sh
$ cd Spider_Projects/imdb

# imdb top 250 movies
$ time python imdb.py

# imdb top rated genres
$ time python genre_mthread.py  # 77.37s user 16.25s system 80% cpu 1:56.39 total
$ time python genre_mprocess.py  # 53.52s user 2.42s system 51% cpu 1:48.47 total
$ time python genre_mpg.py  # 75.91s user 2.95s system 361% cpu 21.809 total
```
<br>

## III. With Scrapy
#### 1. Open the mongodb server

```sh
$ mongod
$ mongo
```

#### 2. Run the application

```sh
$ cd Spider_Projects/stackoverflow/soflow
$ scrapy crawl stack
```



