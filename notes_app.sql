CREATE DATABASE users;
USE users;
CREATE DATABASE note;
USE note;
CREATE DATABASE course;
USE course;

CREATE TABLE IF NOT EXISTS users(
	user_id INT AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    pass VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    notes VARCHAR(255) NULL,
    PRIMARY KEY(user_id)
    );
    
CREATE TABLE IF NOT EXISTS note(
	note_id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    course VARCHAR(255) NOT NULL,
    descript VARCHAR(255) NULL,
    creator_id INT NULL,
    PRIMARY KEY(note_id),
    FOREIGN KEY(creator_id) REFERENCES users(user_id)
    );

CREATE TABLE IF NOT EXISTS course (
    user_id  INT NOT NULL,
    note_id  INT NOT NULL,
    _name VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id, note_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (note_id) REFERENCES note(note_id)
);