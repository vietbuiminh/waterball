--
-- Table structure for table admin
--

DROP TABLE IF EXISTS admin;
CREATE TABLE admin (
  league_name varchar(150) NOT NULL,
  league_abb varchar(10) NOT NULL,
  commissioner_name varchar(50) NOT NULL,
  commissioner_email varchar(50) NOT NULL,
  season INTEGER NOT NULL DEFAULT '1',
  about tinytext NOT NULL ,
  js1 text,
  js2 text,
  site_available char(1) NOT NULL DEFAULT 'Y',
  league_scheduled char(1) NOT NULL DEFAULT 'N',
  session_1_deadline datetime DEFAULT NULL
);

--
-- Dumping data for table admin
--


/*!40000 ALTER TABLE admin DISABLE KEYS */;
INSERT INTO admin VALUES ('TMVL United 1','TMVL','Allan and Max Sellers','allan.sellers@gmail.com',8,'','','','Y','Y','2023-02-18 21:00:00');
/*!40000 ALTER TABLE admin ENABLE KEYS */;


--
-- Table structure for table coaches
--

DROP TABLE IF EXISTS coaches;
CREATE TABLE coaches (
  coach_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  first_name varchar(20) NOT NULL,
  last_name varchar(20) NOT NULL,
  email varchar(40) NOT NULL,
  status varchar(1) NOT NULL DEFAULT 'Y',
  password varchar(20) NOT NULL,
  last_accessed datetime NOT NULL DEFAULT '2020-01-01 00:00:00',
  access_level varchar(10) NOT NULL DEFAULT '0000000000',
  offset INTEGER NOT NULL DEFAULT '-6'
) ;

--
-- Dumping data for table coaches
--


/*!40000 ALTER TABLE coaches DISABLE KEYS */;
INSERT INTO coaches VALUES (1, 'Max','Sellers','maxesellers@gmail.com','Y','12MadMax','2023-02-11 04:19:11','0000000000',-5),
(2, 'Viet','Bui','vietbui20@augustana.edu','Y','7Wonders','2023-02-11 04:19:11','0000000000',-5);
/*!40000 ALTER TABLE coaches ENABLE KEYS */;


--
-- Table structure for table lineups
--

DROP TABLE IF EXISTS lineups;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE lineups (
  lineup_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  team_id INTEGER NOT NULL,
  match_number INTEGER NOT NULL,
  cf_player INTEGER NOT NULL,
  cd_player INTEGER NOT NULL,
  lw_player INTEGER NOT NULL,
  rw_player INTEGER NOT NULL,
  ld_player INTEGER NOT NULL,
  rd_player INTEGER NOT NULL,
  gk_player INTEGER NOT NULL
) ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table lineups
--


