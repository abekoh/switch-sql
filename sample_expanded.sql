select *
from (
  select *
  from salmon01.item
  where id = '1000'
  union all
  select *
  from salmon02.item
  where id = '1000'
)
