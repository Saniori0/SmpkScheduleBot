docker-compose pull python
docker-compose up --force-recreate --build -d python
docker image prune -f
