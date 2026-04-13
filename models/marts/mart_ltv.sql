with activity as (
    select * from {{ ref('int_customer_activity') }}
),

monthly as (
    select * from {{ ref('int_monthly_revenue') }}
),

-- LTV cumulée mois par mois
cumulative as (
    select
        customer_id,
        month_start,
        total_revenue,
        sum(total_revenue) over (
            partition by customer_id
            order by month_start
            rows between unbounded preceding and current row
        )                                  as ltv_cumulative
    from monthly
),

final as (
    select
        c.customer_id,
        c.shop_name,
        c.country,
        c.plan_name,
        c.first_transaction_date,
        c.last_transaction_date,
        c.active_months,
        c.total_transactions,
        c.total_gmv,
        c.total_revenue_generated,
        c.tenure_months,
        cu.month_start,
        cu.total_revenue                    as monthly_revenue,
        cu.ltv_cumulative                   as ltv,

        -- Revenu moyen par mois (ARPU)
        round(
            c.total_revenue_generated / nullif(c.active_months, 0)
        , 2)                                as arpu

    from activity c
    left join cumulative cu on c.customer_id = cu.customer_id
)

select * from final