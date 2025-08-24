Questions for the Product Team About Missing Requirements:
Question1: Pricing and Costs
    Should product prices vary by warehouse or remain consistent across all warehouses?
    How should supplier cost prices relate to company sale prices?     
    Are price updates automated or manual?
Question2: Bundles Behavior
    When a bundle is sold, should the inventory of each component product automatically decrease accordingly?
    Can bundles contain other bundles (nested bundles), or only individual products?
Question3: Inventory and Stock Management
    Should the system support minimum stock thresholds, reorder points, or alerts for low stock?
    Are returns, damages, or inventory adjustments tracked differently?
Question4: User and Security
    Should user roles and permissions be defined more granularly (e.g., who can edit prices, adjust inventory)?
    Is there a need for an audit log beyond inventory changes for other entities?
Question5: Order and Transaction Management
    Will the system handle sales orders, purchase orders, and transfers between warehouses?
    Should orders support partial fulfillment or backorders?
Question6: Product Variants and Attributes
    Are product variants (e.g., size, color) required? If so, how should these be represented?
Question7: Integration and External Systems
    Are there integrations with external accounting, ERP, or supplier systems expected?

Explanation and Justification of Design Choices:
1. Indexed foreign keys (product_id, warehouse_id in Inventory) optimize common join and filter queries, improving read performance in typical inventory lookups.
2. Composite unique constraints (product_id, warehouse_id) in Inventory enforce business rules to avoid duplicate stock entries per warehouse-product pair.
3. UNIQUE on SKU enforces platform-wide uniqueness, a critical business requirement to avoid product identification conflicts.
4. CHECK constraints on price and quantity (non-negative) ensure data validity and reduce errors from invalid inputs.
5. Foreign keys with ON DELETE CASCADE maintain referential integrity, automatically cleaning dependent data when parents are deleted.
6. Captures changes for auditability, troubleshooting, and reporting purposes, key for operational transparency.
7. Storing before/after quantities and reasons allows clear traceability of stock movements.
8. Prevents a bundle from including itself via a CHECK constraint, preserving data consistency.