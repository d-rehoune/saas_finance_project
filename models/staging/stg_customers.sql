with source as (
    select * from {{ source('raw', 'raw_customers') }}
),

renamed as (
    select
        customer_id,
        shop_name,
        country,
        cast(created_at as date) as created_at
    from source
)

select * from renamed