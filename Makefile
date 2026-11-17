run-dev: 
	uvicorn main:app --reload

stop-dev: 
	docker compose down

update-requirements: 
	pip freeze > requirements.txt

goto-psql: 
	docker compose exec db psql -U brayley -d shortener

list-ports: 
	sudo lsof -i

