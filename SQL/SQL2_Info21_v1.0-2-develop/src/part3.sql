DROP FUNCTION IF EXISTS fnc_readable_transferred_points;

CREATE OR REPLACE FUNCTION fnc_readable_transferred_points()
RETURNS TABLE(Peer1 VARCHAR, Peer2 VARCHAR, "PointsAmount" BIGINT) AS $$
BEGIN
	RETURN QUERY
	WITH reversed AS (
		SELECT
			CASE WHEN CheckingPeer > CheckedPeer THEN CheckingPeer ELSE CheckedPeer END AS CheckingPeer,
			CASE WHEN CheckingPeer > CheckedPeer THEN CheckedPeer ELSE CheckingPeer END AS CheckedPeer,
			CASE WHEN CheckingPeer > CheckedPeer THEN PointsAmount ELSE -PointsAmount END AS PointsAmount
		FROM TransferredPoints
	)
	SELECT CheckingPeer AS peer1, CheckedPeer AS Peer2, SUM(PointsAmount) FROM reversed
	GROUP BY CheckingPeer, CheckedPeer;
END;
$$ LANGUAGE plpgsql;

--select * from fnc_readable_transferred_points()


-----------------------------------------------------------------------------------------------------------------------------
drop function if exists fnc_checks_xp;

create or replace function fnc_checks_xp()
returns table (peer varchar, Task varchar, "XPAmount" INT) as $$
Begin
return query
select checks.peer as Peer, checks.task as Task, XPAmount as XP
from XP
JOIN Checks on Checks.id = XP."Check";
END
$$ language plpgsql;

--select * from fnc_checks_xp()
 -----------------------------------------------------------------------------------------------


drop function if exists fnc_not_left_students(d date);

create or replace function fnc_not_left_students(d date)
returns table (peer varchar) as $$
begin
return query
with s as(select timetracking.peer, count(timetracking.state) c, timetracking.date from timetracking
		 WHERE state = 2 AND date = date GROUP BY timetracking.peer, timetracking.date)
		 SELECT s.peer FROM s WHERE c = 1;

End;
$$ LANGUAGE plpgsql;

--select fnc_not_left_students('2021-07-27')

---------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION calculate_change_in_points()
RETURNS TABLE (PeerNickname VARCHAR, ChangeInPoints numeric) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.Nickname AS PeerNickname,
        COALESCE(SUM(tp.PointsAmount), 0) AS ChangeInPoints
    FROM
        Peers p
    LEFT JOIN
        (
            SELECT
                CheckingPeer AS Peer,
                SUM(PointsAmount) AS PointsAmount
            FROM
                TransferredPoints
            GROUP BY
                CheckingPeer

            UNION ALL

            SELECT
                CheckedPeer AS Peer,
                -SUM(PointsAmount) AS PointsAmount
            FROM
                TransferredPoints
            GROUP BY
                CheckedPeer
        ) tp ON p.Nickname = tp.Peer
    GROUP BY
        p.Nickname
    ORDER BY
        ChangeInPoints DESC;

    RETURN;
END;
$$ LANGUAGE plpgsql;

--SELECT * FROM calculate_change_in_points();


--------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION prp_change_short_method()
RETURNS TABLE(Peer VARCHAR, PointsChange NUMERIC) AS $$
BEGIN
	RETURN QUERY
	WITH sums AS (
		SELECT Peer1 AS Peer, SUM("PointsAmount") AS PointsChange
		FROM fnc_readable_transferred_points()
		GROUP BY Peer1
		UNION
		SELECT Peer2 AS Peer, -SUM("PointsAmount") AS PointsChange
		FROM fnc_readable_transferred_points()
		GROUP BY Peer2
	)
	SELECT sums.Peer, SUM(sums.PointsChange)
	FROM sums
	GROUP BY sums.Peer;
END;
$$ LANGUAGE plpgsql;
--select * from prp_change_short_method();

--------------------------------------------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS most_checked_tasks(c refcursor);
CREATE OR REPLACE PROCEDURE most_checked_tasks(
    IN c refcursor
)
LANGUAGE plpgsql AS $most_checked_tasks$
    BEGIN
        OPEN c for
        WITH counted_checks AS (SELECT task, date, count(task) amount FROM checks GROUP BY task, date),
        max_count AS (SELECT cc.task, cc.date, cc.amount FROM counted_checks cc
        WHERE amount = (SELECT max(amount) FROM counted_checks WHERE counted_checks.date = cc.date))
        SELECT date, task FROM  max_count ORDER BY date;
    end;
    $most_checked_tasks$;

