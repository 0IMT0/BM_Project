-- fpn
select bmra_fpnlevel.ts, bmra_fpnlevel.vp, bmra_fpn.bmu_id
    from bmra_fpnlevel
left join bmra_fpn
    on bmra_fpn.id = bmra_fpnlevel.fpn_id
where bmra_fpnlevel.ts = '2023-01-18 03:00'
order by bmra_fpnlevel.ts;