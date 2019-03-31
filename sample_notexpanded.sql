select *
from (
  select *
  from salmon##.item
  where id = '1000'
)
