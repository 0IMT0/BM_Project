-- boalf_merged_CT
select bmra_boalflevel.ts, bmra_boalflevel.va, bmra_boalf.bmu_id 
    from bmra_boalflevel
left join bmra_boalf
    on bmra_boalf.id = bmra_boalflevel.boalf_id
where bmra_boalflevel.ts >= '2023-01-01'
    and bmra_boalflevel.ts <= '2023-01-01'
    and bmu_id = 'E_MOYEW-1'
order by bmra_boalflevel.ts;