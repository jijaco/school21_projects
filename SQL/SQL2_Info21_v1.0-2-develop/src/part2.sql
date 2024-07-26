DROP PROCEDURE IF EXISTS add_p2p_review;
CREATE PROCEDURE add_p2p_review (IN peer_nickname VARCHAR,
                              IN checking_peer VARCHAR,
                              IN task_name VARCHAR,
                              IN check_status STATUS,
                              IN check_time TIME) AS $$
DECLARE check_id INTEGER DEFAULT 0;
BEGIN
    IF (check_status = 'Start') THEN 
        IF ((SELECT COUNT(*) FROM p2p AS p
            JOIN Checks AS c ON p."Check" = c.id
            WHERE p.CheckingPeer = checking_peer AND
                c.Peer = peer_nickname AND
                c.Task = task_name) = 0) THEN
                            check_id:=(SELECT MAX(id) FROM checks) + 1;
                            INSERT INTO Checks VALUES (check_id,
                                                        peer_nickname,
                                                        task_name,
                                                        current_date);
                            INSERT INTO p2p VALUES ((SELECT MAX(id) FROM p2p) + 1,
                                                        check_id,
                                                        checking_peer,
                                                        check_status,
                                                        check_time);
        ELSE
            RAISE EXCEPTION 'Error. Review already in progress or review completed';
        END IF;
    ELSE
        check_id:=(SELECT c.id FROM p2p AS p
                    JOIN Checks AS c ON p."Check" = c.id
                    WHERE p.CheckingPeer = checking_peer AND
                          c.Peer = peer_nickname AND
                          c.Task = task_name
                    LIMIT 1);
        IF (check_id != 0) THEN
            IF ((SELECT COUNT(*) FROM p2p
                WHERE "Check" = check_id AND 
                      State IN ('Success', 'Failure')) = 0) THEN
                            INSERT INTO p2p VALUES ((SELECT MAX(id) FROM p2p) + 1,
                                                        check_id,
                                                        checking_peer,
                                                        check_status,
                                                        check_time);
                ELSE
                    RAISE EXCEPTION 'Error. Review completed';
            END IF;
        ELSE 
            RAISE EXCEPTION 'Error. Review has not begun';
        END IF;
        
    END IF;
END $$ LANGUAGE plpgsql;

CALL add_p2p_review('peer2', 'peer1', 'C2_SimpleBashUtils', 'Start', '12:00:00');
CALL add_p2p_review('peer2', 'peer1', 'C2_SimpleBashUtils', 'Failure', '13:00:00');
-- CALL add_p2p_review('peer2', 'peer1', 'C2_SimpleBashUtils', 'Success', '13:00:00'); Error
CALL add_p2p_review('peer5', 'peer10', 'C2_SimpleBashUtils', 'Start', '14:00:00');
CALL add_p2p_review('peer5', 'peer10', 'C2_SimpleBashUtils', 'Success', '15:00:00');


DROP PROCEDURE IF EXISTS add_verter_review;
CREATE PROCEDURE add_verter_review (IN checked_peer VARCHAR,
                              IN task_name VARCHAR,
                              IN check_status STATUS,
                              IN check_time TIME) AS $$
DECLARE check_id INTEGER DEFAULT 0;
DECLARE last_check_status VARCHAR;
BEGIN
    SELECT A.State, A."Check" FROM (
        SELECT p2p.State, p2p."Check", c.id, MAX(c.id) OVER() AS last_check_id, p2p.Time FROM p2p
                JOIN Checks c ON p2p."Check" = c.id
                WHERE c.Peer = checked_peer AND
                        c.Task = task_name
    ) AS A
    INTO last_check_status, check_id
    WHERE last_check_id = id
    ORDER BY A.Time DESC
    LIMIT 1;
    IF (check_status = 'Start') THEN
        IF (last_check_status = 'Success') AND ((SELECT COUNT(*) FROM verter WHERE "Check" = check_id) = 0) THEN
            INSERT INTO verter
            VALUES ((SELECT MAX(id) FROM verter) + 1,
                    check_id,
                    check_status,
                    check_time);
        ELSE
            RAISE EXCEPTION 'Error. Peer Review has not been successful or Verter Review has already been initiated';
        END IF;
    ELSE
        IF ((SELECT State FROM verter WHERE "Check" = check_id ORDER BY Time DESC LIMIT 1) = 'Start') THEN
                INSERT INTO verter VALUES ((SELECT max(id) FROM verter) + 1,
                                        check_id, 
                                        check_status,
                                        check_time);
        ELSE 
            RAISE EXCEPTION 'Error. Verter review has not started or has already been completed';
        END IF;
    END IF;
END $$ LANGUAGE plpgsql;

CALL add_verter_review('peer10', 'C2_SimpleBashUtils', 'Start', '15:20:00');
CALL add_verter_review('peer10', 'C2_SimpleBashUtils', 'Failure', '15:30:00');
-- CALL add_verter_review('peer3', 'C2_SimpleBashUtils', 'Success', '15:30:00'); Error

DROP FUNCTION IF EXISTS update_transferredpoints() CASCADE;
CREATE FUNCTION update_transferredpoints() RETURNS TRIGGER AS $$
BEGIN 
    IF (NEW.State = 'Start') THEN
        UPDATE TransferredPoints
        SET PointsAmount = PointsAmount + 1
        WHERE CheckingPeer = NEW.CheckingPeer AND
              CheckedPeer = (SELECT peer FROM Checks WHERE id = NEW."Check");
    END IF;
    RETURN NULL;
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_transferredpoints ON p2p;
CREATE TRIGGER trg_transferredpoints
AFTER INSERT ON p2p
    FOR EACH ROW
    EXECUTE FUNCTION update_transferredpoints();


DROP FUNCTION IF EXISTS check_insert_xp() CASCADE;
CREATE FUNCTION check_insert_xp() RETURNS TRIGGER AS $$
DECLARE max_task_xp INTEGER;
BEGIN 
    max_task_xp:=(SELECT t.MaxXP FROM Tasks as t
                  JOIN Checks as c ON c.Task = t.Title
                  WHERE c.id = NEW."Check");
    IF (NEW.XpAmount > max_task_xp) OR 
       ((SELECT COUNT(*) FROM p2p
            WHERE NEW."Check" = p2p."Check" AND p2p.state = 'Success') != 1) OR
       ((SELECT COUNT(*) FROM verter 
            WHERE NEW."Check" = verter."Check" AND verter.state = 'Failure') > 0) THEN
        RAISE EXCEPTION 'Error. Review not in Success status or incorrect number of XP exceeds maximum';
    END IF;
    RETURN (NEW.id, NEW."Check", NEW.XpAmount);
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_insert_xp ON xp;
CREATE TRIGGER trg_insert_xp
BEFORE INSERT ON xp
    FOR EACH ROW
    EXECUTE FUNCTION check_insert_xp();


INSERT INTO XP VALUES (1, 9, 500);
