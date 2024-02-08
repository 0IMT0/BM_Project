-- mil
select bmra_millevel.ts, bmra_millevel.vf, bmra_mil.bmu_id
from bmra_millevel
left join bmra_mil
    on bmra_millevel.mil_id = bmra_mil.id
where bmra_millevel.ts = '2023-01-18 03:00';