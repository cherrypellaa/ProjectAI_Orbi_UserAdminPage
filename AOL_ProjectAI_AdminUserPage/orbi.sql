BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "activity_log" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER,
	"action"	VARCHAR(255),
	"location"	VARCHAR(100),
	"timestamp"	DATETIME,
	PRIMARY KEY("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(100) NOT NULL,
	"password"	VARCHAR(200) NOT NULL,
	"role"	VARCHAR(20) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("username")
);
INSERT INTO "activity_log" VALUES (1,4,'Location Update','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:06:02.109945');
INSERT INTO "activity_log" VALUES (2,4,'Location Update','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:07:01.698237');
INSERT INTO "activity_log" VALUES (3,4,'Detected objects: person','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:08:00.184206');
INSERT INTO "activity_log" VALUES (4,4,'Detected objects: person','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:08:26.630631');
INSERT INTO "activity_log" VALUES (5,4,'object detection stopped.','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:08:39.897124');
INSERT INTO "activity_log" VALUES (6,4,'Location Update','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:15:53.878139');
INSERT INTO "activity_log" VALUES (7,4,'take object.','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:17:18.562581');
INSERT INTO "activity_log" VALUES (8,4,'Detected objects: person','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:17:52.718222');
INSERT INTO "activity_log" VALUES (9,4,'object detection stopped.','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:18:08.519448');
INSERT INTO "activity_log" VALUES (10,4,'Detected objects: person','Jalan Biru Laut Timur, RW 08, Kelapa Gading Timur, Kelapa Gading, Jakarta Utara, Daerah Khusus ibukota Jakarta, Jawa, 14240, Indonesia','2025-06-09 09:18:26.734599');
INSERT INTO "user" VALUES (1,'admin','scrypt:32768:8:1$JPfyZuZIT3wmJA6E$7eeabcd5e1b1a45d17a24c63a4acc7ecdee3e60f467c6c313eba0a8c7d8c83a05ea22fc5f1c3838943c2649befb4d61859de361c2c25fd67cd5b5190ad59cd52','admin');
INSERT INTO "user" VALUES (2,'user','scrypt:32768:8:1$W6KY00UAr6OBDjHP$f3238c8736dbdfaafd1626855a7702320ee1bb54973512593e9421e9f8bcc3a04fd39a338181b2b0a5c4442464569b329ce27a36dd6ff2542350b2136d1438c7','user');
INSERT INTO "user" VALUES (3,'ricel','scrypt:32768:8:1$agL30h3kZcc2zy7D$37150fa5f1353439bd0ea0f61f58227f17443a751de7c356962e1586c70f6a96bd6188404bf9c4197f0c8dbb5d100b0bf8688808f8466417e6736a182d21f347','admin');
INSERT INTO "user" VALUES (4,'marvela','scrypt:32768:8:1$FrJMi3LSgifvQlfx$649d8e91c41ed2d38e5a44514d6528ec47d0c1422b8c9e0f9f54e79d412a6f6e2882bf9505ba8a7f3b1e37c521b0b411e4dbbfc020f6d7857c495871afc1dac0','user');
COMMIT;
