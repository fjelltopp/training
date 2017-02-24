docker build -t sql-ex .
docker run -it --rm -p 8888:8888 --network host -v /home/jyri/meerkat-code/training/data_storage_solutions/notebook/excersises:/home/jovyan/work sql-ex