/*!40000 ALTER TABLE lineups DISABLE KEYS */;
INSERT INTO lineups VALUES (1,1,1,81,65,1,9,17,25,97),(2,2,1,82,66,2,10,18,26,98),(3,3,1,83,67,3,11,19,27,99),(4,4,1,84,68,4,12,20,28,100),(5,5,1,85,69,5,13,21,29,101),(6,6,1,86,70,6,14,22,30,102),(7,7,1,87,71,7,15,23,31,103),(8,8,1,88,72,8,16,24,32,104),(9,1,2,89,73,33,41,49,57,105),(10,2,2,90,74,34,42,50,58,106),(11,3,2,91,75,35,43,51,59,107),(12,4,2,92,76,36,44,52,60,108),(13,5,2,93,77,37,45,53,61,109),(14,6,2,94,78,38,46,54,62,110),(15,7,2,95,79,39,47,55,63,111),(16,8,2,96,80,40,48,56,64,112),(17,1,3,81,65,1,9,17,25,97),(18,2,3,82,66,2,10,18,26,98),(19,3,3,83,67,3,11,19,27,99),(20,4,3,84,68,4,12,20,28,100),(21,5,3,85,69,5,13,21,29,101),(22,6,3,86,70,6,14,22,30,102),(23,7,3,87,71,7,15,23,31,103),(24,8,3,88,72,8,16,24,32,104),(25,1,4,89,73,33,41,49,57,105),(26,2,4,90,74,34,42,50,58,106),(27,3,4,91,75,35,43,51,59,107),(28,4,4,92,76,36,44,52,60,108),(29,5,4,93,77,37,45,53,61,109),(30,6,4,94,78,38,46,54,62,110),(31,7,4,95,79,39,47,55,63,111),(32,8,4,96,80,40,48,56,64,112),(33,1,5,81,65,1,9,17,25,97),(34,2,5,82,66,2,10,18,26,98),(35,3,5,83,67,3,11,19,27,99),(36,4,5,84,68,4,12,20,28,100),(37,5,5,85,69,5,13,21,29,101),(38,6,5,86,70,6,14,22,30,102),(39,7,5,87,71,7,15,23,31,103),(40,8,5,88,72,8,16,24,32,104),(41,1,6,89,73,33,41,49,57,105),(42,2,6,90,74,34,42,50,58,106),(43,3,6,91,75,35,43,51,59,107),(44,4,6,92,76,36,44,52,60,108),(45,5,6,93,77,37,45,53,61,109),(46,6,6,94,78,38,46,54,62,110),(47,7,6,95,79,39,47,55,63,111),(48,8,6,96,80,40,48,56,64,112),(49,1,7,81,65,1,9,17,25,97),(50,2,7,82,66,2,10,18,26,98),(51,3,7,83,67,3,11,19,27,99),(52,4,7,84,68,4,12,20,28,100),(53,5,7,85,69,5,13,21,29,101),(54,6,7,86,70,6,14,22,30,102),(55,7,7,87,71,7,15,23,31,103),(56,8,7,88,72,8,16,24,32,104),(57,1,8,89,73,33,41,49,57,105),(58,2,8,90,74,34,42,50,58,106),(59,3,8,91,75,35,43,51,59,107),(60,4,8,92,76,36,44,52,60,108),(61,5,8,93,77,37,45,53,61,109),(62,6,8,94,78,38,46,54,62,110),(63,7,8,95,79,39,47,55,63,111),(64,8,8,96,80,40,48,56,64,112),(65,1,9,81,65,1,9,17,25,97),(66,2,9,82,66,2,10,18,26,98),(67,3,9,83,67,3,11,19,27,99),(68,4,9,84,68,4,12,20,28,100),(69,5,9,85,69,5,13,21,29,101),(70,6,9,86,70,6,14,22,30,102),(71,7,9,87,71,7,15,23,31,103),(72,8,9,88,72,8,16,24,32,104),(73,1,10,89,73,33,41,49,57,105),(74,2,10,90,74,34,42,50,58,106),(75,3,10,91,75,35,43,51,59,107),(76,4,10,92,76,36,44,52,60,108),(77,5,10,93,77,37,45,53,61,109),(78,6,10,94,78,38,46,54,62,110),(79,7,10,95,79,39,47,55,63,111),(80,8,10,96,80,40,48,56,64,112),(81,1,11,81,65,1,9,17,25,97),(82,2,11,82,66,2,10,18,26,98),(83,3,11,83,67,3,11,19,27,99),(84,4,11,84,68,4,12,20,28,100),(85,5,11,85,69,5,13,21,29,101),(86,6,11,86,70,6,14,22,30,102),(87,7,11,87,71,7,15,23,31,103),(88,8,11,88,72,8,16,24,32,104),(89,1,12,89,73,33,41,49,57,105),(90,2,12,90,74,34,42,50,58,106),(91,3,12,91,75,35,43,51,59,107),(92,4,12,92,76,36,44,52,60,108),(93,5,12,93,77,37,45,53,61,109),(94,6,12,94,78,38,46,54,62,110),(95,7,12,95,79,39,47,55,63,111),(96,8,12,96,80,40,48,56,64,112),(97,1,13,81,65,1,9,17,25,97),(98,2,13,82,66,2,10,18,26,98),(99,3,13,83,67,3,11,19,27,99),(100,4,13,84,68,4,12,20,28,100),(101,5,13,85,69,5,13,21,29,101),(102,6,13,86,70,6,14,22,30,102),(103,7,13,87,71,7,15,23,31,103),(104,8,13,88,72,8,16,24,32,104),(105,1,14,89,73,33,41,49,57,105),(106,2,14,90,74,34,42,50,58,106),(107,3,14,91,75,35,43,51,59,107),(108,4,14,92,76,36,44,52,60,108),(109,5,14,93,77,37,45,53,61,109),(110,6,14,94,78,38,46,54,62,110),(111,7,14,95,79,39,47,55,63,111),(112,8,14,96,80,40,48,56,64,112),(113,1,15,81,65,1,9,17,25,97),(114,2,15,82,66,2,10,18,26,98),(115,3,15,83,67,3,11,19,27,99),(116,4,15,84,68,4,12,20,28,100),(117,5,15,85,69,5,13,21,29,101),(118,6,15,86,70,6,14,22,30,102),(119,7,15,87,71,7,15,23,31,103),(120,8,15,88,72,8,16,24,32,104),(121,1,16,89,73,33,41,49,57,105),(122,2,16,90,74,34,42,50,58,106),(123,3,16,91,75,35,43,51,59,107),(124,4,16,92,76,36,44,52,60,108),(125,5,16,93,77,37,45,53,61,109),(126,6,16,94,78,38,46,54,62,110),(127,7,16,95,79,39,47,55,63,111),(128,8,16,96,80,40,48,56,64,112);
/*!40000 ALTER TABLE lineups ENABLE KEYS */;


