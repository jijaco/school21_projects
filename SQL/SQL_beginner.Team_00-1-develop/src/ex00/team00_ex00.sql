CREATE TABLE cost_way
(
point1 VARCHAR NOT NULL,
point2 VARCHAR NOT NULL,
cost BIGINT
);
INSERT INTO cost_way values ('A', 'B', 10);
INSERT INTO cost_way values ('B', 'A', 10);
---------------------------
INSERT INTO cost_way values ('B', 'C', 35);
INSERT INTO cost_way values ('C', 'B', 35);
---------------------------
INSERT INTO cost_way values ('B', 'D', 25);
INSERT INTO cost_way values ('D', 'B', 25);
---------------------------
INSERT INTO cost_way values ('D', 'C', 30);
INSERT INTO cost_way values ('C', 'D', 30);
---------------------------
INSERT INTO cost_way values ('A', 'D', 20);
INSERT INTO cost_way values ('D', 'A', 20);
---------------------------
INSERT INTO cost_way values ('A', 'C', 15);
INSERT INTO cost_way values ('C', 'A', 15);


WITH RECURSIVE solution(point1, point2, path, cost, recurisve_depth) AS (
    SELECT
    cost_way.point1, cost_way.point2, (cost_way.point1 || '->' || cost_way.point2) AS path, cost_way.cost, 0 AS recurisve_depth
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
WHERE point2 = 'A' AND recurisve_depth > 2 AND cost =(SELECT MIN(cost) FROM solution WHERE point2 = 'A' AND recurisve_depth > 2)
ORDER BY 1,2;
