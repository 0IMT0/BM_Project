-- fpn_merged_CT
select bmra_fpnlevel.ts, bmra_fpn.sd, bmra_fpn.sp, bmra_fpnlevel.vp
    from bmra_fpnlevel
inner join bmra_fpn
    on bmra_fpn.id = bmra_fpnlevel.fpn_id
where bmra_fpn.sd >= '2023-01-01'
    and bmra_fpn.sd <= '2023-01-02'
    and bmu_id = 'E_MOYEW-1'
order by bmra_fpnlevel.ts;
