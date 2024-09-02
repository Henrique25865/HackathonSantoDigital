-- Tabela Calendar
CREATE TABLE Calendar (
    Date DATE PRIMARY KEY
);

-- Tabela Customers
CREATE TABLE Customers (
    CustomerKey INTEGER PRIMARY KEY,
    Prefix TEXT,
    FirstName TEXT,
    LastName TEXT,
    BirthDate DATE,
    MaritalStatus TEXT,
    Gender TEXT,
    EmailAddress TEXT,
    AnnualIncome TEXT,
    TotalChildren INTEGER,
    EducationLevel TEXT,
    Occupation TEXT,
    HomeOwner TEXT
);

-- Tabela Product Categories
CREATE TABLE ProductCategories (
    ProductCategoryKey INTEGER PRIMARY KEY,
    CategoryName TEXT
);

-- Tabela Product Subcategories
CREATE TABLE ProductSubcategories (
    ProductSubcategoryKey INTEGER PRIMARY KEY,
    SubcategoryName TEXT,
    ProductCategoryKey INTEGER,
    FOREIGN KEY (ProductCategoryKey) REFERENCES ProductCategories(ProductCategoryKey)
);

-- Tabela Products
CREATE TABLE Products (
    ProductKey INTEGER PRIMARY KEY,
    ProductSubcategoryKey INTEGER,
    ProductSKU TEXT,
    ProductName TEXT,
    ModelName TEXT,
    ProductDescription TEXT,
    ProductColor TEXT,
    ProductSize TEXT,
    ProductStyle TEXT,
    ProductCost REAL,
    ProductPrice REAL,
    FOREIGN KEY (ProductSubcategoryKey) REFERENCES ProductSubcategories(ProductSubcategoryKey)
);

-- Tabela Returns
CREATE TABLE Returns (
    ReturnDate DATE,
    TerritoryKey INTEGER,
    ProductKey INTEGER,
    ReturnQuantity INTEGER,
    FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey)
);

-- Tabela Sales 2015
CREATE TABLE Sales_2015 (
    OrderDate DATE,
    StockDate DATE,
    OrderNumber TEXT,
    ProductKey INTEGER,
    CustomerKey INTEGER,
    TerritoryKey INTEGER,
    OrderLineItem INTEGER,
    OrderQuantity INTEGER,
    FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES Customers(CustomerKey),
    FOREIGN KEY (TerritoryKey) REFERENCES Territories(SalesTerritoryKey)
);

-- Tabela Sales 2016
CREATE TABLE Sales_2016 (
    OrderDate DATE,
    StockDate DATE,
    OrderNumber TEXT,
    ProductKey INTEGER,
    CustomerKey INTEGER,
    TerritoryKey INTEGER,
    OrderLineItem INTEGER,
    OrderQuantity INTEGER,
    FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES Customers(CustomerKey),
    FOREIGN KEY (TerritoryKey) REFERENCES Territories(SalesTerritoryKey)
);

-- Tabela Sales 2017
CREATE TABLE Sales_2017 (
    OrderDate DATE,
    StockDate DATE,
    OrderNumber TEXT,
    ProductKey INTEGER,
    CustomerKey INTEGER,
    TerritoryKey INTEGER,
    OrderLineItem INTEGER,
    OrderQuantity INTEGER,
    FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES Customers(CustomerKey),
    FOREIGN KEY (TerritoryKey) REFERENCES Territories(SalesTerritoryKey)
);

-- Tabela Territories
CREATE TABLE Territories (
    SalesTerritoryKey INTEGER PRIMARY KEY,
    Region TEXT,
    Country TEXT,
    Continent TEXT
);
