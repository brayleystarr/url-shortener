run-dev: 
	uvicorn main:app --reload

stop-dev: 
	docker compose down

update-requirements: 
	pip freeze > requirements.txt

list-ports: 
	netstat -n

start: 
	tmux new-session -d -s database_container 'cd $(CURDIR) && docker compose up'
	tmux new-session -d -s application_server 'cd $(CURDIR) && .venv/bin/uvicorn main:app --reload'
	tmux new-session -d -s database_testing 'cd $(CURDIR) && docker compose exec db psql -U brayley -d shortener'
	gnome-terminal -- bash -c 'tmux attach -t database_container'
	gnome-terminal -- bash -c 'tmux attach -t application_server'
	gnome-terminal -- bash -c 'tmux attach -t database_testing'

stop: 
	tmux send-keys -t database_container 'docker compose down' C-m
	tmux send-keys -t application_server C-c
	tmux send-keys -t database_testing C-c
	tmux kill-session -t database_container
	tmux kill-session -t application_server
	tmux kill-session -t database_testing
