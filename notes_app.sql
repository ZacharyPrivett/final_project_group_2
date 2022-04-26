DROP DATABASE IF EXISTS notes;

CREATE DATABASE IF NOT EXISTS notes;

USE notes;

CREATE TABLE IF NOT EXISTS users(
    user_id INT AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    pw VARCHAR(255) NOT NULL,
    PRIMARY KEY(user_id)
    );

CREATE TABLE IF NOT EXISTS note(
    note_id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    course VARCHAR(255) NOT NULL,
    descript VARCHAR(255) NULL,
    content TEXT NOT NULL,
    creator_id INT NOT NULL,
    PRIMARY KEY(note_id),
    FOREIGN KEY(creator_id) REFERENCES users(user_id)
    );

CREATE TABLE IF NOT EXISTS comments(
    comment_id INT AUTO_INCREMENT,
    content TEXT NOT NULL,
    time_stamp TEXT NOT NULL,
    commenter_id INT,
    thread_id INT NOT NULL,
    PRIMARY KEY(comment_id),
    FOREIGN KEY(commenter_id) REFERENCES users(user_id),
    FOREIGN KEY(thread_id) REFERENCES note(note_id)
    );