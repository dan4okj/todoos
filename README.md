RESTful TODO API

Init:
  docker-compose build
  docker-compose up

Init database
	docker-compose run todoapi python manage.py recreate-db

Insert test user
	docker-compose run todoapi python manage.py create-test-user

Run tests
	docker-compose run todoapi python manage.py test


Issues:
  - Login/Logout - Currently you can request as many access tokens as you want
  but logout invalidates only one
  - More tests need to be added
  - Refactor models a bit

Possible Improvements:
  - Todo items to have a separate name, description and due date
  - Define better environments
