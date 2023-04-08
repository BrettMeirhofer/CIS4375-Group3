CREATE TABLE Country(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	country_name nvarchar(60),
);

CREATE TABLE CustomerStatus(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	status_name nvarchar(40),
	status_desc nvarchar(200) NULL,
	is_active bit DEFAULT 1,
);

CREATE TABLE ProductStatus(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	status_name nvarchar(40),
	status_desc nvarchar(200) NULL,
	is_active bit DEFAULT 1,
);

CREATE TABLE PromoStatus(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	status_name nvarchar(40),
	status_desc nvarchar(200) NULL,
	is_active bit DEFAULT 1,
);

CREATE TABLE ProductTag(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	tag_name nvarchar(40),
	tag_desc nvarchar(200) NULL,
);

CREATE TABLE Brand(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	brand_name nvarchar(40),
	brand_desc nvarchar(200) NULL,
	brand_site nvarchar(200),
);

CREATE TABLE StateProvince(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	state_name nvarchar(60),
	country_id int FOREIGN KEY REFERENCES Country(id),
);

CREATE TABLE Product(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	product_name nvarchar(80),
	product_desc nvarchar(200) NULL,
	product_price numeric(19,4) DEFAULT 0.0,
	product_brand_id int FOREIGN KEY REFERENCES Brand(id) NULL,
	product_status_id int FOREIGN KEY REFERENCES ProductStatus(id) NULL,
	created_date date,
);

CREATE TABLE Promo(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	promo_name nvarchar(80),
	promo_code nvarchar(10) UNIQUE,
	promo_status_id int FOREIGN KEY REFERENCES PromoStatus(id),
	created_date date,
	end_date date NULL,
	promo_desc nvarchar(400) NULL,
);

CREATE TABLE ProductProductTag(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	product_id int FOREIGN KEY REFERENCES Product(id),
	product_tag_id int FOREIGN KEY REFERENCES ProductTag(id),
	created_date date,
);

CREATE TABLE ProductImage(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	product_id int FOREIGN KEY REFERENCES Product(id),
	image_url nvarchar(200),
	image_caption nvarchar(200) NULL,
);

CREATE TABLE ProductPromo(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	product_id int FOREIGN KEY REFERENCES Product(id),
	promo_id int FOREIGN KEY REFERENCES Promo(id),
	current_price numeric(19,4) DEFAULT 0.0,
	promo_price numeric(19,4) DEFAULT 0.0,
);

CREATE TABLE Customer(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	first_name nvarchar(200),
	last_name nvarchar(200),
	email nvarchar(254),
	created_date date,
	customer_status_id int FOREIGN KEY REFERENCES CustomerStatus(id),
	phone_number nvarchar(12) NULL,
	zip_code nvarchar(10),
	city nvarchar(35) DEFAULT 'Houston',
	address nvarchar(100) DEFAULT '3242 StreetName',
	state_id int FOREIGN KEY REFERENCES StateProvince(id),
	country_id int FOREIGN KEY REFERENCES Country(id),
);

CREATE TABLE CustomerPromo(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	customer_id int FOREIGN KEY REFERENCES Customer(id),
	promo_id int FOREIGN KEY REFERENCES Promo(id),
	total_spent numeric(19,4) DEFAULT 0.0,
	total_discount numeric(19,4) DEFAULT 0.0,
	created_date date,
);

CREATE TABLE CustomerProductPromo(
	id int NOT NULL PRIMARY KEY IDENTITY(1,1),
	customer_promo_id int FOREIGN KEY REFERENCES CustomerPromo(id),
	product_id int FOREIGN KEY REFERENCES Product(id),
	normal_price numeric(19,4) DEFAULT 0.0,
	promo_price numeric(19,4) DEFAULT 0.0,
	line_total numeric(19,4) DEFAULT 0.0,
	line_discount numeric(19,4) DEFAULT 0.0,
	quantity int DEFAULT 0,
);

