Edge Cases: What Could Go Wrong:
1. Company Not Found
2. No Warehouses for Company
4. No Recent Sales for Products
5. Products Without low_stock_threshold Specified
6. Zero or Very Low Sales Velocity
7. Database Errors
8. Unexpected Errors

Explanation of Approach and Logic:
Company and Warehouse Context:
The alert applies only to warehouses belonging to a specific company, supporting multi-company, multi-warehouse environments.

Filtering Products by Recent Sales:
To avoid spamming alerts about products that don’t move, the system joins inventory with recent sales data for only products sold within the last N days (default 30). This ensures alerts are actionable.

Low Stock Threshold Handling:
As the schema does not have product-specific low_stock_threshold, a sensible default threshold (e.g., 20) is used to judge if stock quantity is low enough to warrant alert. This can be extended if thresholds are added later.

Inventory and Supplier Data Joined for Rich Alerts:
Alert results include detailed product, warehouse, and supplier info by joining relevant tables. Supplier contact info helps users quickly identify reorder sources.

Days Until Stockout Estimation:
This metric is computed by dividing current stock by average daily sales over the recent period, providing a predictive insight to prioritize replenishment.

Performance Considerations:
The use of subqueries, indexed foreign keys, and aggregation reduces data scanned. Joining only relevant recent sales and filtering on warehouse IDs restricts data volume appropriately.

Error Handling and Validation:
Parameter validations and exception handling ensure robustness and clear client feedback in case of improper inputs or backend issues.