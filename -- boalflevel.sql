-- boalflevel
select*
from bmra_boalflevel
where bmra_boalflevel.ts >= '2023-01-01 00:00'
    and bmra_boalflevel.ts <= '2023-01-31 23:59';