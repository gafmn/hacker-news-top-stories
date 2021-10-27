#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $POSTGRES_HN_USER WITH PASSWORD '$POSTGRES_HN_PASSWORD';
    CREATE DATABASE $POSTGRES_HN_DB;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_HN_DB TO $POSTGRES_HN_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_HN_USER" --dbname "$POSTGRES_HN_DB" <<-EOSQL
    CREATE TABLE h_articles (
      hash INT,
      created_at varchar(20) NOT NULL,
      PRIMARY KEY(hash)
    );
    
    CREATE TABLE hsat_article_descriptions (
      hash INT,
      article_hash INT,
      name varchar(300),
      link varchar(300),
      rating INT,
      PRIMARY KEY(hash),
      CONSTRAINT fk_article
        FOREIGN KEY(article_hash)
          REFERENCES h_articles(hash)
    );
EOSQL
