
#-- ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~
#--TO RESET EXECUTE THE FOLLOWING STEPS IN ORDER
#--RUN DDL
#--RUN DML
#--RUN THE FOLLOWING QUERY: CALL reset_all_tables()
#-- ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~

DROP PROCEDURE IF EXISTS reset_all_tables;
DROP PROCEDURE IF EXISTS drop_all;
DROP PROCEDURE IF EXISTS create_all_tables;
-- DROP PROCEDURE IF EXISTS insert_sample_data;

CREATE PROCEDURE drop_all() 
BEGIN

DROP TABLE IF EXISTS tutor;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS expertise;
DROP TABLE IF EXISTS availability;
DROP TABLE IF EXISTS session;
-- DROP TABLE IF EXISTS user;

END;


CREATE PROCEDURE create_all_tables()
BEGIN

CREATE TABLE tutor(
    tutor_vnumber VARCHAR(255),
    tutor_name VARCHAR(255)
);

-----------Just because php is being dumb with tutor-------------
CREATE TABLE tutor1(
    tutor_vnumber VARCHAR(255),
    tutor_name VARCHAR(255)
);

--
-- CREATE TABLE user(
--     user VARCHAR(255),
--     password VARCHAR(255)
-- );

CREATE TABLE course(
    course_code VARCHAR(255)
);

CREATE TABLE expertise(
    expertise_vnumber VARCHAR(255),
    expertise_code VARCHAR(255)
);

CREATE TABLE availability(
    availability_vnumber VARCHAR(255),
    availability_day VARCHAR(255),
    availability_time VARCHAR(255)
);

CREATE TABLE session(
    session_vnumber VARCHAR(255),
    session_code VARCHAR(255),
    session_day VARCHAR(255),
    session_time VARCHAR(255)
);

END;

-- CREATE PROCEDURE insert_sample_data()
-- BEGIN
--     INSERT INTO user(user, password) VALUES('admin', '123');
-- END;

CREATE PROCEDURE reset_all_tables() 
BEGIN
    CALL drop_all();
    CALL create_all_tables();
    -- CALL insert_sample_data();
    -- CALL create_views();
END;






 
