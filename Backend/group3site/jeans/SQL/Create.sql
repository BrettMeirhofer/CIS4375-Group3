CREATE TABLE Image(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	image_url nvarchar(200) NOT NULL,
	image_caption nvarchar(200),
);

CREATE TABLE CustomerStatus(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	status_name nvarchar(40) NOT NULL,
	status_desc nvarchar(200),
	is_active bit NOT NULL DEFAULT 1,
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
	customer_status_id int FOREIGN KEY REFERENCES CustomerStatus(id),
);

CREATE TABLE Product(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	product_name nvarchar(80) NOT NULL,
	product_desc nvarchar(200),
	product_price numeric NOT NULL DEFAULT 0,
	product_brand_id int FOREIGN KEY REFERENCES Brand(id),
	product_status_id int FOREIGN KEY REFERENCES ProductStatus(id),
	created_date date NOT NULL,
);

CREATE TABLE Promo(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	promo_name nvarchar(80) NOT NULL,
	promo_code nvarchar(10) NOT NULL UNIQUE,
	promo_status_id int FOREIGN KEY REFERENCES PromoStatus(id),
	created_date date NOT NULL,
);

CREATE TABLE ProductProductTag(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	product_id int FOREIGN KEY REFERENCES Product(id),
	product_tag_id int FOREIGN KEY REFERENCES ProductTag(id),
	created_date date NOT NULL,
);

CREATE TABLE ProductImage(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	product_id int FOREIGN KEY REFERENCES Product(id),
	product_image_id int FOREIGN KEY REFERENCES Image(id),
);

CREATE TABLE ProductPromo(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	product_id int FOREIGN KEY REFERENCES Product(id),
	promo_id int FOREIGN KEY REFERENCES Promo(id),
);

