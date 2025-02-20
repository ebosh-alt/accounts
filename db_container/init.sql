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
            id       bigint PRIMARY KEY,
            username text
        );

        CREATE TABLE sellers
        (
            id       bigint PRIMARY KEY,
            username text,
            rating   float,
            balance  float,
            wallet   text
        );

        create table categories
        (
            id   serial PRIMARY KEY,
            name text
        );

        create table subcategories
        (
            id          serial PRIMARY KEY,
            name        text,
            category_id int REFERENCES categories (id)
        );

        CREATE TABLE deals
        (
            id                  serial PRIMARY KEY,
            buyer_id            bigint REFERENCES users (id),
            seller_id           bigint REFERENCES sellers (id),
            price               float,
            wallet              text,
            payment_status      int,
            date                date,
            guarantor           bool
        );

        CREATE TABLE accounts
        (
            id             serial PRIMARY KEY,
            name           text,
            price          float,
            description    text,
            data           text,
            view_type      bool,
            subcategory_id int REFERENCES subcategories (id),
            deal_id        int REFERENCES deals (id),
            uid            text
        );

        CREATE TABLE chats
        (
            id        bigint PRIMARY KEY,
            user_id   bigint REFERENCES users (id),
            seller_id bigint REFERENCES sellers (id)
        );

        create table shops
        (
            id          serial PRIMARY KEY,
            name        text,
            description text,
            path_photo  text
        );

        create table acceptable_account_categories
        (
            id   serial PRIMARY KEY,
            name text
        );
        
        RAISE NOTICE 'Таблицы успешно созданы.';
    EXCEPTION
        WHEN OTHERS THEN
            RAISE EXCEPTION 'Ошибка при создании таблиц: %', SQLERRM;
    END
$$;