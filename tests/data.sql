INSERT INTO users (username, password, email)
VALUES
("test1", "pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f", "test1@gamil.com"),
("test2", "pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79", "test2@gmail.com"),
("test3", "pbkdf2:sha256:50000$DJPfsx3N3fghgh$urffffsadrfrfkkutkfj945dsdddffffffsvvd58594439afd485fddee8", "test3@gmail.com");

INSERT INTO requests (sender_id, receiver_id)
VALUES (1, 2);
