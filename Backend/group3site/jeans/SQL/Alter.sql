ALTER TABLE Product ADD
	product_brand_id int FOREIGN KEY REFERENCES Brand(id),
	product_status_id int FOREIGN KEY REFERENCES ProductStatus(id);

ALTER TABLE Promo ADD
	promo_status_id int FOREIGN KEY REFERENCES PromoStatus(id);

ALTER TABLE ProductProductTag ADD
	product_id int FOREIGN KEY REFERENCES Product(id),
	product_tag_id int FOREIGN KEY REFERENCES ProductTag(id);

ALTER TABLE ProductImage ADD
	product_id int FOREIGN KEY REFERENCES Product(id),
	product_image_id int FOREIGN KEY REFERENCES Image(id);

ALTER TABLE ProductPromo ADD
	product_id int FOREIGN KEY REFERENCES Product(id),
	promo_id int FOREIGN KEY REFERENCES Promo(id);