--BEGIN ;
--call most_checked_tasks('2');
--FETCH ALL IN "2";
--end;

----------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION finished_block(
    IN pblock VARCHAR
)
RETURNS TABLE (Peer VARCHAR, Day DATE) AS $$
BEGIN
    --RAISE NOTICE 'Block: %', pblock;

    RETURN QUERY
    WITH cur_block AS (
        SELECT Task
        FROM Checks
        WHERE Task LIKE '%' || pblock || '%'
    )
    SELECT
        c.Peer,
        MAX(c.Date) AS Day
    FROM
        cur_block cb
    JOIN
        Checks c ON c.Task = cb.Task
    JOIN
        XP x ON c.ID = x."Check"
    GROUP BY
        c.Peer;

    --RAISE NOTICE 'Query executed successfully';
END;
$$ LANGUAGE plpgsql;
--SELECT * FROM finished_block('SQL'); 

------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION best_checkers()
RETURNS TABLE(Peer VARCHAR, RecommendedPeer VARCHAR) AS $$
BEGIN
RETURN QUERY
	WITH friends_recommend AS (
		SELECT Recommendations.Peer, Recommendations.RecommendedPeer, COUNT(Recommendations.RecommendedPeer) AS recoms
		FROM Recommendations
		GROUP BY Recommendations.Peer, Recommendations.RecommendedPeer
	),
	peer_recom_counts AS (
		SELECT friends_recommend.RecommendedPeer, COUNT(friends_recommend.RecommendedPeer) AS total_recoms, Friends.Peer1 AS Peer
		FROM friends_recommend
		LEFT JOIN Friends ON friends_recommend.Peer = Friends.Peer2
		WHERE Friends.Peer1 != friends_recommend.RecommendedPeer
		GROUP BY friends_recommend.RecommendedPeer, friends_recommend.Peer,Friends.Peer1
	),
	result_table AS (
		SELECT peer_recom_counts.Peer, peer_recom_counts.RecommendedPeer, total_recoms, 
			ROW_NUMBER() OVER (PARTITION BY peer_recom_counts.Peer ORDER BY COUNT(*) DESC) AS rank
		FROM peer_recom_counts
		WHERE total_recoms = (SELECT MAX(total_recoms) 
						FROM peer_recom_counts) AND peer_recom_counts.Peer != peer_recom_counts.RecommendedPeer
		GROUP BY peer_recom_counts.Peer, peer_recom_counts.RecommendedPeer, total_recoms
		ORDER BY peer_recom_counts.Peer ASC
	)
	SELECT result_table.Peer, result_table.RecommendedPeer
	FROM result_table
	WHERE rank = 1;
END;
$$ LANGUAGE plpgsql;

--select * from best_checkers();


-------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION blocks_percentage(pblock1 VARCHAR, pblock2 VARCHAR)
RETURNS TABLE (StartedBlock1 BIGINT, StartedBlock2 BIGINT, StartedBothBlocks BIGINT, DidntStatrAnyBlocks BIGINT) AS $$
BEGIN
RETURN QUERY
	WITH started_first AS (
		SELECT DISTINCT Peer
		From Checks
		WHERE Task LIKE '%' || pblock1 || '%'
	),
	started_second AS (
		SELECT DISTINCT Peer
		From Checks
		WHERE Task LIKE '%' || pblock2 || '%'
	),
	started_only_first AS(
		SELECT *
		FROM started_first
		LEFT JOIN started_second ON started_second.Peer = started_first.Peer
		WHERE started_second.Peer IS NULL
	),
	started_only_second AS(
		SELECT *
		FROM started_second
		LEFT JOIN started_first ON started_second.Peer = started_first.Peer
		WHERE started_first.Peer IS NULL
	),
	started_both AS (
		SELECT *
		FROM started_first
		INTERSECT
		SELECT *
		FROM started_second
	),
	didnt_start AS (
		SELECT Nickname
		FROM Peers
		WHERE Nickname NOT IN (SELECT * FROM started_first) AND Nickname NOT IN (SELECT * FROM started_second)
	)
	SELECT 100 * (SELECT COUNT(*)
			FROM started_only_first) / 
			(SELECT COUNT(*) 
			FROM Peers), 
			100 * (SELECT COUNT(*)
			FROM started_only_second) / 
			(SELECT COUNT(*) 
			FROM Peers),
			100 * (SELECT COUNT(*)
			FROM started_both) / 
			(SELECT COUNT(*) 
			FROM Peers),
			100 * (SELECT COUNT(*)
			FROM didnt_start) / 
			(SELECT COUNT(*) 
			FROM Peers)
	FROM started_first, started_second, started_both, didnt_start
	LIMIT 1;
