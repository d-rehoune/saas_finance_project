with enriched as (
    select * from {{ ref('int_transactions_enriched') }}
),

subscriptions as (
    select * from {{ ref('stg_subscriptions') }}
),

activity as (
    select
        customer_id,
        shop_name,
        country,
        plan_name,
        min(transaction_date)                           as first_transaction_date,
        max(transaction_date)                           as last_transaction_date,
        count(distinct transaction_month)               as active_months,
        count(transaction_id)                           as total_transactions,
        sum(case when is_success then amount else 0 end) as total_gmv,
        sum(flowpay_revenue)                            as total_revenue_generated,

        -- Ancienneté en mois
        datediff('month', min(transaction_date), max(transaction_date)) as tenure_months
    from enriched
    group by 1, 2, 3, 4
)

select * from activity