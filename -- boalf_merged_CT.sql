-- boalf_merged_CT
select bmra_boalflevel.ts, bmra_boalflevel.va, bmra_boalf.bmu_id, bmra_bmu.type_id
    from bmra_boalflevel
left join bmra_boalf
    on bmra_boalf.id = bmra_boalflevel.boalf_id
left join bmra_bmu
    on bmra_boalf.bmu_id = bmra_bmu.id
where bmra_boalflevel.ts >= '2023-09-27'
    and bmra_boalflevel.ts <= '2023-09-28'
--    and bmu_id = 'E_MOYEW-1'
order by bmra_boalflevel.ts;