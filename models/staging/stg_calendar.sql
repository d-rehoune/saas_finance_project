with dates as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2024-01-01' as date)",
        end_date="cast('2026-01-01' as date)"
    ) }}
),

calendar as (
    select
        cast(date_day as date)                        as date_day,
        year(date_day)                                as year,
        month(date_day)                               as month_number,
        day(date_day)                                 as day_number,
        date_trunc('month', date_day)                 as month_start,
        last_day(date_day)                            as month_end,
        quarter(date_day)                             as quarter_number,
        'Q' || quarter(date_day)                      as quarter_label,
        year(date_day) || '-' || lpad(month(date_day), 2, '0') as year_month,
        dayofweek(date_day)                           as day_of_week,
        case when dayofweek(date_day) in (0, 6)
             then true else false end                 as is_weekend
    from dates
)

select * from calendar