END;
$$ LANGUAGE plpgsql;

--select * from blocks_percentage ('A', 'C');  
-- 10

DROP PROCEDURE IF EXISTS get_perc_birthday_success_and_failure CASCADE;
CREATE PROCEDURE get_perc_birthday_success_and_failure(cursor refcursor default 'cursor') AS
$$
BEGIN
    OPEN cursor FOR
        SELECT 
            COUNT(CASE WHEN current_status = 'Success' THEN current_status ELSE NULL END) * 100 / COUNT(*) AS SuccessfulChecks,
            COUNT(CASE WHEN current_status = 'Failure' THEN current_status ELSE NULL END) * 100 / COUNT(*) AS UnsuccessfulChecks
        FROM 
        ( SELECT DISTINCT p.nickname, c.id,
            COALESCE(FIRST_VALUE(v.State) OVER(PARTITION BY c.id ORDER BY v.Time DESC),
                    FIRST_VALUE(p2p.State) OVER(PARTITION BY c.id ORDER BY p2p.Time DESC)) AS current_status
        FROM peers AS p
        LEFT JOIN Checks AS c ON p.nickname = c.peer
        LEFT JOIN p2p ON c.id = p2p."Check"
        LEFT JOIN verter AS v ON c.id = v."Check"
        WHERE to_char(p.birthday, 'dd-mm') = to_char(c.date, 'dd-mm')) AS A
        WHERE current_status IN ('Success', 'Failure');
END $$ LANGUAGE plpgsql;

BEGIN;
CALL get_perc_birthday_success_and_failure();
FETCH ALL FROM "cursor";
END;


-- 11

DROP PROCEDURE IF EXISTS get_peers_success_2_of_3_tasks CASCADE;
CREATE PROCEDURE get_peers_success_2_of_3_tasks(task1 VARCHAR, task2 VARCHAR, task3 VARCHAR, cursor refcursor default 'cursor') AS
$$
BEGIN
    OPEN cursor FOR
        WITH peers_tasks_x_status AS (
            SELECT nickname, ARRAY_AGG(task_x_status)::text AS tasks_x_status FROM (
                SELECT DISTINCT p.nickname, CONCAT(c.task, '-',
                    COALESCE(FIRST_VALUE(v.State) OVER(PARTITION BY c.id ORDER BY v.Time DESC),
                            FIRST_VALUE(p2p.State) OVER(PARTITION BY c.id ORDER BY p2p.Time DESC))) AS task_x_status
                FROM peers AS p
                LEFT JOIN Checks AS c ON p.nickname = c.peer
                LEFT JOIN p2p ON c.id = p2p."Check"
                LEFT JOIN verter AS v ON c.id = v."Check"
            ) AS A
            GROUP BY nickname
        )

        SELECT nickname
        FROM peers_tasks_x_status
        WHERE tasks_x_status LIKE CONCAT('%', task1, '-', 'Success', '%') AND
            tasks_x_status LIKE CONCAT('%', task2, '-', 'Success', '%') AND
            tasks_x_status LIKE CONCAT('%', task3, '-', 'Failure', '%');
END $$ LANGUAGE plpgsql;

BEGIN;
CALL get_peers_success_2_of_3_tasks('C3_s21_string+', 'C2_SimpleBashUtils', 'C4_s21_math');
FETCH ALL FROM "cursor";
END;

-- 12

DROP PROCEDURE IF EXISTS get_task_x_prev CASCADE;
CREATE PROCEDURE get_task_x_prev(cursor refcursor default 'cursor') AS
$$
BEGIN
    OPEN cursor FOR
        WITH RECURSIVE parent AS (
            SELECT 'C2_SimpleBashUtils'::VARCHAR AS Task, 0 AS PrevCount
            UNION ALL
            SELECT t.title, PrevCount + 1
            FROM parent AS p
            JOIN tasks t ON t.parenttask = p.Task
        )
        SELECT *
        FROM parent;
END $$ LANGUAGE plpgsql;

BEGIN;
CALL get_task_x_prev();
FETCH ALL FROM "cursor";
END;

-- 13

