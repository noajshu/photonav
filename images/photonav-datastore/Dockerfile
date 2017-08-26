FROM postgres:9.6

COPY code/schema.sql /schema.sql

RUN echo 'psql -v ON_ERROR_STOP=1 -f /schema.sql' >> /docker-entrypoint-initdb.d/init-user-db.sh
