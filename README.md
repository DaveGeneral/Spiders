# Web Spider by Python

In this repository, I try to use some wonderful python libraries and framework to achieve tricky web crawlers. 
<br><br>

## I. Set Environment 

##### 1. Activate a virtualenv using python3 

```sh		
$ virtualenv env3 /usr/local/bin/python3
```

##### 2. Install the required libraries

```sh
$ pip install -r requirements.txt
```

##### 3. Notes: Make sure you have installed mongodb in your system

<br>

## II. Method without framework (Douban, Baozou and IMDB)

#### 1. Create user and MySql database

````sh

$ cd Spider_Projects/template
$ cat pre.sql
```

Follow the steps in this document to create the corresonding user, password and database
<br>
#### 2. Run the script and compare

Here we use different models to make comparision based on cpu use, runtime etc.
<br>
##### a. Douban(Normal and multi_threads)

``` sh
$ cd Spider_Projects/douban

$ time python douban.py
1.62s user 0.23s system 8% cpu 21.560 total

$ time python douban_mthread.py
2.64s user 0.76s system 81% cpu 4.154 total
```


##### b. Baozou(Normal and multi_process)

``` sh
$ cd Spider_Projects/baozou

$ time python baozou.py

$ time python baozou_mprocess.py
```

##### c. IMDB(multi_threads, multi_thread and multi_process+gevent)

``` sh
$ cd Spider_Projects/imdb

$ time python genre_mthread.py

$ time python genre_mprocess.py

$ time python genre_mpg.py


```
<br>

## III. Method with framework Scrapy (Stackoverflow)

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



