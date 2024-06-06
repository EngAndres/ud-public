# DataBase Foundation - Course Project Example

This is a reference project based on course work across different workshops, exploring concepts as; _relational databases design_, _sql_, and _RESTful web services_.

The idea is to provide a project structure where users can interract with web services to make operations with the database. At the same time, use _containers_ to make a simple deployment of all. Also, _SQL_ code should be adjusted for both _MySQL_ y _PostgreSQL_.

## The Problem

Here the problem was rrelated with a well known product from _Alphabet_ called _YouTube_. You should image as a _Database Engineer_ for that product. The idea is gather requirements and put in _user stories_ simple sentence format, design database, build database, and use a RESTful api to serve the database interactions.

### User Stories



## Design



## Containers

For _MySQL_ a container using _latest_ image available in _DockerHub_ is used. Using $3306$ as exposed port, in the container environment variables _MYSQL\_ROOT\_PASSWORD_ and _MYSQL\_DATABASE_ the access to database is setup. You could change _enviroment variables_ values to adjust your deploys.

For _PostgreSQL_ a container using _latest_ image available in _DockerHub_ is used. Using $5432$ as exposed port, in the container environment variables _POSTGRES\_USER_, _POSTGRES\_PASSWORD_ and _POSTGRES\_DB_ the access to database is setup. You could change _enviroment variables_ values to adjust your deploys.



## Technical Concerns

As you want to become in a _senior database engineer_, you must to show your best cards.
In this case, the use of _store procedures_, _triggers_, and _views_ is imperative win this challenge.

As follows there is a list of technical decisions on the database applying conceps as mentioned above.
