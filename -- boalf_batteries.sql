-- boalf_merged
select bmra_boalf.ts, bmra_boalf.bmu_id, bmra_boalflevel.va
    from bmra_boalf
left join bmra_boalflevel
    on bmra_boalflevel.boalf_id = bmra_boalf.id
inner join bmra_bmu
    on bmra_boalf.bmu_id = bmra_bmu.id
where bmra_boalf.ts >= '2023-01-01'
    and bmra_boalf.ts < '2023-01-02'
    and bmra_bmu.type_id = 'BATT'
order by bmra_boalf.ts, bmra_boalflevel.ts; 