
backend_id=`docker ps | grep staging-backend | awk '{print $1}'`
docker exec -it $backend_id /bin/bash
