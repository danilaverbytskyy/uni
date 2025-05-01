create or replace function update_total_price_insert() returns trigger as
$$
BEGIN
    update orders
    set total_price = total_price + new.quantity * new.price
    where orders.id = new.order_id;
    return null;
end;
$$ language plpgsql;

create or replace function update_total_price_delete() returns trigger as
$$
BEGIN
    update orders
    set total_price = total_price - old.quantity * old.price
    where orders.id = old.order_id;
    return null;
end;
$$ language plpgsql;

create trigger update_total_price_insert_trigger
    after insert
    on orders_products
    for each row
execute procedure update_total_price_insert();

create trigger update_total_price_delete_trigger
    after delete
    on orders_products
    for each row
execute procedure update_total_price_delete();

create or replace function cascade_client_delete() returns trigger as
$$
BEGIN
    WITH client_orders AS (SELECT id
                           FROM orders
                           WHERE client_id = OLD.id)

    DELETE
    FROM orders_products
    WHERE order_id IN (SELECT id FROM client_orders);

    DELETE FROM orders WHERE client_id = OLD.id;

    return old;
end;
$$ language plpgsql;

create trigger cascade_client_delete_trigger
    before delete
    on clients
    for each row
execute procedure cascade_client_delete();

create or replace function cascade_product_delete() returns trigger as
$$
BEGIN
    delete
    from orders_products
    where product_id = old.id;

    return old;
end;
$$ language plpgsql;

create trigger cascade_product_delete_trigger
    before delete
    on products
    for each row
execute procedure cascade_product_delete();