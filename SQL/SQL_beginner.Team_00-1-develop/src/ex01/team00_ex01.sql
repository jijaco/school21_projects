WITH RECURSIVE solution(point1, point2, path, cost, recurisve_depth) AS (
    SELECT
    cost_way.point1, cost_way.point2, (cost_way.point1 || '->' || cost_way.point2) AS path  , cost_way.cost, 0 AS recurisve_depth
    FROM cost_way
    WHERE point1 = 'A'
    UNION
    SELECT
    cost_way.point1, cost_way.point2, (solution.path || '->' || cost_way.point2), solution.cost + cost_way.cost, recurisve_depth + 1
    FROM solution
    INNER JOIN cost_way ON cost_way.point1 = solution.point2
    WHERE  recurisve_depth < 3 AND cost_way.point2 NOT IN(solution.point1)
)
SELECT cost AS total_cost, path as tour FROM solution
WHERE point2 = 'A' AND recurisve_depth > 2
ORDER BY 1,2;