create table if not exists Clients
(
    id     serial primary key,
    name   varchar,
    address varchar,
    phone  varchar
);

create table if not exists Orders
(
    id          serial primary key,
    client_id   integer references Clients (id),
    total_price integer,
    date        date
);

create table if not exists Products
(
    id serial primary key,
    title varchar,
    ed varchar
);

create table if not exists Orders_Products(
    id serial primary key,
    order_id integer references Orders(id),
    product_id integer references Products(id),
    price integer,
    quantity integer,
    isDelivered boolean
);