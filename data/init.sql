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

-- drop table users;
-- drop table sellers;
-- drop table categories;
-- drop table subcategories;
-- drop table items;
-- drop table deals;
-- drop table chats;