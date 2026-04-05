with source as (
    select * from {{ source('raw', 'raw_subscriptions') }}
),

renamed as (
    select
        subscription_id,
        customer_id,
        plan_name,
        monthly_fixed_fee,
        commission_rate,
        per_transaction_fee,
        status,
        cast(subscription_start_date as date) as subscription_start_date,
        cast(subscription_end_date   as date) as subscription_end_date,

        -- champ calculé utile pour la suite
        case when status = 'active' then true else false end as is_active
    from source
)

select * from renamed