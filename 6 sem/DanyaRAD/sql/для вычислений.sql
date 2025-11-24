SELECT 
    p.title AS "Название товара",
    p.ed AS "Единица измерения",
    COUNT(op.order_id) AS "Количество заказов",
    SUM(op.price * op.quantity) AS "Общая сумма",
    SUM(CASE WHEN op.isDelivered THEN 1 ELSE 0 END) AS "Доставлено",
    SUM(CASE WHEN NOT op.isDelivered THEN 1 ELSE 0 END) AS "Не доставлено"
FROM 
    Products p
LEFT JOIN 
    Orders_Products op ON p.id = op.product_id
LEFT JOIN 
    Orders o ON op.order_id = o.id
where date>=to_date(:leftBorderDate) and date<=to_date(:rightBorderDate)
GROUP BY 
    p.title, p.ed
ORDER BY 
    "Общая сумма" DESC;