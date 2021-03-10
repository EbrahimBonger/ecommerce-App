-- add drop table for all your tables if they exist
-- DROP TABLE IF EXISTS table_name CASCADE;


-- add create table for all your tabled

-- add drop table for all your tables if they exist
-- DROP TABLE IF EXISTS table_name CASCADE;


-- add create table for all your tabled
-- User, Product, Orders, Catagory 
-- AUTO_INCREMENT = generate a unique identity for new rows

DROP TABLE IF EXISTS user;
CREATE TABLE `user` (
  `userId` BIGINT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NULL DEFAULT NULL,
  `first_name` VARCHAR(50) NULL DEFAULT NULL,
  `last_name` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(50) NULL,
  `passwordHash` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`userId`)
);

INSERT INTO `user` ( `username`, `first_name`, `last_name`, `email`, `passwordHash`) VALUES
('user', 'user', 'user', 'user', 'pass' );

INSERT INTO `user` ( `username`, `first_name`, `last_name`, `email`, `passwordHash`) VALUES
('user', 'user', 'user', 'user', 'pass' );




DROP TABLE IF EXISTS product;
CREATE TABLE `product` (
    `productId` BIGINT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(50) NULL DEFAULT NULL,
    `categoryname` VARCHAR(50) NULL DEFAULT NULL,
    `price` FLOAT NOT NULL DEFAULT 0,
    `quantity` SMALLINT(6) NOT NULL DEFAULT 0,
    PRIMARY KEY (`productId`)
);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('shampoo','self-care', 10, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('conditioner','self-care', 10, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('lotion','cosmotics', 10, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('soap','home-cleaning', 10, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('detergent','home-cleaning', 10, 10);



DROP TABLE IF EXISTS category;
CREATE TABLE `category` (
    `categoryId` BIGINT NOT NULL AUTO_INCREMENT,
    `categoryname` VARCHAR(75) NOT NULL,
    PRIMARY KEY (`categoryId`)
);

INSERT INTO `category` (`categoryname`) VALUES
('self-care');

INSERT INTO `category` (`categoryname`) VALUES
('cosmotics');

INSERT INTO `category` (`categoryname`) VALUES
('home-cleaning');

DROP TABLE IF EXISTS orders;
CREATE TABLE `orders` (
    `orderId` BIGINT NOT NULL AUTO_INCREMENT,
    `userId` BIGINT NULL DEFAULT NULL,
    `productId` BIGINT NOT NULL,
    `quantity` SMALLINT(6) NOT NULL DEFAULT 0,
    `price` FLOAT NOT NULL DEFAULT 0,
    `date` DATE,
    PRIMARY KEY (`orderId`, `productId`)
);

-- add insert statements to populate your tables


