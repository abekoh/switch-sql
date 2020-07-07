select *
from (
  select count(*)
  from salmon01.item
  where id = '1000'
  union all
  select count(*)
  from salmon02.item
  where id = '1000'
)
