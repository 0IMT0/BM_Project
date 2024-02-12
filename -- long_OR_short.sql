-- long_OR_short
select bmra_disebsp.sd, bmra_disebsp.sp, bmra_disebsp.pd
    from bmra_disebsp
where bmra_disebsp.sd = '2023-03-05'
order by bmra_disebsp.sp;
