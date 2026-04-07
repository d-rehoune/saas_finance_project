with enriched as (
    select * from {{ ref('int_transactions_enriched') }}
),

monthly as (
    select
        transaction_month                               as month_start,
        customer_id,
        shop_name,
        country,
        plan_name,
        monthly_fixed_fee,

        -- Volume
        count(transaction_id)                           as total_transactions,
        sum(case when is_success then amount else 0 end) as gmv,

        -- Revenus FlowPay
        sum(flowpay_revenue)                            as transactional_revenue,
        monthly_fixed_fee                               as subscription_revenue,
        sum(flowpay_revenue) + monthly_fixed_fee        as total_revenue,

        -- Chargebacks
        sum(is_chargeback)                              as nb_chargebacks,
        sum(case when is_chargeback = 1
                 then abs(net_amount) else 0 end)       as chargeback_amount
    from enriched
    group by 1, 2, 3, 4, 5, 6
)

select * from monthly