--
-- Table structure for table player_stats
--

DROP TABLE IF EXISTS player_stats;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE player_stats (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  season INTEGER DEFAULT '1',
  player_id INTEGER DEFAULT NULL,
  age INTEGER DEFAULT NULL,
  team_id INTEGER DEFAULT NULL,
  opp_team_id INTEGER DEFAULT NULL,
  match_number INTEGER DEFAULT NULL,
  t_set varchar(6) DEFAULT NULL,
  position varchar(4) DEFAULT NULL,
  sets_played INTEGER DEFAULT NULL,
  attack_attempts INTEGER DEFAULT NULL,
  kills INTEGER DEFAULT NULL,
  attack_errors INTEGER DEFAULT NULL,
  attack_percentage double DEFAULT NULL,
  assists INTEGER DEFAULT NULL,
  serve_poINTEGERs INTEGER DEFAULT NULL,
  aces INTEGER DEFAULT NULL,
  serve_errors INTEGER DEFAULT NULL,
  serve_receptions INTEGER DEFAULT NULL,
  serve_reception_errors INTEGER DEFAULT NULL,
  digs INTEGER DEFAULT NULL,
  solo_blocks INTEGER DEFAULT NULL,
  assist_blocks INTEGER DEFAULT NULL,
  block_errors INTEGER DEFAULT NULL,
  total_poINTEGERs double DEFAULT NULL,
  passer_rating_total INTEGER DEFAULT '0',
  setting_attempts INTEGER DEFAULT '0',
  passer_rating_3_count INTEGER DEFAULT '0',
  serve_attempts INTEGER DEFAULT '0',
  match_rating double DEFAULT '0'
) ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table player_stats
--


/*!40000 ALTER TABLE player_stats DISABLE KEYS */;
/*!40000 ALTER TABLE player_stats ENABLE KEYS */;


--
-- Table structure for table players
--

DROP TABLE IF EXISTS players;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE players (
  player_id INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
  team_id INTEGER DEFAULT NULL,
  first_name text,
  last_name text,
  age text,
  position text,
  jersey INTEGER NOT NULL DEFAULT '0',
  swimming INTEGER NOT NULL DEFAULT '0',
  ballhandling INTEGER NOT NULL DEFAULT '0',
  passing INTEGER NOT NULL DEFAULT '0',
  shooting INTEGER NOT NULL DEFAULT '0',
  defense INTEGER NOT NULL DEFAULT '0',
  goalkeeping INTEGER NOT NULL DEFAULT '0',
  fit INTEGER NOT NULL DEFAULT '0',
  aggression INTEGER NOT NULL DEFAULT '0',
  overall INTEGER NOT NULL DEFAULT '0'
) ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table players
--


