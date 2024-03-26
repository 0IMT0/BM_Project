-- boalf
select*
    from bmra_boalflevel
where ts >= '2023-01-01 00:00'
    and ts <= '2023-01-31 23:59'
order by ts;