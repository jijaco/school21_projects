Create table Peers(
Nickname varchar not NULL primary key,
Birthday date not null
);

INSERT INTO Peers(Nickname, Birthday)
Values ('peer1', '1996-01-01'),
       ('peer2', '1996-01-02'),
       ('peer3', '1996-01-03'),
       ('peer4', '1996-01-04'),
       ('peer5', '1996-01-05'),
       ('peer6', '1996-01-06'),
       ('peer7', '1996-01-07'),
       ('peer8', '1996-01-08'),
       ('peer9', '1996-01-09'),
       ('peer10', '1996-01-10');
	   
Create table Tasks(
title varchar primary key,
parentTask varchar,
MaxXP INTEGER not null,
FOREIGN KEY (ParentTask) REFERENCES Tasks (Title)
);

INSERT INTO Tasks
VALUES
       ('C2_SimpleBashUtils', NULL, 250),
       ('C3_s21_string+', 'C2_SimpleBashUtils', 500),
       ('C4_s21_math', 'C2_SimpleBashUtils', 300),
       ('C5_s21_decimal', 'C4_s21_math', 350),
       ('C6_s21_matrix', 'C5_s21_decimal', 200),
       ('C7_SmartCalc_v1.0', 'C6_s21_matrix', 500),
       ('C8_3DViewer_v1.0', 'C7_SmartCalc_v1.0', 750),
       ('DO1_Linux', 'C3_s21_string+', 300),
       ('DO2_Linux Network', 'DO1_Linux', 250),
       ('DO3_LinuxMonitoring v1.0', 'DO2_Linux Network', 350),
       ('DO4_LinuxMonitoring v2.0', 'DO3_LinuxMonitoring v1.0', 350),
       ('DO5_SimpleDocker', 'DO3_LinuxMonitoring v1.0', 300),
       ('DO6_CICD', 'DO5_SimpleDocker', 300),
       ('CPP1_s21_matrix+', 'C8_3DViewer_v1.0', 300),
       ('CPP2_s21_containers', 'CPP1_s21_matrix+', 350),
       ('CPP3_SmartCalc_v2.0', 'CPP2_s21_containers', 600),
       ('CPP4_3DViewer_v2.0', 'CPP3_SmartCalc_v2.0', 750),
       ('CPP5_3DViewer_v2.1', 'CPP4_3DViewer_v2.0', 600),
       ('CPP6_3DViewer_v2.2', 'CPP4_3DViewer_v2.0', 800),
       ('CPP7_MLP', 'CPP4_3DViewer_v2.0', 700),
       ('CPP8_PhotoLab_v1.0', 'CPP4_3DViewer_v2.0', 450),
       ('CPP9_MonitoringSystem', 'CPP4_3DViewer_v2.0', 1000),
       ('A1_Maze', 'CPP4_3DViewer_v2.0', 300),
       ('A2_SimpleNavigator v1.0', 'A1_Maze', 400),
       ('A3_Parallels', 'A2_SimpleNavigator v1.0', 300),
       ('A4_Crypto', 'A2_SimpleNavigator v1.0', 350),
       ('A5_s21_memory', 'A2_SimpleNavigator v1.0', 400),
       ('A6_Transactions', 'A2_SimpleNavigator v1.0', 700),
       ('A7_DNA Analyzer', 'A2_SimpleNavigator v1.0', 800),
       ('A8_Algorithmic trading', 'A2_SimpleNavigator v1.0', 800),
       ('SQL1_Bootcamp', 'C8_3DViewer_v1.0', 1500),
       ('SQL2_Info21 v1.0', 'SQL1_Bootcamp', 500),
       ('SQL3_RetailAnalitycs v1.0', 'SQL2_Info21 v1.0', 600);
	   
CREATE TYPE status as ENUM('Start', 'Success', 'Failure');

CREATE table Checks(
id BIGINT not null primary key,
Peer varchar not null,
Task varchar not null,
Date date not null,
FOREIGN KEY (Peer) REFERENCES Peers (Nickname),
FOREIGN KEY (Task) REFERENCES Tasks (Title)
);

INSERT INTO Checks (id, peer, task, date)
VALUES (1, 'peer1', 'C2_SimpleBashUtils', '2023-03-01'),
       (2, 'peer1', 'C2_SimpleBashUtils', '2023-03-02'),
       (3, 'peer2', 'C4_s21_math', '2023-03-02'),
       (4, 'peer3', 'C2_SimpleBashUtils', '2023-03-03'),
       (5, 'peer3', 'C3_s21_string+', '2023-03-04'),
       (6, 'peer4', 'DO1_Linux', '2023-03-05'),
       (7, 'peer5', 'DO2_Linux Network', '2023-03-05'),
       (8, 'peer6', 'DO2_Linux Network', '2023-03-05'),
       (9, 'peer7', 'DO3_LinuxMonitoring v1.0', '2023-03-07'),
       (10, 'peer8', 'C5_s21_decimal', '2023-03-08'),
       (11, 'peer9', 'C3_s21_string+', '2023-03-08'),
       (12, 'peer10', 'C4_s21_math', '2023-03-08'),
       (13, 'peer2', 'C3_s21_string+', '2023-03-08'),
       (14, 'peer3', 'DO1_Linux', '2023-03-09'),
       (15, 'peer1', 'C6_s21_matrix', '2023-03-10'),
       (16, 'peer8', 'DO1_Linux', '2023-03-10'),
       (17, 'peer5', 'C2_SimpleBashUtils', '2023-03-12'),
       (18, 'peer4', 'C6_s21_matrix', '2023-04-01'),
       (19, 'peer7', 'DO1_Linux', '2023-04-05'),
       (20, 'peer10', 'C3_s21_string+', '2023-04-06'),
       (21, 'peer7', 'DO2_Linux Network', '2023-04-06'),
       (22, 'peer7', 'DO3_LinuxMonitoring v1.0', '2023-04-07'),
       (23, 'peer7', 'DO4_LinuxMonitoring v2.0', '2023-04-08'),
       (24, 'peer7', 'DO5_SimpleDocker', '2023-04-09'),
       (25, 'peer7', 'DO6_CICD', '2023-04-10'),
       (26, 'peer3', 'C4_s21_math', '2023-04-06'),
       (27, 'peer3', 'C5_s21_decimal', '2023-03-07'),
       (28, 'peer3', 'C6_s21_matrix', '2023-03-08'),
       (29, 'peer3', 'C7_SmartCalc_v1.0', '2023-03-09'),
       (30, 'peer3', 'C8_3DViewer_v1.0', '2023-03-10');

CREATE TABLE P2P(
id BIGINT not NULL primary key,
"Check" BIGINT NOT NULL,
checkingPeer varchar not null,
State status not null,
Time time NOT NULL,
constraint fk_check FOREIGN KEY("Check") references Checks(ID),
constraint fk_check_peer FOREIGN KEY(checkingPeer) references Peers(Nickname)
);

INSERT INTO P2P (id, "Check", CheckingPeer, State, Time)
VALUES (1, 1, 'peer2', 'Start', '09:00:00'),
       (2, 1, 'peer2', 'Failure', '10:00:00'),
       (3, 2, 'peer3', 'Start', '13:00:00'),
       (4, 2, 'peer3', 'Success', '14:00:00'),
       (5, 3, 'peer1', 'Start', '22:00:00'),
       (6, 3, 'peer1', 'Success', '23:00:00'),
       (7, 4, 'peer4', 'Start', '15:00:00'),
       (8, 4, 'peer4', 'Success', '16:00:00'),
       (9, 5, 'peer5', 'Start', '14:00:00'),
       (10, 5, 'peer5', 'Success', '15:00:00'),
       (11, 6, 'peer6', 'Start', '01:00:00'),
       (12, 6, 'peer6', 'Success', '02:00:00'),
       (13, 7, 'peer7', 'Start', '10:00:00'),
       (14, 7, 'peer7', 'Success', '12:00:00'),
       (15, 8, 'peer8', 'Start', '12:00:00'),
       (16, 8, 'peer8', 'Success', '13:00:00'),
       (17, 9, 'peer9', 'Start', '12:00:00'),
       (18, 9, 'peer9', 'Success', '13:00:00'),
       (19, 10, 'peer10', 'Start', '19:00:00'),
       (20, 11, 'peer5', 'Start', '15:00:00'),
       (21, 11, 'peer5', 'Success', '15:01:00'),
       (22, 12, 'peer7', 'Start', '22:00:00'),
       (23, 12, 'peer7', 'Failure', '23:00:00'),
       (24, 13, 'peer4', 'Start', '22:00:00'),
       (25, 13, 'peer4', 'Success', '23:00:00'),
       (26, 14, 'peer1', 'Start', '22:00:00'),
       (27, 14, 'peer1', 'Success', '23:00:00'),
       (28, 15, 'peer9', 'Start', '04:00:00'),
       (29, 15, 'peer9', 'Success', '05:00:00'),
       (30, 16, 'peer1', 'Start', '05:00:00'),
       (31, 16, 'peer1', 'Failure', '06:00:00'),
       (32, 17, 'peer7', 'Start', '07:00:00'),
       (33, 17, 'peer7', 'Success', '08:00:00'),
       (34, 18, 'peer10', 'Start', '08:00:00'),
       (35, 18, 'peer10', 'Success', '09:00:00'),
       (36, 19, 'peer2', 'Start', '09:00:00'),
       (37, 19, 'peer2', 'Success', '10:00:00'),
       (38, 20, 'peer6', 'Start', '11:00:00'),
       (39, 21, 'peer1', 'Start', '11:00:00'),
       (40, 21, 'peer1', 'Success', '12:00:00'),
       (41, 22, 'peer2', 'Start', '05:00:00'),
       (42, 22, 'peer2', 'Success', '06:00:00'),
       (43, 23, 'peer3', 'Start', '10:00:00'),
       (44, 23, 'peer3', 'Success', '11:00:00'),
       (45, 24, 'peer4', 'Start', '11:00:00'),
       (46, 24, 'peer4', 'Success', '12:00:00'),
       (47, 25, 'peer5', 'Start', '18:00:00'),
       (48, 25, 'peer5', 'Success', '19:00:00'),
       (49, 26, 'peer6', 'Start', '15:00:00'),
       (50, 26, 'peer6', 'Success', '16:00:00');
      
CREATE TABLE Verter(
id BIGINT not null primary key,
"Check" bigint not null,
State status not null,
Time time not null,
constraint fk_check_verter FOREIGN KEY("Check") references Checks(ID)
);

INSERT INTO Verter (id, "Check", State, Time)
values
       (1, 2, 'Start', '13:01:00'),
       (2, 2, 'Success', '13:02:00'),
       (3, 3, 'Start', '23:01:00'),
       (4, 3, 'Success', '23:02:00'),
       (5, 4, 'Start', '16:01:00'),
       (6, 4, 'Failure', '16:02:00'),
       (7, 5, 'Start', '15:01:00'),
       (8, 5, 'Success', '15:02:00'),
       (9, 13, 'Start', '23:01:00'),
       (10, 13, 'Success', '23:02:00'),
       (11, 15, 'Start', '05:01:00'),
       (12, 15, 'Failure', '05:02:00'),
       (13, 17, 'Start', '06:01:00'),
       (14, 17, 'Success', '06:02:00'),
       (15, 18, 'Start', '06:01:00'),
       (16, 18, 'Success', '06:02:00'),
       (17, 19, 'Start', '06:01:00'),
       (18, 19, 'Failure', '06:02:00'),
       (19, 21, 'Start', '12:01:00'),
       (20, 21, 'Success', '12:02:00'),
       (21, 22, 'Start', '06:01:00'),
       (22, 22, 'Success', '06:02:00'),
       (23, 23, 'Start', '11:01:00'),
       (24, 23, 'Success', '11:02:00'),
       (25, 24, 'Start', '12:01:00'),
       (26, 24, 'Success', '12:02:00'),
       (27, 25, 'Start', '19:01:00'),
       (28, 25, 'Success', '19:02:00'),
       (29, 26, 'Start', '16:01:00'),
       (30, 26, 'Success', '16:02:00');


	   
Create table TransferredPoints(
id bigint generated always as identity 
(increment 1 start 1) primary key,
CheckingPeer varchar NOT NULL,
CheckedPeer  varchar NOT NULL,
PointsAmount integer NOT NULL,
FOREIGN KEY (CheckingPeer) REFERENCES Peers (Nickname),
FOREIGN KEY (CheckedPeer) REFERENCES Peers (Nickname)
);
INSERT INTO TransferredPoints (CheckingPeer, CheckedPeer, PointsAmount)
select checkingpeer, Peer, count(*) from P2P
join Checks C on C.ID = P2P."Check"
where State != 'Start'
group by 1,2;


CREATE TABLE Friends
( ID bigint  NOT NULL GENERATED ALWAYS AS IDENTITY
 (INCREMENT 1 START 1) PRIMARY KEY,
  Peer1 varchar NOT NULL,
  Peer2 varchar NOT NULL,
  FOREIGN KEY (Peer1) REFERENCES Peers (Nickname),
  FOREIGN KEY (Peer2) REFERENCES Peers (Nickname)
);
INSERT INTO Friends (Peer1, Peer2)
select p1.Nickname a, p2.Nickname b
from Peers p1, Peers p2
where p1.Nickname < p2.Nickname;

CREATE TABLE Recommendations
(ID bigint PRIMARY KEY NOT NULL,
 Peer varchar NOT NULL,
 RecommendedPeer varchar NOT NULL,
 FOREIGN KEY (Peer) REFERENCES Peers (Nickname),
 FOREIGN KEY (RecommendedPeer) REFERENCES Peers (Nickname)
);

INSERT INTO Recommendations (id, Peer, RecommendedPeer)
VALUES (1, 'peer1', 'peer2'),
       (2, 'peer1', 'peer3'),
       (3, 'peer2', 'peer5'),
       (4, 'peer3', 'peer5'),
       (5, 'peer4', 'peer1'),
       (6, 'peer5', 'peer10'),
       (7, 'peer6', 'peer4'),
       (8, 'peer7', 'peer5'),
       (9, 'peer8', 'peer1'),
       (10, 'peer9', 'peer6');
	   
	   
CREATE TABLE XP
(
    ID       bigint PRIMARY KEY ,
    "Check"  bigint  NOT NULL ,
    XPAmount integer NOT NULL ,
    foreign key ("Check") references Checks (ID)
);

INSERT INTO XP (id, "Check", XPAmount)
VALUES (1, 2, 240),
       (2, 3, 300),
       (3, 5, 200),
       (4, 6, 250),
       (5, 7, 250),
       (6, 8, 250),
       (7, 9, 350),
       (8, 11, 450),
       (9, 13, 500),
       (10, 14, 300),
       (11, 17, 250),
       (12, 18, 150),
       (13, 21, 250),
       (14, 22, 350),
       (15, 23, 350),
       (16, 24, 300),
       (17, 25, 300),
       (18, 26, 300),
       (19, 27, 350),
       (20, 28, 200),
       (21, 29, 500),
       (22, 30, 750);

CREATE TABLE TimeTracking
( ID bigint PRIMARY KEY NOT NULL,
  Peer   varchar NOT NULL,
  "Date"   date NOT NULL,
  Time   time NOT NULL,
  State int NOT NULL CHECK ( State IN (1, 2)),
  FOREIGN KEY (Peer) REFERENCES Peers (Nickname)
);

INSERT INTO TimeTracking (id, Peer, Date, Time, State)
VALUES (1, 'peer1', '2023-03-02', '08:00:00', 1),
       (2, 'peer1', '2023-03-02', '18:00:00', 2),
       (3, 'peer2', '2023-03-02', '18:30:00', 1),
       (4, 'peer2', '2023-03-02', '23:30:00', 2),
       (5, 'peer4', '2023-04-02', '18:10:00', 1),
       (6, 'peer4', '2023-04-02', '21:00:00', 2),
       (7, 'peer3', '2023-04-22', '10:00:00', 1),
       (8, 'peer5', '2023-04-22', '11:00:00', 1),
       (9, 'peer5', '2023-04-22', '21:00:00', 2),
       (10, 'peer3', '2023-04-22', '23:00:00', 2),
       (11, 'peer7', '2023-05-02', '18:10:00', 1),
       (12, 'peer7', '2023-05-02', '21:00:00', 2),
       (13, 'peer7', '2023-05-02', '22:10:00', 1),
       (14, 'peer7', '2023-05-02', '23:50:00', 2);

Create or replace procedure export(
In tableName varchar, In path text, In separator char) as $$
BEGIN
EXECUTE format('COPY %s TO ' '%s' ' DELIMITER ''%s'' CSV HEADER;',
			  tablename, path, separator);
			  
END;
$$ LANGUAGE plpgsql;


Create or replace procedure import(IN tablename varchar, IN path text, IN separator char) AS $$
    BEGIN
        EXECUTE format('COPY %s FROM ''%s'' DELIMITER ''%s'' CSV HEADER;',
            tablename, path, separator);
    END;
$$ LANGUAGE plpgsql;