/*!40000 ALTER TABLE players DISABLE KEYS */;
INSERT INTO players VALUES (1,1,'Orville','Chan','Fr','Attacker',1,61,87,61,83,68,0,0,96,71),(2,2,'Morgan','Booth','So','Attacker',1,83,83,76,74,82,0,0,70,79),(3,3,'Aharon','Gamble','Fr','Attacker',1,87,99,89,67,64,0,0,77,81),(4,4,'Corrigan','Hampton','Sr','Attacker',1,64,62,77,95,61,0,0,69,71),(5,5,'Adrik','Moses','Sr','Attacker',1,96,81,74,82,65,0,0,84,79),(6,6,'Phillips','Leonard','Sr','Attacker',1,78,75,60,60,73,0,0,47,69),(7,7,'Boss','Fisher','Fr','Attacker',1,95,93,72,82,87,0,0,83,85),(8,8,'Tycen','Love','Sr','Attacker',1,65,75,76,78,61,0,0,55,70),(9,1,'Demarion','Dixon','So','Attacker',2,74,88,74,66,92,0,0,46,78),(10,2,'Riddik','Green','Sr','Attacker',2,92,93,93,74,74,0,0,85,85),(11,3,'Malakhi','Watts','Fr','Attacker',2,84,90,70,90,65,0,0,86,79),(12,4,'Zyad','Hernandez','Fr','Attacker',2,61,71,72,63,81,0,0,78,69),(13,5,'Savon','Santana','So','Attacker',2,70,90,74,70,70,0,0,57,74),(14,6,'Damarrion','Chang','Jr','Attacker',2,66,63,92,86,95,0,0,71,80),(15,7,'Alyk','Lopez','Fr','Attacker',2,67,61,67,67,82,0,0,94,68),(16,8,'Azim','Rhodes','Sr','Attacker',2,69,68,70,91,75,0,0,76,74),(17,1,'Bingham','Barker','So','Attacker',3,67,75,68,88,94,0,0,89,78),(18,2,'Braydon','Carr','Sr','Attacker',3,96,84,83,91,81,0,0,40,87),(19,3,'Kmauri','Willis','Jr','Attacker',3,78,76,67,80,89,0,0,79,77),(20,4,'Domonick','Day','So','Attacker',3,96,94,82,74,98,0,0,47,88),(21,5,'Zack','Love','So','Attacker',3,89,67,69,73,76,0,0,74,75),(22,6,'Kuper','Townsend','Jr','Attacker',3,83,74,70,76,74,0,0,62,75),(23,7,'Temujin','Quinn','Jr','Attacker',3,83,71,78,79,62,0,0,85,74),(24,8,'Kerim','Bowen','So','Attacker',3,62,86,99,96,73,0,0,56,82),(25,1,'Kaique','Khan','Jr','Attacker',4,73,82,64,99,84,0,0,89,79),(26,2,'Adlai','Kemp','Jr','Attacker',4,90,68,72,99,74,0,0,56,80),(27,3,'Eren','Poole','Sr','Attacker',4,88,88,83,90,88,0,0,88,87),(28,4,'Fordham','Joyce','Fr','Attacker',4,88,86,93,68,94,0,0,61,86),(29,5,'Bradin','Delgado','Sr','Attacker',4,87,91,60,99,69,0,0,92,80),(30,6,'Dillinger','Mcconnell','Jr','Attacker',4,61,85,79,83,64,0,0,42,73),(31,7,'Zak','Weber','Jr','Attacker',4,97,96,78,89,69,0,0,58,85),(32,8,'Marvion','Pope','So','Attacker',4,80,60,74,81,69,0,0,43,73),(33,1,'Zavion','Gardner','So','Attacker',5,75,92,71,86,98,0,0,42,83),(34,2,'Jonathon','Rojas','So','Attacker',5,92,91,84,94,85,0,0,72,89),(35,3,'Trendon','Huffman','So','Attacker',5,61,88,82,75,88,0,0,62,78),(36,4,'Jerrel','Buchanan','Fr','Attacker',5,90,60,88,74,87,0,0,95,80),(37,5,'Mechel','Cook','Sr','Attacker',5,67,72,67,91,81,0,0,98,75),(38,6,'Melik','Mcmillan','So','Attacker',5,82,87,75,83,90,0,0,81,83),(39,7,'Hudeyfi','Fisher','Fr','Attacker',5,69,77,85,74,65,0,0,54,73),(40,8,'Caspar','Cummings','Jr','Attacker',5,66,66,86,60,73,0,0,88,70),(41,1,'Harland','Francis','Fr','Attacker',6,75,80,71,75,77,0,0,64,75),(42,2,'Azel','Kelly','Fr','Attacker',6,70,75,95,85,99,0,0,50,84),(43,3,'Cinch','Macdonald','Sr','Attacker',6,92,96,70,78,73,0,0,48,81),(44,4,'Jujuan','Cross','Jr','Attacker',6,94,78,90,89,94,0,0,69,89),(45,5,'Dyron','Fry','Fr','Attacker',6,72,81,95,89,68,0,0,59,80),(46,6,'Torris','Hale','Jr','Attacker',6,91,92,77,80,98,0,0,65,87),(47,7,'Nawaf','Webb','Sr','Attacker',6,89,79,89,66,96,0,0,46,84),(48,8,'Miciah','Gates','Fr','Attacker',6,97,92,95,80,78,0,0,70,88),(49,1,'Amram','Mays','Sr','Attacker',7,82,82,79,68,85,0,0,70,79),(50,2,'Jesper','Duke','Sr','Attacker',7,66,93,81,70,73,0,0,99,76),(51,3,'Maison','Calderon','Fr','Attacker',7,90,95,92,61,72,0,0,79,82),(52,4,'Jayvian','Wiggins','Jr','Attacker',7,81,85,67,88,70,0,0,54,77),(53,5,'Lanson','Cannon','Jr','Attacker',7,88,79,94,72,91,0,0,85,85),(54,6,'Marshun','Woodard','Fr','Attacker',7,62,64,69,70,77,0,0,94,68),(55,7,'Kyvin','Allen','Sr','Attacker',7,86,84,85,95,73,0,0,56,84),(56,8,'Navi','Solomon','Jr','Attacker',7,94,60,87,82,71,0,0,50,79),(57,1,'Fredis','Rush','Fr','Attacker',8,77,79,85,73,98,0,0,68,82),(58,2,'Adel','Ryan','Fr','Attacker',8,61,62,80,85,90,0,0,56,75),(59,3,'Bowden','Nelson','Jr','Attacker',8,97,84,70,84,86,0,0,59,84),(60,4,'Kaelyn','Kaiser','So','Attacker',8,86,82,82,83,76,0,0,95,81),(61,5,'Baby','Morse','Jr','Attacker',8,75,91,73,74,60,0,0,47,74),(62,6,'Murat','Carlson','Jr','Attacker',8,68,78,78,82,71,0,0,81,75),(63,7,'Keion','Navarro','So','Attacker',8,73,98,85,99,81,0,0,88,86),(64,8,'Jalan','Prince','So','Attacker',8,86,70,75,88,99,0,0,78,83),(65,1,'Jiram','Rollins','Sr','CD',9,65,60,65,99,99,0,0,99,81),(66,2,'Kwaku','Salas','Fr','CD',9,74,67,75,67,76,0,0,55,72),(67,3,'Dov','Osborne','Sr','CD',9,76,80,81,72,87,0,0,63,80),(68,4,'Neziah','Lucas','Jr','CD',9,64,77,79,74,91,0,0,86,79),(69,5,'Yerik','Barker','So','CD',9,94,98,71,96,98,0,0,40,92),(70,6,'Sagen','Morton','Fr','CD',9,81,78,86,98,87,0,0,90,86),(71,7,'Christain','Lucero','So','CD',9,62,68,96,96,89,0,0,86,83),(72,8,'Domanick','Hensley','So','CD',9,96,79,88,97,76,0,0,98,85),(73,1,'Behrett','Clements','Jr','CD',10,90,93,94,94,84,0,0,47,89),(74,2,'Yad','Cochran','Fr','CD',10,95,77,82,69,99,0,0,42,86),(75,3,'Shelby','Miles','Fr','CD',10,94,99,89,71,92,0,0,45,89),(76,4,'Treveon','Mullen','Jr','CD',10,99,99,86,96,84,0,0,81,91),(77,5,'Justine','Brooks','Sr','CD',10,88,74,63,66,88,0,0,87,77),(78,6,'Julien','Kirby','Jr','CD',10,80,71,78,95,95,0,0,56,85),(79,7,'Viaan','Roberson','So','CD',10,77,69,75,83,78,0,0,75,76),(80,8,'Victor','Bean','Jr','CD',10,68,71,74,87,81,0,0,89,77),(81,1,'Edgard','Bernard','Jr','CF',11,59,77,61,96,73,0,0,73,77),(82,2,'Scottie','Reed','Jr','CF',11,69,98,97,89,67,0,0,51,86),(83,3,'Kru','West','Jr','CF',11,57,60,95,91,87,0,0,63,79),(84,4,'Ephram','Fischer','So','CF',11,98,82,64,88,93,0,0,50,85),(85,5,'Kano','Duke','So','CF',11,66,61,98,87,61,0,0,33,76),(86,6,'Kyrion','Bishop','Jr','CF',11,54,86,85,95,51,0,0,61,79),(87,7,'Aahan','Barrera','Jr','CF',11,64,65,70,85,98,0,0,27,76),(88,8,'Traiden','Mcknight','Fr','CF',11,99,79,88,82,41,0,0,76,80),(89,1,'Ubaidullah','Terry','Fr','CF',12,89,61,80,94,71,0,0,26,81),(90,2,'Traevion','Gordon','Fr','CF',12,61,74,85,84,46,0,0,89,73),(91,3,'Aristides','Mendoza','So','CF',12,60,70,78,93,68,0,0,64,77),(92,4,'Larsen','Mathews','Fr','CF',12,68,84,65,89,71,0,0,85,78),(93,5,'Akio','Vincent','Jr','CF',12,58,68,72,83,52,0,0,38,70),(94,6,'Colsen','Pugh','Jr','CF',12,69,96,88,87,97,0,0,96,87),(95,7,'Amadeo','Newman','Jr','CF',12,91,95,78,90,92,0,0,81,89),(96,8,'Shahid','Stephenson','So','CF',12,75,95,90,85,96,0,0,46,87),(97,1,'Raynav','Archer','So','GK',13,0,0,60,0,0,76,0,87,68),(98,2,'Romel','Best','Sr','GK',13,0,0,90,0,0,77,0,17,83),(99,3,'Cage','Stuart','Fr','GK',13,0,0,88,0,0,82,0,26,85),(100,4,'Shlok','Solis','Fr','GK',13,0,0,88,0,0,99,0,33,93),(101,5,'Shivam','Harper','Jr','GK',13,0,0,84,0,0,83,0,47,83),(102,6,'Pacey','Novak','Fr','GK',13,0,0,85,0,0,87,0,35,86),(103,7,'Kendriel','Levine','Fr','GK',13,0,0,91,0,0,93,0,67,92),(104,8,'Jhael','Lindsey','So','GK',13,0,0,79,0,0,97,0,10,88),(105,1,'Teddy','Case','So','GK',14,0,0,78,0,0,84,0,70,81),(106,2,'Jarron','Mclaughlin','So','GK',14,0,0,78,0,0,85,0,24,81),(107,3,'Yaman','Li','So','GK',14,0,0,79,0,0,76,0,88,77),(108,4,'Tannor','Brooks','Jr','GK',14,0,0,93,0,0,85,0,71,89),(109,5,'Sheamus','Brock','Fr','GK',14,0,0,68,0,0,95,0,48,81),(110,6,'Luc','Madden','Jr','GK',14,0,0,65,0,0,80,0,64,72),(111,7,'Colyn','Wood','Fr','GK',14,0,0,63,0,0,81,0,80,72),(112,8,'Dante','Kirby','Fr','GK',14,0,0,71,0,0,81,0,87,76);
/*!40000 ALTER TABLE players ENABLE KEYS */;


