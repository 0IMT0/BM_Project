SELECT bmra_boalf.ts, bmra_boalf.bmu_id
FROM bmra_boalf
INNER JOIN bmra_bmu ON bmra_boalf.bmu_id = bmra_bmu.id
WHERE bmra_boalf.ts >= '2023-01-01'
    AND bmra_boalf.ts < '2023-01-02'
    AND bmra_bmu.type_id = 'BATT'
ORDER BY bmra_boalf.ts;