select coalesce(u.name, 'not defined')     as name,
       coalesce(u.lastname, 'not defined') as lastname,
       cur.name                            as currency_name,
       cur.money * coalesce(min, max)      as currency_in_usd
from (select name, user_id, money,
             (select currency.rate_to_usd
              from currency
              where currency.id = b.currency_id
                and currency.updated <= b.updated
              order by rate_to_usd
              limit 1) as min,
             (select currency.rate_to_usd
              from currency
              where currency.id = b.currency_id
                and currency.updated > b.updated
              order by rate_to_usd
              limit 1) as max
    from currency c
    join balance b on c.id = b.currency_id
    group by b.user_id, currency_id, b.updated, name, money) cur
left join "user" u on cur.user_id = u.id
order by name desc,
         lastname,
         currency_name;