docker rmi $(docker images -f "dangling=true" -q)
docker builder prune
docker compose build api --no-cache
