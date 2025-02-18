\c postgres
CREATE EXTENSION IF NOT EXISTS dblink;
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'accounts') THEN
      PERFORM dblink_exec('dbname=postgres user=' || current_user, 'CREATE DATABASE accounts');
   END IF;
END
$$;
\c accounts
DO
$$
    BEGIN
        CREATE TABLE users
        (
            id       int PRIMARY KEY,
            username text
        );

        CREATE TABLE sellers
        (
            id       int PRIMARY KEY,
            username text,
            rating   float,
            balance  float,
            wallet   text
        );

        create table categories
        (
            id   int PRIMARY KEY,
            name text
        );

        create table subcategories
        (
            id          int PRIMARY KEY,
            name        text,
            category_id int REFERENCES categories (id)
        );

        CREATE TABLE deals
        (
            id         int PRIMARY KEY,
            user_id    int REFERENCES users (id),
            seller_id  int REFERENCES sellers (id),
            price      float,
            wallet     text,
            type       int,
            status     int,
            created_at date
        );

        CREATE TABLE accounts
        (
            id             int PRIMARY KEY,
            name           text,
            price          float,
            description    text,
            data           text,
            view_type      int,
            subcategory_id int REFERENCES subcategories (id),
            deal_id        int REFERENCES deals (id)
        );

        CREATE TABLE chats
        (
            id        int PRIMARY KEY,
            user_id   int REFERENCES users (id),
            seller_id int REFERENCES sellers (id)
        );

        create table shops
        (
            id          int PRIMARY KEY,
            name        text,
            description text,
            path_photo  text
        );

        create table acceptable_account_categories
        (
            id   int PRIMARY KEY,
            name text
        );
        
        RAISE NOTICE 'Таблицы успешно созданы.';
    EXCEPTION
        WHEN OTHERS THEN
            RAISE EXCEPTION 'Ошибка при создании таблиц: %', SQLERRM;
    END
$$;