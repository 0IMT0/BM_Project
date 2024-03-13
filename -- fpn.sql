-- fpnlevel
select bmra_fpn.sd, bmra_fpn.sd, bmra_fpnlevel.vp
    from bmra_fpnlevel
left join bmra_fpn
    on bmra_fpn.id = bmra_fpnlevel.fpn_id
where bmra_fpnlevel.ts = '2023-01-18 03:00'
order by sd, sp;