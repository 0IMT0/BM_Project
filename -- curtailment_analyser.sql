-- curtailment
select bmra_boav.ts, bmra_boav.nn, bmra_boav.bv, bmra_boav.bmu_id, bmra_bmu.type_id
    from bmra_boav
left join bmra_bmu
    on bmra_bmu.id = bmra_boav.bmu_id
where bmra_boav.ts >= '2023-01-01'
    and bmra_boav.ts < '2023-01-02'
    and (bmra_bmu.type_id = 'WON' OR bmra_bmu.type_id = 'WOFF')
order by bmra_boav.ts;
