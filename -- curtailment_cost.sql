select bmra_ebocf.sd, bmra_ebocf.bc, bmra_ebocf.bmu_id 
    from bmra_ebocf
inner join bmra_bmu
    on bmra_bmu.id = bmra_ebocf.bmu_id
where bmra_ebocf.sd >= '2023-01-01'
    and bmra_ebocf.sd < '2024-01-01'
    and (bmra_bmu.type_id = 'WON' or bmra_bmu.type_id = 'WOFF')
    and bmra_ebocf.nn < 1
order by bmra_ebocf.sd, bmra_ebocf.sp;
