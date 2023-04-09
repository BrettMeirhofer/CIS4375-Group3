BULK INSERT CustomerStatus
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\CustomerStatus.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductStatus
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\ProductStatus.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT PromoStatus
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\PromoStatus.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductTag
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\ProductTag.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT Brand
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\Brand.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT Product
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\Product.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT Promo
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\Promo.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT Customer
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\Customer.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductProductTag
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\ProductProductTag.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductImage
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\ProductImage.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductPromo
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\ProductPromo.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT CustomerPromo
FROM "C:\Users\elite\OneDrive\Documents\School\CIS 4375 Spring 2023\CIS4375-Group3\Backend\group3site\jeans\Data\CustomerPromo.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO
