update games set awayteam_id = 50 where awayteam_id = 1;
update games set awayteam_id = 40 where awayteam_id = 2;
update games set awayteam_id = 49 where awayteam_id = 3;
update games set awayteam_id = 48 where awayteam_id = 4;
update games set awayteam_id = 33 where awayteam_id = 5;
update games set awayteam_id = 42 where awayteam_id = 6;
update games set awayteam_id = 39 where awayteam_id = 7;
update games set awayteam_id = 47 where awayteam_id = 8;
update games set awayteam_id = 51 where awayteam_id = 9;
update games set awayteam_id = 41 where awayteam_id = 10;
update games set awayteam_id = 46 where awayteam_id = 11;
update games set awayteam_id = 66 where awayteam_id = 12;
update games set awayteam_id = 52 where awayteam_id = 13;
update games set awayteam_id = 55 where awayteam_id = 14;
update games set awayteam_id = 63 where awayteam_id = 15;
update games set awayteam_id = 45 where awayteam_id = 16;
update games set awayteam_id = 34 where awayteam_id = 17;
update games set awayteam_id = 71 where awayteam_id = 18;
update games set awayteam_id = 38 where awayteam_id = 19;
update games set awayteam_id = 44 where awayteam_id = 20;

| lineup_id        | int(11)       | YES  |     | NULL    |       |
| game_id          | int(11)       | YES  |     | NULL    |       |
| home_team_id     | int(11)       | YES  |     | NULL    |       |
| away_team_id     | int(11)       | YES  |     | NULL    |       |
| home_defenders   | varchar(1000) | YES  |     | NULL    |       |
| home_midfielders | varchar(1000) | YES  |     | NULL    |       |
| home_attackers   | varchar(1000) | YES  |     | NULL    |       |
| home_subs        | varchar(1000) | YES  |     | NULL    |       |
| away_defenders   | varchar(1000) | YES  |     | NULL    |       |
| away_midfielders | varchar(1000) | YES  |     | NULL    |       |
| away_attackers   | varchar(1000) | YES  |     | NULL    |       |
| away_subs        | varchar(1000) | YES  |     | NULL    |       |
| userid 



insert into lineups(lineup_id, game_id, home_team_id, away_team_id, home_keeper, away_keeper, home_defenders, away_defenders, home_midfielders, away_midfielders, home_attackers, away_attackers, home_subs, away_subs,userid) values('1', '307', '33','46','882','2728','378,742,885,886', '2920,3421,18771,18772','902,903,901,904','2926,18778,18779,18784','18,274','18788,18906','2931,18846,2935,153434,153430', '18776,18772,18770,1098,2778', '3'); 
insert into lineups(lineup_id, game_id, home_team_id, away_team_id, home_keeper, away_keeper, home_defenders, away_defenders, home_midfielders, away_midfielders, home_attackers, away_attackers, home_subs, away_subs,userid) values('1', '307', '33','46','882','18146','378,742,885,886', '2920,3421,18771,18776','902,903,901,904','2926,18785,18779,18784','18,274','18788,18906','2931,18846,2935,153434,153430', '18778,18772,18770,1098,2778', '6'); 

insert into lineups(lineup_id, game_id, home_team_id, away_team_id, home_keeper, away_keeper, home_defenders, away_defenders, home_midfielders, away_midfielders, home_attackers, away_attackers, home_subs, away_subs,userid) values('2', '364', '33','49','882','2986','378,742,885,886', '2280,2278,2282,2285','902,903,901,904','2289,2290,2291,2292','18,274','907,1166','2931,18846,2935,153434,153430', '48,17,548,2273,19220', '3');
insert into lineups(lineup_id, game_id, home_team_id, away_team_id, home_keeper, away_keeper, home_defenders, away_defenders, home_midfielders, away_midfielders, home_attackers, away_attackers, home_subs, away_subs,userid) values('2', '364', '33','49','882','2273','378,742,885,886', '2280,2278,2282,2285','902,903,901,904','2289,2290,2291,2292','18,274','907,1166','2931,18846,2935,153434,153430', '48,17,548,2986,19220', '7');

insert into lineups(lineup_id, game_id, home_team_id, away_team_id, home_keeper, away_keeper, home_defenders, away_defenders, home_midfielders, away_midfielders, home_attackers, away_attackers, home_subs, away_subs,userid) values('3', '344', '33','49','882','2727','378,742,885,886','2731,15745,1119,19124','902,903,901,904','174,15799,19831,20110,25089','18,274','19974','2931,18846,2935,153434,153430', '19465,276263,215873,278083,197811', '3'); 
insert into lineups(lineup_id, game_id, home_team_id, away_team_id, home_keeper, away_keeper, home_defenders, away_defenders, home_midfielders, away_midfielders, home_attackers, away_attackers, home_subs, away_subs,userid) values('3', '344', '33','49','882','2727','378,742,885,886','2731,15745,1119,19124','902,903,901,904','174,15799,19831,20110,25089','18,274','19974','2931,18846,2935,153434,153430', '19465,276263,215873,278083,197811', '7'); 


