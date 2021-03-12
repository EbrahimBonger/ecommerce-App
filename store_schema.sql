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

DROP TABLE IF EXISTS history;
CREATE TABLE `history` (
    `userId` BIGINT,
    `orderId` BIGINT,
    `productId` BIGINT
    
);

-- insert product history

INSERT INTO `history` ( `userId`, `orderId`, `productId`) VALUES
(1, 1, 1);

INSERT INTO `history` ( `userId`, `orderId`, `productId`) VALUES
(1, 1, 3);

INSERT INTO `history` ( `userId`, `orderId`, `productId`) VALUES
(1, 1, 5);

INSERT INTO `history` ( `userId`, `orderId`, `productId`) VALUES
(1, 2, 7);

INSERT INTO `history` ( `userId`, `orderId`, `productId`) VALUES
(1, 2, 9);

INSERT INTO `history` ( `userId`, `orderId`, `productId`) VALUES
(1, 2, 11);

INSERT INTO `history` ( `userId`, `orderId`, `productId`) VALUES
(1, 3, 13);

INSERT INTO `history` ( `userId`, `orderId`, `productId`) VALUES
(1, 3, 15);

INSERT INTO `history` ( `userId`, `orderId`, `productId`) VALUES
(1, 3, 17);

-- regidter two sample users

INSERT INTO `user` ( `username`, `first_name`, `last_name`, `email`, `passwordHash`) VALUES
('user', 'user', 'user', 'user', 'pass' );

INSERT INTO `user` ( `username`, `first_name`, `last_name`, `email`, `passwordHash`) VALUES
('user2', 'user2', 'user2', 'user2', 'pass2' );


DROP TABLE IF EXISTS product;
CREATE TABLE `product` (
    `productId` BIGINT AUTO_INCREMENT,
    `title` VARCHAR(50) NULL DEFAULT NULL,
    `categoryname` VARCHAR(50) NULL DEFAULT NULL,
    `price` FLOAT NOT NULL DEFAULT 0,
    `quantity` SMALLINT(6) NOT NULL DEFAULT 0,
    PRIMARY KEY (`productId`)
);





-- Oil & moisturizer category

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Growth Oil','Oil & moisturizer', 14, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Sandalwood Balm','Oil & moisturizer', 9, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Beard Cream','Oil & moisturizer', 10, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Growth Vatamin Spray','Oil & moisturizer', 16, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Cedar Beard Oil','Oil & moisturizer', 7, 10);


-- Accelerators catedory

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Beard Shampoo','Accelerators', 12, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Sandalwood Oil','Accelerators', 17, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Ceadr Beard Oil','Accelerators', 14, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Riptide Beard Spray','Accelerators', 17, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Riptide Beard Oil','Accelerators', 13, 10);

-- Clean & hold category

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Beard Wash','Clean & hold', 19, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Beard Wax','Clean & hold', 11, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Body Wash','Clean & hold', 15, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Hair Pomade','Clean & hold', 14, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Facial Wash','Clean & hold', 18, 10);

-- Grooming

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Beard Trimmer','Grooming', 89, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Beard Brush','Grooming', 5, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Folding Comb','Grooming', 4, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Beard Scissor','Grooming', 24, 10);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Edge Razor','Grooming', 34, 10);


-- Merch category

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Snapback Army Green','Merch', 10, 13);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Snapback Heather Gray','Merch', 10, 13);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Dad Hat','Merch', 10, 13);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Island Hoodie','Merch', 10, 13);

INSERT INTO `product` (`title`, `categoryname`, `price`, `quantity`) VALUES
('Island T-Shirt','Merch', 10, 13);









DROP TABLE IF EXISTS category;
CREATE TABLE `category` (
    `categoryId` BIGINT AUTO_INCREMENT,
    `categoryname` VARCHAR(75) NOT NULL,
    PRIMARY KEY (`categoryId`)
);



DROP TABLE IF EXISTS orders;
CREATE TABLE `orders` (
    `orderId` BIGINT AUTO_INCREMENT,
    `userId` BIGINT,
    `date` DATE,
    PRIMARY KEY (`orderId`, `userId`)
    
);
 -- '%y-%m-%d' YYYY-MM-DD
INSERT INTO `orders` ( `orderId`, `userId`, `date`) VALUES
(1, 1, '2020-05-09' );

INSERT INTO `orders` ( `orderId`, `userId`, `date`) VALUES
(3, 1, '2021-11-03' );

INSERT INTO `orders` ( `orderId`, `userId`, `date`) VALUES
(2, 1, '2020-07-12' );






-- add insert statements to populate your tables


