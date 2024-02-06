-- mel
select bmra_mellevel.ts, bmra_mellevel.ve, bmra_mel.bmu_id
from bmra_mellevel
left join bmra_mel
    on bmra_mellevel.mel_id = bmra_mel.id
where bmra_mellevel.ts = '2023-01-18 03:00';

