#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $POSTGRES_HN_USER WITH PASSWORD '$POSTGRES_HN_PASSWORD';
    CREATE DATABASE $POSTGRES_HN_DB;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_HN_DB TO $POSTGRES_HN_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_HN_USER" --dbname "$POSTGRES_HN_DB" <<-EOSQL
    CREATE TABLE h_articles (
      name varchar(50),
      created_at varchar(20) NOT NULL,
      PRIMARY KEY(name)
    );
    
    CREATE TABLE hsat_article_descriptions (
      hash varchar(30),
      article_name varchar(50),
      link varchar(30),
      rating INT,
      PRIMARY KEY(hash),
      CONSTRAINT fk_article
        FOREIGN KEY(article_name)
          REFERENCES h_articles(name)
    );
EOSQL
