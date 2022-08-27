# Sellor web-app
### App is built using Python: Django and Django Rest Framework, PostgreSQL, HTML/CSS/BOOTSTRAP, JavaScript, Redis.
## Running Online on https://sellor.herokuapp.com/
#### It's an online store/platform for people based in Poland (for now), where you can look for things to buy, or put something for sale. If you find product you are interested in you can add it to wishlist or chat the sellor to agree to meet and buy it from him. In other words the app serves just as agent that allows you to search for products or for customers that'd probably buy your products.
There are *also*:
  - Built-in categories and tags, that can be extended from admin page.
  - Real-time chats functionality through Django Channels.
  - Dashboard, where you can check your history/summary.
  - Feedback page, where you can share your impressions about this app.
  - Report functionality: you can report user, that will also add him to your blacklist.
  - Built-in uneditable Polish cities list.
  - Basic search functionality
  - Tests mostly written with unittests(django.test.TestCase), and a bit PyTest.
  
Moreover there's also a basic **API** done via DRF for future purposes.
#### In "production" app is deployed on Heroku, media files are stored On Amazon S3 Bucket, database engine - PostrgreSQL 

## Requirements
 - **Docker & Docker Compose installed**
 
## Setup
 - open terminal (better as administrator) in project's root folder (where *Dockerfile* and *docker-compose.yml* files are located) and type following:
```
$ docker-compose build
$ docker-compose up
```
 - wait for server to start, then quit by pressing: Ctrl + C.
#### Finally, run:
```
$ docker-compose run --rm app sh -c "python manage.py migrate && python manage.py loaddata examples_fixture.json"
$ docker-compose up
```
The website now should be running on http://localhost:8000 with some dummy data.
#### Later to start the server again: ```$ docker-compose up```
