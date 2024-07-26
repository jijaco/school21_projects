with currency_last_usd_rate as (
    select distinct *
    from currency
    order by updated desc,
             id
    limit (select count(*) from (select distinct id from currency) all_id)
),   transactions_sum as (
    select user_id, type, currency_id, sum(money) as volume
    from balance
    group by user_id, type, currency_id
    order by user_id,
             type
     )
select coalesce(u.name, 'not defined')          as name,
       coalesce(u.lastname, 'not defined')      as lastname,
       ts.type,
       ts.volume,
       c.name                                   as currency_name,
       coalesce(c.rate_to_usd, 1)               as last_rate_to_usd,
       (coalesce(c.rate_to_usd, 1) * ts.volume) as total_volume_in_usd
from "user" u
full join transactions_sum ts on u.id = ts.user_id
full join currency_last_usd_rate c on c.id = ts.currency_id
order by name desc,
         lastname,
         type;
