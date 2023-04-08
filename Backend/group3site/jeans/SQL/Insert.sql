BULK INSERT Country
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\Country.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT CustomerStatus
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\CustomerStatus.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductStatus
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\ProductStatus.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT PromoStatus
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\PromoStatus.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductTag
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\ProductTag.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT Brand
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\Brand.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT StateProvince
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\StateProvince.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT Product
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\Product.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT Promo
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\Promo.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductProductTag
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\ProductProductTag.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductImage
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\ProductImage.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT ProductPromo
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\ProductPromo.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT Customer
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\Customer.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT CustomerPromo
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\CustomerPromo.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

BULK INSERT CustomerProductPromo
FROM "F:\School\CIS4375-Group3\Backend\group3site\jeans\Data\CustomerProductPromo.tsv"
WITH
	(
	CHECK_CONSTRAINTS,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n',
	KEEPIDENTITY
	)
GO

