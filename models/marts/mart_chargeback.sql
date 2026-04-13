with monthly as (
    select * from {{ ref('int_monthly_revenue') }}
),

final as (
    select
        month_start,
        customer_id,
        shop_name,
        country,
        plan_name,
        total_transactions,
        nb_chargebacks,
        chargeback_amount,
        gmv,

        -- Default Rate
        round(nb_chargebacks / nullif(total_transactions, 0) * 100, 2) as default_rate_pct,

        -- Impact chargeback sur le GMV
        round(chargeback_amount / nullif(gmv, 0) * 100, 2)             as chargeback_impact_pct

    from monthly
)

select * from final