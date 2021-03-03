-- add drop table for all your tables if they exist
-- DROP TABLE IF EXISTS table_name CASCADE;


-- add create table for all your tabled

-- add drop table for all your tables if they exist
-- DROP TABLE IF EXISTS table_name CASCADE;


-- add create table for all your tabled
-- User, Product, Orders, Catagory 
-- AUTO_INCREMENT = generate a unique identity for new rows
create table user (
  `userId` BIGINT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NULL DEFAULT NULL,
  `middleName` VARCHAR(50) NULL DEFAULT NULL,
  `lastName` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(50) NULL,
  `passwordHash` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`userId`)
);

INSERT INTO user (username, middleName, lastName)
VALUES ('value1', 'value2', 'value3'); 

create table product (
    `productId` BIGINT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(75) NOT NULL,
    `categoryId` BIGINT NOT NULL,
    `price` FLOAT NOT NULL DEFAULT 0,
    `quantity` SMALLINT(6) NOT NULL DEFAULT 0,
    PRIMARY KEY (`productId`),
);

create table category (
    `categoryId` BIGINT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(75) NOT NULL,
    PRIMARY KEY (`categoryId`)
);

create table order (
    `orderId` BIGINT NOT NULL AUTO_INCREMENT,
    `userId` BIGINT NULL DEFAULT NULL,
    `productId` BIGINT NULL DEFAULT NULL,
    `quantity` SMALLINT(6) NOT NULL DEFAULT 0,
    `date` DATE,
    PRIMARY KEY (`orderId`, `productId`)
);

-- add insert statements to populate your tables

-- add insert statements to populate your tables
