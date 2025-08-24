# SamyakKankariya-Bynry
1. Issue: Lack of Input Validation
Impact:
•	Incorrect types (e.g., string for price) can cause failures or corrupt data.
•	Negative prices or quantities violate business rules and cause logical errors.
Fix:
•	Explicitly validate required fields (sku, name, warehouse_id).
•	Validate optional fields like price and initial_quantity for type and value constraints.
2. Issue: Inventory Created Without Product or Warehouse Existence Validation
Impact:
•	Inventory entries linked to non-existent products or warehouses cause broken references, Leads to database inconsistency.
Fix:
•	The new code verifies the warehouse exists before proceeding and associates inventory only with validated product and warehouse records.
3. Issue: Separate Commits Causing Partial Data Persistence
Impact:
•	Product may get created but inventory insertion fails, leaving orphan product records without inventory, creating inconsistent application state.
Fix:
•	Wrap both product creation (if needed) and inventory creation in a single transaction.
•	Use db.session.flush() to defer commit while getting product ID.
4. Issue: No SKU Uniqueness Check
Impact:
•	Platform-level SKU uniqueness is critical for accurate product identification and tracking.
Fix:
•	The new code queries the database to check if a product with the provided SKU already exists.
•	If so, it does not create a new product but uses the existing one, preventing duplicates.
•	Returns a conflict error (409) if there's a mismatch in product name with the same SKU to prevent inconsistent data.
5. Issue: No Handling of Existing Inventory for Warehouse/Product Combination
Impact:
•	Duplicate inventory entries for the same product and warehouse can be created, inflating stock or causing confusion. Resulting inaccurate stock levels and reporting errors.
Fix:
•	Check inventory entry exists for the product in the specified warehouse before creating.