docker compose down
docker rmi $(docker images -f "dangling=true" -q)
docker builder prune
docker volume prune
docker compose build api --no-cache
docker rmi $(docker images -f "dangling=true" -q)
