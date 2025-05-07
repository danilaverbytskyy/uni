insert into clients (id, name, address, phone)
values (1, 'Даня Вербицкий', 'Ставропольская 107/5', '+79883589734');

insert into clients (id, name, address, phone)
values (2, 'Эмилия Марковна', 'Ставропольская 107/5', '89782263905');

insert into clients (id, name, address, phone)
values (3, 'Паатов Владислав', 'г.Майкоп', '+89782263905');

insert into products (id, title, ed)
VALUES (1, 'Латте', 'литр');
insert into products (id, title, ed)
VALUES (2, 'Творожное колечко', 'штук');
insert into products (id, title, ed)
VALUES (3, 'Трубочка со сгущенкой', 'штук');

insert into orders (id, client_id, total_price, date)
VALUES (1, 1, 0, to_date('2025-04-20 22:30:00', 'YYYY-MM-DD HH24:MI:SS'));
insert into orders (id, client_id, total_price, date)
VALUES (2, 2, 0, to_date('2025-04-20 22:30:00', 'YYYY-MM-DD HH24:MI:SS'));
insert into orders (id, client_id, total_price, date)
VALUES (3, 2, 0, to_date('2025-04-20 22:30:00', 'YYYY-MM-DD HH24:MI:SS'));

insert into orders_products(order_id, product_id, price, quantity, isdelivered)
VALUES (1, 1, 100, 13, true);
insert into orders_products(order_id, product_id, price, quantity, isdelivered)
VALUES (2, 2, 15, 25, false);
insert into orders_products(order_id, product_id, price, quantity, isdelivered)
VALUES (2, 2, 150, 25, false);