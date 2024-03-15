-- bod
SELECT *
FROM bmra_bod
WHERE sd = '2023-01-18'
    AND sp = 30
    AND nn > 0
    AND NOT (op = 0 AND bp = 0 AND vb1 = 0 AND vb2 = 0);

