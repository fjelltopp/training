docker build -t sql-ex .
docker run -it --rm -p 8888:8888 --network host -v excersises:/home/jovyan/work sql-ex
