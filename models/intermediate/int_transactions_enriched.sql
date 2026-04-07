with transactions as (
    select * from {{ ref('stg_transactions') }}
),

subscriptions as (
    select * from {{ ref('stg_subscriptions') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

final as (
    select
        t.transaction_id,
        t.transaction_date,
        t.transaction_month,
        t.customer_id,
        c.shop_name,
        c.country,
        s.plan_name,
        s.monthly_fixed_fee,
        s.commission_rate,
        s.per_transaction_fee,
        t.amount,
        t.net_amount,
        t.payment_method,
        t.status,
        t.flowpay_revenue,
        t.is_chargeback,
        t.is_success,
        t.is_failed
    from transactions t
    left join subscriptions s on t.customer_id = s.customer_id
    left join customers c     on t.customer_id = c.customer_id
)

select * from final