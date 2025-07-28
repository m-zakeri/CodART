docker compose down
docker rmi $(docker images -f "dangling=true" -q)
docker -y builder prune
docker -y volume prune
docker compose build api --no-cache
docker rmi $(docker images -f "dangling=true" -q)
