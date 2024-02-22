-- real_generation_CT
select distinct p114_abv.sd as sd, p114_abp.sp as sp, vol 
    from p114_abv 
    left join p114_abp 
    on p114_abv.id = p114_abp.abv_id 
    left join p114_sr_type 
    on p114_abv.sr_type_id = p114_sr_type.id 
    inner join 
    (SELECT sd, sp, max(p114_sr_type.order) as ordinal 
    FROM p114_abv 
    left join p114_abp 
    on p114_abv.id = p114_abp.abv_id 
    left join p114_sr_type 
    on p114_abv.sr_type_id = p114_sr_type.id 
    where bmu_id='E_MOYEW-1' 
    and p114_abv.sd>='2023-01-01' 
    and p114_abv.sd<'2023-01-02' 
    group by sd, sp 
    order by sd, sp) as inner_query 
    on inner_query.sd = p114_abv.sd 
    and inner_query.sp = p114_abp.sp 
    and inner_query.ordinal = p114_sr_type.order 
    where bmu_id='E_MOYEW-1' 
    and p114_abv.sd>='2023-01-01' 
    and p114_abv.sd<'2023-01-02' 
    order by sd, sp;
