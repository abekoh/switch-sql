select *
from (
  select count(*)
  from salmon##.item
  where id = '1000'
)
