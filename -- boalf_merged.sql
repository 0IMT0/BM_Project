-- boalf_merged
select bmra_boalf.id, bmra_boalflevel.ts, bmra_boalflevel.va, bmra_boalf.ts, bmra_boalf.ta, bmra_boalf.bmu_id, bmra_bmu.name, bmra_bmu.type_id from bmra_boalflevel
left join bmra_boalf
    on bmra_boalf.id = bmra_boalflevel.boalf_id
left join bmra_bmu
    on bmra_boalf.bmu_id = bmra_bmu.id
where bmra_boalflevel.ts = '2023-01-18 03:00'
order by bmra_boalflevel.ts;

