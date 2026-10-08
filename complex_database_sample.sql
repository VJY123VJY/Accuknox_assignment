CREATE TABLE IF NOT EXISTS tenants (
    tenant_id SERIAL PRIMARY KEY,
    tenant_name VARCHAR(100) NOT NULL UNIQUE,
    subscription_tier VARCHAR(20) NOT NULL DEFAULT 'standard' CHECK (subscription_tier IN ('free', 'standard', 'enterprise')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    sku VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_tenant_sku UNIQUE (tenant_id, sku)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id BIGSERIAL PRIMARY KEY,
    tenant_id INT NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    order_status VARCHAR(30) NOT NULL DEFAULT 'pending' CHECK (order_status IN ('pending', 'processing', 'completed', 'cancelled')),
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00 CHECK (total_amount >= 0),
    order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id) ON DELETE RESTRICT,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    subtotal NUMERIC(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

CREATE INDEX IF NOT EXISTS idx_orders_tenant_status_date 
ON orders (tenant_id, order_status, order_date DESC);

CREATE INDEX IF NOT EXISTS idx_users_active_tenant 
ON users (tenant_id, email) 
WHERE is_active = TRUE;

CREATE INDEX IF NOT EXISTS idx_products_tenant_category 
ON products (tenant_id, category);

WITH monthly_sales_agg AS (
    SELECT 
        o.tenant_id,
        t.tenant_name,
        DATE_TRUNC('month', o.order_date) AS sales_month,
        COUNT(o.order_id) AS total_orders,
        SUM(o.total_amount) AS monthly_revenue
    FROM orders o
    JOIN tenants t ON o.tenant_id = t.tenant_id
    WHERE o.order_status = 'completed'
    GROUP BY o.tenant_id, t.tenant_name, DATE_TRUNC('month', o.order_date)
),
sales_with_trends AS (
    SELECT
        tenant_name,
        sales_month,
        total_orders,
        monthly_revenue,
        SUM(monthly_revenue) OVER (
            PARTITION BY tenant_name 
            ORDER BY sales_month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_tenant_revenue,
        LAG(monthly_revenue, 1) OVER (
            PARTITION BY tenant_name 
            ORDER BY sales_month
        ) AS previous_month_revenue
    FROM monthly_sales_agg
),
top_customers_ranked AS (
    SELECT
        u.tenant_id,
        u.user_id,
        u.full_name,
        SUM(o.total_amount) AS total_spend,
        DENSE_RANK() OVER (
            PARTITION BY u.tenant_id 
            ORDER BY SUM(o.total_amount) DESC
        ) AS spender_rank
    FROM users u
    JOIN orders o ON u.user_id = o.user_id
    WHERE o.order_status = 'completed'
    GROUP BY u.tenant_id, u.user_id, u.full_name
)
SELECT 
    tenant_name,
    TO_CHAR(sales_month, 'YYYY-MM') AS month_label,
    total_orders,
    monthly_revenue,
    cumulative_tenant_revenue,
    ROUND(
        COALESCE(
            ((monthly_revenue - previous_month_revenue) / NULLIF(previous_month_revenue, 0)) * 100,
            0
        ), 2
    ) AS mom_growth_percentage
FROM sales_with_trends
ORDER BY tenant_name, sales_month;
