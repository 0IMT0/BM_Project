-- fpn_merged
select bmra_fpnlevel.ts, bmra_fpnlevel.vp
    from bmra_fpnlevel
inner join bmra_fpn
    on bmra_fpn.id = bmra_fpnlevel.fpn_id
where bmra_fpn.sd >= '2023-01-01 00:00'
    and bmra_fpnlevel.ts <= '2023-02-01 00:00'
    and bmu_id = 'E_MOYEW-1'
order by bmra_fpnlevel.ts;
