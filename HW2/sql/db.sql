-- CREATE SCHEMA dbsys IF NOT EXIST;

CREATE TABLE student_attendance (
  id INT PRIMARY KEY AUTO_INCREMENT,
  student_id VARCHAR(20) NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (student_id)
);

CREATE TABLE student_info (
  id INT AUTO_INCREMENT,
  student_id VARCHAR(20) NOT NULL,
  name VARCHAR(255) NOT NULL,
  dept_id VARCHAR(20) NOT NULL,
  dob DATETIME NOT NULL,
  UNIQUE (id),
  PRIMARY KEY (student_id),
  UNIQUE (student_id)
);

CREATE TABLE department (
  id INT AUTO_INCREMENT,
  dept_id VARCHAR(20) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  num_of_faculty INT DEFAULT 0,
  UNIQUE(dept_id)
);

