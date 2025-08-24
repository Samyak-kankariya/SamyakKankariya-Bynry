CREATE TABLE Companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Warehouses (
    warehouse_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id) ON DELETE CASCADE
);


CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    sku VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(12, 2) NOT NULL CHECK (price >= 0),
    is_bundle BOOLEAN DEFAULT FALSE
);

CREATE TABLE ProductBundles (
    bundle_id INT NOT NULL,
    component_product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (bundle_id, component_product_id),
    FOREIGN KEY (bundle_id) REFERENCES Products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (component_product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
    CHECK (bundle_id <> component_product_id)
);

CREATE TABLE Inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    UNIQUE (product_id, warehouse_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id) ON DELETE CASCADE
);

CREATE TABLE InventoryHistory (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    inventory_id INT NOT NULL,
    quantity_before INT NOT NULL,
    quantity_after INT NOT NULL,
    reason VARCHAR(100),
    changed_by_user_id INT,
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id) ON DELETE CASCADE
);

CREATE TABLE Suppliers (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    contact_info TEXT,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id) ON DELETE CASCADE
);

CREATE TABLE SupplierProducts (
    supplier_id INT NOT NULL,
    product_id INT NOT NULL,
    supplier_sku VARCHAR(100),
    cost_price DECIMAL(12, 2) CHECK (cost_price >= 0),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
    UNIQUE (supplier_id, product_id)
);

CREATE INDEX idx_inventory_product_warehouse ON Inventory(product_id, warehouse_id);
CREATE INDEX idx_inventoryhistory_inventory ON InventoryHistory(inventory_id);
CREATE INDEX idx_supplierproducts_supplier_product ON SupplierProducts(supplier_id, product_id);