# SQL

## Commandes de base

### SELECT
```sql
-- Sélection simple
SELECT column1, column2 FROM table_name;

-- Toutes les colonnes
SELECT * FROM users;

-- Avec alias
SELECT first_name AS prenom, last_name AS nom FROM users;

-- Distinct
SELECT DISTINCT country FROM customers;
```

### WHERE
```sql
-- Conditions simples
SELECT * FROM users WHERE age > 18;
SELECT * FROM products WHERE price BETWEEN 10 AND 50;
SELECT * FROM users WHERE name LIKE 'J%';
SELECT * FROM orders WHERE status IN ('pending', 'processing');

-- Conditions combinées
SELECT * FROM users WHERE age > 18 AND country = 'France';
SELECT * FROM users WHERE age < 18 OR is_admin = TRUE;

-- NULL
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;
```

### ORDER BY et LIMIT
```sql
SELECT * FROM products ORDER BY price DESC;
SELECT * FROM products ORDER BY category ASC, price DESC;
SELECT * FROM products LIMIT 10 OFFSET 20;
```

### INSERT
```sql
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');

-- Insertion multiple
INSERT INTO users (name, email) VALUES
    ('John', 'john@example.com'),
    ('Jane', 'jane@example.com');
```

### UPDATE
```sql
UPDATE users SET email = 'new@example.com' WHERE id = 1;
UPDATE products SET price = price * 1.1 WHERE category = 'electronics';
```

### DELETE
```sql
DELETE FROM users WHERE id = 1;
DELETE FROM logs WHERE created_at < '2024-01-01';
```

## Jointures

### INNER JOIN
```sql
SELECT orders.id, users.name, orders.total
FROM orders
INNER JOIN users ON orders.user_id = users.id;
```

### LEFT JOIN
```sql
SELECT users.name, COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id;
```

### RIGHT JOIN
```sql
SELECT orders.id, users.name
FROM orders
RIGHT JOIN users ON orders.user_id = users.id;
```

### FULL OUTER JOIN
```sql
SELECT * FROM table1
FULL OUTER JOIN table2 ON table1.id = table2.foreign_id;
```

### Self Join
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

## Agrégation

### Fonctions d'agrégation
```sql
SELECT COUNT(*) FROM users;
SELECT SUM(amount) FROM orders;
SELECT AVG(price) FROM products;
SELECT MIN(price), MAX(price) FROM products;
```

### GROUP BY
```sql
SELECT category, COUNT(*) as count, AVG(price) as avg_price
FROM products
GROUP BY category;
```

### HAVING
```sql
SELECT category, COUNT(*) as count
FROM products
GROUP BY category
HAVING COUNT(*) > 10;
```

## Sous-requêtes

```sql
-- Dans WHERE
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 100);

-- Dans FROM
SELECT avg_orders.category, avg_orders.avg_total
FROM (
    SELECT category, AVG(total) as avg_total
    FROM orders
    GROUP BY category
) as avg_orders;

-- Sous-requête corrélée
SELECT * FROM products p
WHERE price > (
    SELECT AVG(price) FROM products WHERE category = p.category
);
```

## Fonctions de fenêtre

```sql
-- ROW_NUMBER
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- PARTITION BY
SELECT department, name, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;

-- Running total
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;
```

## Index

```sql
-- Création
CREATE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Suppression
DROP INDEX idx_users_email;
```

## Transactions

```sql
BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;
-- ou ROLLBACK en cas d'erreur;
```

## Optimisation

### EXPLAIN
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### Bonnes pratiques
- Utiliser des index sur les colonnes fréquemment filtrées
- Éviter SELECT * en production
- Limiter les résultats avec LIMIT
- Utiliser des requêtes préparées contre les injections SQL
- Normaliser les données pour éviter la redondance
- Dénormaliser stratégiquement pour les performances de lecture
