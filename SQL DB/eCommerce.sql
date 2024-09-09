drop database eCommerce;
create database eCommerce;
use eCommerce;

create table products(
product_id int auto_increment primary key,
product_name  varchar(255)not null,
category  varchar(255)not null,
image varchar(255)not null,
price  varchar(255) not null,
quantity      varchar(255) not null,
discount  varchar(255),
discount_price varchar(255),
description   varchar(255) not null,
ratings varchar(255),
colour varchar(255) not null,
status varchar(255) 
);

create table customers(customer_id int auto_increment primary key,
name   varchar(255)not null,
email  varchar(255)unique not null,
phone  varchar(255)unique not null,
password varchar(255) not null,
address  varchar(255)not null
);

create table cart(cart_id int auto_increment primary key,
customer_id int not null,
date datetime default current_timestamp,
status   varchar(255)not null,
foreign key (customer_id) references customers(customer_id)
);

create table orders(order_id int auto_increment primary key,
product_id int not null,
cart_id int not null,
quantity varchar(255)not null,
date datetime default current_timestamp,
status varchar(255)not null,
total_price varchar(255),
foreign key(product_id) references products(product_id),
foreign key(cart_id) references cart(cart_id)
);

