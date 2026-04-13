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
        gmv,
        transactional_revenue,
        subscription_revenue,
        total_revenue,

        -- Net Take Rate
        coalesce(round(total_revenue / nullif(gmv, 0) * 100, 2), 0) as net_take_rate_pct

    from monthly
)

select * from final