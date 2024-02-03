-- bids
select bmra_bod.nn, bmra_bod.op, bmra_bod.bp, bmra_bod.vb1, bmra_bod.vb2, bmra_bmu.id, bmra_bmu.name, bmra_bmu.type_id  
from bmra_bod
left join bmra_bmu
    on bmra_bod.bmu_id = bmra_bmu.id
where ts1 = '2023-01-18 03:00'
    and nn < 0
    and not (op = 0 AND bp = 0 AND vb1 = 0 AND vb2 = 0)
order by bp desc;