--
-- Table structure for table schedule
--

DROP TABLE IF EXISTS schedule;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE schedule (
  schedule_id INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
  season INTEGER DEFAULT NULL,
  match_number INTEGER DEFAULT NULL,
  home_id INTEGER DEFAULT NULL,
  away_id INTEGER DEFAULT NULL,
  home_goals INTEGER DEFAULT NULL,
  away_goals INTEGER DEFAULT NULL,
  match_type text,
  competition_abb text,
  competition_type text,
  tiebreaker text,
  played text,
  commentary text,
  boxscore text,
  debug text,
  html_report text,
  home_rating double DEFAULT NULL,
  away_rating double DEFAULT NULL
) ;

INSERT INTO schedule VALUES (1,1,1,1,4,0,0,'H','C-1','L','N','N',NULL,NULL,NULL,NULL,1496.40125,1499.020994),(2,1,1,2,3,0,0,'H','C-1','L','N','N',NULL,NULL,NULL,NULL,1488.207702,1476.263766),(3,1,1,5,8,0,0,'H','C-1','L','N','N',NULL,NULL,NULL,NULL,1485.808381,1502.012449),(4,1,1,6,7,0,0,'H','C-1','L','N','N',NULL,NULL,NULL,NULL,1473.449435,1482.283177),(5,1,2,3,1,0,0,'H','C-2','L','N','N',NULL,NULL,NULL,NULL,1515.827734,1544.370634),(6,1,2,4,2,0,0,'H','C-2','L','N','N',NULL,NULL,NULL,NULL,1467.114849,1492.553366),(7,1,2,7,5,0,0,'H','C-2','L','N','N',NULL,NULL,NULL,NULL,1520.512221,1476.178695),(8,1,2,8,6,0,0,'H','C-2','L','N','N',NULL,NULL,NULL,NULL,1509.402788,1504.912127),(9,1,3,1,2,0,0,'H','C-3','L','N','N',NULL,NULL,NULL,NULL,1507.811574,1536.529204),(10,1,3,3,4,0,0,'H','C-3','L','N','N',NULL,NULL,NULL,NULL,1489.951146,1541.389396),(11,1,3,5,6,0,0,'H','C-3','L','N','N',NULL,NULL,NULL,NULL,1475.787929,1529.795095),(12,1,3,7,8,0,0,'H','C-3','L','N','N',NULL,NULL,NULL,NULL,1509.198624,1490.943697),(13,1,4,1,8,0,0,'H','NC-1','N','N','N',NULL,NULL,NULL,NULL,1502.76587,1507.797717),(14,1,4,2,7,0,0,'H','NC-1','N','N','N',NULL,NULL,NULL,NULL,1533.070487,1499.709751),(15,1,4,3,6,0,0,'H','NC-1','N','N','N',NULL,NULL,NULL,NULL,1446.395964,1521.648666),(16,1,4,4,5,0,0,'H','NC-1','N','N','N',NULL,NULL,NULL,NULL,1517.343197,1455.542116),(17,1,5,4,1,0,0,'H','C-4','L','N','N',NULL,NULL,NULL,NULL,1496.40125,1499.020994),(18,1,5,3,2,0,0,'H','C-4','L','N','N',NULL,NULL,NULL,NULL,1488.207702,1476.263766),(19,1,5,8,5,0,0,'H','C-4','L','N','N',NULL,NULL,NULL,NULL,1485.808381,1502.012449),(20,1,5,7,6,0,0,'H','C-4','L','N','N',NULL,NULL,NULL,NULL,1473.449435,1482.283177),(21,1,6,3,1,0,0,'H','C-5','L','N','N',NULL,NULL,NULL,NULL,1515.827734,1544.370634),(22,1,6,4,2,0,0,'H','C-5','L','N','N',NULL,NULL,NULL,NULL,1467.114849,1492.553366),(23,1,6,7,5,0,0,'H','C-5','L','N','N',NULL,NULL,NULL,NULL,1520.512221,1476.178695),(24,1,6,8,6,0,0,'H','C-5','L','N','N',NULL,NULL,NULL,NULL,1509.402788,1504.912127),(25,1,7,2,1,0,0,'H','C-6','L','N','N',NULL,NULL,NULL,NULL,1507.811574,1536.529204),(26,1,7,4,3,0,0,'H','C-6','L','N','N',NULL,NULL,NULL,NULL,1489.951146,1541.389396),(27,1,7,6,5,0,0,'H','C-6','L','N','N',NULL,NULL,NULL,NULL,1475.787929,1529.795095),(28,1,7,8,7,0,0,'H','C-6','L','N','N',NULL,NULL,NULL,NULL,1509.198624,1490.943697),(29,1,8,8,2,0,0,'H','NC-2','N','N','N',NULL,NULL,NULL,NULL,1502.76587,1507.797717),(30,1,8,7,1,0,0,'H','NC-2','N','N','N',NULL,NULL,NULL,NULL,1533.070487,1499.709751),(31,1,8,6,4,0,0,'H','NC-2','N','N','N',NULL,NULL,NULL,NULL,1446.395964,1521.648666),(32,1,8,5,3,0,0,'H','NC-2','N','N','N',NULL,NULL,NULL,NULL,1517.343197,1455.542116),(33,1,9,1,4,0,0,'H','C-7','L','N','N',NULL,NULL,NULL,NULL,1496.40125,1499.02099),(34,1,9,2,3,0,0,'H','C-7','L','N','N',NULL,NULL,NULL,NULL,1488.2077,1476.26377),(35,1,9,5,8,0,0,'H','C-7','L','N','N',NULL,NULL,NULL,NULL,1485.80838,1502.01245),(36,1,9,6,7,0,0,'H','C-7','L','N','N',NULL,NULL,NULL,NULL,1473.44943,1482.28318),(37,1,10,3,1,0,0,'H','C-8','L','N','N',NULL,NULL,NULL,NULL,1515.82773,1544.37063),(38,1,10,4,2,0,0,'H','C-8','L','N','N',NULL,NULL,NULL,NULL,1467.11485,1492.55337),(39,1,10,7,5,0,0,'H','C-8','L','N','N',NULL,NULL,NULL,NULL,1520.51222,1476.17869),(40,1,10,8,6,0,0,'H','C-8','L','N','N',NULL,NULL,NULL,NULL,1509.40279,1504.91213),(41,1,11,1,2,0,0,'H','C-9','L','N','N',NULL,NULL,NULL,NULL,1507.81157,1536.5292),(42,1,11,3,4,0,0,'H','C-9','L','N','N',NULL,NULL,NULL,NULL,1489.95115,1541.3894),(43,1,11,5,6,0,0,'H','C-9','L','N','N',NULL,NULL,NULL,NULL,1475.78793,1529.79509),(44,1,11,7,8,0,0,'H','C-9','L','N','N',NULL,NULL,NULL,NULL,1509.19862,1490.9437),(45,1,12,1,6,0,0,'H','NC-3','N','N','N',NULL,NULL,NULL,NULL,1502.76587,1507.79772),(46,1,12,2,5,0,0,'H','NC-3','N','N','N',NULL,NULL,NULL,NULL,1533.07049,1499.70975),(47,1,12,3,8,0,0,'H','NC-3','N','N','N',NULL,NULL,NULL,NULL,1446.39596,1521.64867),(48,1,12,4,7,0,0,'H','NC-3','N','N','N',NULL,NULL,NULL,NULL,1517.3432,1455.54212),(49,1,13,4,1,0,0,'H','C-10','L','N','N',NULL,NULL,NULL,NULL,0,0),(50,1,13,3,2,0,0,'H','C-10','L','N','N',NULL,NULL,NULL,NULL,0,0),(51,1,13,8,5,0,0,'H','C-10','L','N','N',NULL,NULL,NULL,NULL,0,0),(52,1,13,7,6,0,0,'H','C-10','L','N','N',NULL,NULL,NULL,NULL,0,0),(53,1,14,3,1,0,0,'H','C-11','L','N','N',NULL,NULL,NULL,NULL,0,0),(54,1,14,4,2,0,0,'H','C-11','L','N','N',NULL,NULL,NULL,NULL,0,0),(55,1,14,7,5,0,0,'H','C-11','L','N','N',NULL,NULL,NULL,NULL,0,0),(56,1,14,8,6,0,0,'H','C-11','L','N','N',NULL,NULL,NULL,NULL,0,0),(57,1,15,2,1,0,0,'H','C-12','L','N','N',NULL,NULL,NULL,NULL,0,0),(58,1,15,4,3,0,0,'H','C-12','L','N','N',NULL,NULL,NULL,NULL,0,0),(59,1,15,6,5,0,0,'H','C-12','L','N','N',NULL,NULL,NULL,NULL,0,0),(60,1,15,8,7,0,0,'H','C-12','L','N','N',NULL,NULL,NULL,NULL,0,0),(61,1,16,8,4,0,0,'H','NC-4','N','N','N',NULL,NULL,NULL,NULL,0,0),(62,1,16,7,3,0,0,'H','NC-4','N','N','N',NULL,NULL,NULL,NULL,0,0),(63,1,16,6,2,0,0,'H','NC-4','N','N','N',NULL,NULL,NULL,NULL,0,0),(64,1,16,5,1,0,0,'H','NC-4','N','N','N',NULL,NULL,NULL,NULL,0,0);

