with source as (
    select * from {{ source('raw', 'raw_transactions') }}
),

renamed as (
    select
        transaction_id,
        customer_id,
        subscription_id,
        cast(transaction_date as timestamp) as transaction_date,
        date_trunc('month', cast(transaction_date as timestamp)) as transaction_month,
        amount,
        net_amount,
        currency,
        payment_method,
        status,
        flowpay_revenue,
        is_chargeback,

        -- flags utiles
        case when status = 'success'    then true else false end as is_success,
        case when status = 'failed'     then true else false end as is_failed
    from source
)

select * from renamed