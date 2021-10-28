#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $POSTGRES_HN_USER WITH PASSWORD '$POSTGRES_HN_PASSWORD';
    CREATE DATABASE $POSTGRES_HN_DB;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_HN_DB TO $POSTGRES_HN_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_HN_USER" --dbname "$POSTGRES_HN_DB" <<-EOSQL
    CREATE TABLE h_articles (
      article_name varchar(300),
      name_hashed_key INT,
      load_ts varchar(20) NOT NULL,
      PRIMARY KEY(name_hashed_key)
    );
    
    CREATE TABLE hsat_article_descriptions (
      hkey_article INT,
      score INT,
      url varchar(300),
      CONSTRAINT fk_article
        FOREIGN KEY(hkey_article)
          REFERENCES h_articles(name_hashed_key)
    );
EOSQL
