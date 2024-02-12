-- boav
select*
    from bmra_boav
where bmra_boav.ts >= '2023-01-01 00:00'
    and bmra_boav.ts <= '2023-01-31 23:59';
