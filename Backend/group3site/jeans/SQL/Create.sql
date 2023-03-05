CREATE TABLE Image(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	image_url nvarchar(200) NOT NULL,
	image_caption nvarchar(200),
);

CREATE TABLE ProductStatus(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	status_name nvarchar(40) NOT NULL,
	status_desc nvarchar(200),
	is_active bit NOT NULL DEFAULT 1,
);

CREATE TABLE PromoStatus(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	status_name nvarchar(40) NOT NULL,
	status_desc nvarchar(200),
	is_active bit NOT NULL DEFAULT 1,
);

CREATE TABLE ProductTag(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	status_name nvarchar(40) NOT NULL,
	status_desc nvarchar(200),
	is_active bit NOT NULL DEFAULT 1,
);

CREATE TABLE Brand(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	brand_name nvarchar(80) NOT NULL,
	brand_desc nvarchar(200),
	brand_site nvarchar(200) NOT NULL,
);

CREATE TABLE Customer(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	first_name nvarchar(200) NOT NULL,
	last_name nvarchar(200) NOT NULL,
	email nvarchar(254) NOT NULL,
	created_date date NOT NULL,
);

CREATE TABLE Product(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	product_name nvarchar(80) NOT NULL,
	product_desc nvarchar(200),
	product_price numeric NOT NULL DEFAULT 0,
	created_date date NOT NULL,
);

CREATE TABLE Promo(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	promo_name nvarchar(80) NOT NULL,
	promo_code nvarchar(10) NOT NULL UNIQUE,
	created_date date NOT NULL,
);

CREATE TABLE ProductProductTag(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	created_date date NOT NULL,
);

CREATE TABLE ProductImage(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
);

CREATE TABLE ProductPromo(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
);