DROP TABLE IF EXISTS standings;
CREATE TABLE standings (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  season varchar(100) DEFAULT '1',
  team_id INTEGER DEFAULT NULL,
  wins INTEGER DEFAULT '0',
  losses INTEGER DEFAULT '0',
  goals_scored INTEGER DEFAULT '0',
  goals_against INTEGER DEFAULT '0',
  competition_abb varchar(10) DEFAULT NULL,
  competition_type varchar(10) DEFAULT NULL,
  group_id varchar(100) DEFAULT ''
) ;

INSERT INTO standings VALUES (1,1,1,0,0,0,0,'C-1','L',''),(2,1,2,0,0,0,0,'C-1','L',''),(3,1,3,0,0,0,0,'C-1','L',''),(4,1,4,0,0,0,0,'C-1','L',''),(5,1,5,0,0,0,0,'C-2','L',''),(6,1,6,0,0,0,0,'C-2','L',''),(7,1,7,0,0,0,0,'C-2','L',''),(8,1,8,0,0,0,0,'C-2','L','');


DROP TABLE IF EXISTS teams;
CREATE TABLE teams (
  team_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name varchar(30) NOT NULL,
  city varchar(30) NOT NULL,
  nickname varchar(30) NOT NULL,
  coach_id INTEGER NOT NULL,
  abb varchar(3) NOT NULL,
  short_name varchar(30) NOT NULL,
  division varchar(100) DEFAULT NULL,
  cp INTEGER NOT NULL DEFAULT '0',
  cp_used INTEGER NOT NULL DEFAULT '0',
  recruiting_poINTEGERs INTEGER NOT NULL DEFAULT '0',
  active char(1) NOT NULL DEFAULT 'Y',
  overall INTEGER NOT NULL DEFAULT '0',
  aggression INTEGER NOT NULL DEFAULT '0',
  logo text NOT NULL Default '0'
) ;

INSERT INTO teams VALUES (1,'St. Charles','St. Charles','Scarecrows',1,'STC','St. Charles','West',62,0,967,'Y',79,69, '0'),(2,'Columbia','Columbia','Crazy Tomatoes',1,'CCT','Columbia','West',76,0,1463,'Y',81,58,'0'),(3,'New Orleans','New Orleans','Swamp Rats',1,'NOS','New Orleans','West',63,0,1531,'Y',81,66, '0'),(4,'Baton Rouge','Baton Rouge','Bananas',1,'BRB','Baton Rouge','West',62,0,1792,'Y',83,70, '0'),(5,'Carlsbad','Carlsbad','Chameleons',1,'CC','Carlsbad','East',66,0,1315,'Y',79,64, '0'),(6,'Quincy','Quincy','Rabid Biting Mules',1,'QRM','Quincy','East',60,0,1527,'Y',79,68,'0'),(7,'Mendon','Mendon','Mushrooms',1,'MM','Mendon','East',59,0,1289,'Y',81,70,'0'),(8,'Antioch','Antioch','Anglerfish',1,'AA','Antioch','East',71,0,1338,'Y',79,66,'0');