DROP PROCEDURE IF EXISTS prc_lucky_day CASCADE;
CREATE OR REPLACE PROCEDURE prc_lucky_day(N INT, cursor refcursor default 'cursor') AS
$$
BEGIN
    OPEN cursor FOR
        WITH days_x_count AS (
            SELECT
                "date", current_status,
                ROW_NUMBER() OVER(PARTITION BY "date", current_status ORDER BY start_check_time) AS rn
            FROM (
                SELECT DISTINCT c.id, c.date,  
                        MIN(p2p.Time) OVER(PARTITION BY c.id) AS start_check_time, 
                        COALESCE(FIRST_VALUE(v.State) OVER(PARTITION BY c.id ORDER BY v.Time DESC),
                                FIRST_VALUE(p2p.State) OVER(PARTITION BY c.id ORDER BY p2p.Time DESC)) AS current_status
                FROM Checks AS c
                LEFT JOIN p2p ON c.id = p2p."Check"
                LEFT JOIN verter AS v ON c.id = v."Check"
            ) AS A
            WHERE current_status <> 'Start'
        )

        SELECT
            "date"
        FROM days_x_count
        WHERE current_status = 'Success'
        GROUP BY "date"
        HAVING MAX(rn) >= N;
END $$ LANGUAGE plpgsql;

BEGIN;
CALL prc_lucky_day(1);
FETCH ALL FROM "cursor";
END;

-- 14

DROP PROCEDURE IF EXISTS get_peer_max_xp CASCADE;
CREATE OR REPLACE PROCEDURE get_peer_max_xp(cursor refcursor default 'cursor') AS
$$
BEGIN
    OPEN cursor FOR
        SELECT c.peer,
            SUM(xpamount) AS XP
        FROM xp
        JOIN checks c ON xp."Check" = c.id
        GROUP BY peer
        ORDER BY XP DESC, c.peer
        LIMIT 1;
END $$ LANGUAGE plpgsql;

BEGIN;
CALL get_peer_max_xp();
FETCH ALL FROM "cursor";
END;


-- 15

DROP PROCEDURE IF EXISTS get_peers_came_early CASCADE;
CREATE OR REPLACE PROCEDURE get_peers_came_early(preset_time TIME, N INT, cursor refcursor default 'cursor') AS
$$
BEGIN
    OPEN cursor FOR
        SELECT peer
        FROM TimeTracking
        WHERE state = 1 AND 
            time < preset_time
        GROUP BY peer
        HAVING COUNT(state) >= N;
END $$ LANGUAGE plpgsql;

BEGIN;
CALL get_peers_came_early('23:00:00', 2);
FETCH ALL FROM "cursor";
END;

-- 16

DROP PROCEDURE IF EXISTS get_count_out_of_campus CASCADE;
CREATE OR REPLACE PROCEDURE get_count_out_of_campus(N int, M int, cursor refcursor default 'cursor') AS
$$
BEGIN
    OPEN cursor FOR
        SELECT peer
        FROM TimeTracking
        WHERE state = 2 AND 
            "date" >= current_date - CONCAT(N - 1, ' days')::INTERVAL
        GROUP BY peer
        HAVING COUNT(state) >= M;
END $$ LANGUAGE plpgsql;

BEGIN;
CALL get_count_out_of_campus(350, 1);
FETCH ALL FROM "cursor";
END;


-- 17

DROP PROCEDURE IF EXISTS get_perc_early_entry_in_birthday CASCADE;
CREATE OR REPLACE PROCEDURE get_perc_early_entry_in_birthday(cursor refcursor default 'cursor') AS
$$
BEGIN
    OPEN cursor FOR
        SELECT TO_CHAR(TO_DATE(month_number::text, 'MM'), 'Month') AS Month, EarlyEntries
        FROM (
            SELECT DISTINCT month_number,
                COALESCE(ROUND(COUNT(CASE WHEN to_char(p.birthday, 'dd-mm') = to_char(tt.date, 'dd-mm') AND tt.time < '12:00:00' THEN tt.id ELSE NULL END) OVER(PARTITION BY month_number)::NUMERIC /
                NULLIF(COUNT(CASE WHEN to_char(p.birthday, 'dd-mm') = to_char(tt.date, 'dd-mm') THEN tt.id ELSE NULL END) OVER(PARTITION BY month_number), 0)::NUMERIC * 100), 0) AS EarlyEntries        
            FROM TimeTracking AS tt
            LEFT JOIN Peers AS p ON tt.peer = p.nickname
            RIGHT JOIN generate_series(1,12,1) AS month_number ON month_number = extract(month from tt.date) AND tt.state = 1
        ) AS A
        ORDER BY month_number;
END $$ LANGUAGE plpgsql;

BEGIN;
CALL get_perc_early_entry_in_birthday();
FETCH ALL FROM "cursor";
END;
