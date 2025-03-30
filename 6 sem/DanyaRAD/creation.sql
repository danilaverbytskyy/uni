-- drop table if exists Products;
-- drop table if exists Client;
-- drop table if exists Futura;
-- drop table if exists FuturaInfo;


CREATE TABLE if not exists Products
(
    id   serial primary key ,
    name varchar,
    ed   varchar
);

create table if not exists Client
(
    id     serial primary key,
    name   varchar,
    adress varchar,
    phone  varchar
);

create table if not exists Futura
(
    id        serial primary key ,
    IDClient  int references Client (id),
    data      varchar,
    total_sum int
);

create table if not exists FuturaInfo
(
    id         serial primary key ,
    futura_id  int references Futura (id),
    product_id int references Products (id),
    quantity   int,
    price      int
);

create or replace function insert_futura_info() RETURNS trigger as
    $ad_fi_trigger$
    begin
        update Futura set total_sum=total_sum+new.quantity * new.price
        where Futura.id = new.futura_id;
        return null;
    end;
    $ad_fi_trigger$ language plpgsql;

create or replace function delete_futura_info() RETURNS trigger as
    $del_fi_trigger$
    begin
        update Futura set total_sum=total_sum-old.quantity * old.price
        where Futura.id = new.futura_id;
        return null;
    end;
    $del_fi_trigger$ language plpgsql;

create or replace trigger ins_finita_info after insert on FuturaInfo
    for each row execute procedure insert_futura_info();

create or replace trigger del_finita_info after insert on FuturaInfo
    for each row execute procedure delete_futura_info();