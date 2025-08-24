# Backend Intern Case Study – Inventory System (StockFlow)

This repository contains my solution to the backend engineering case study for a fictional B2B inventory platform, "StockFlow". The project simulates key backend tasks such as API debugging, schema modeling, and designing real-world API behavior for inventory tracking.

## Project Scope

The platform allows businesses to manage their products across multiple warehouses, track stock levels, and maintain supplier relationships. The implementation focuses on correctness, maintainability, and assumptions based on incomplete specifications.

## Part 1: API Debugging and Fixes

- Reviewed a non-functional POST endpoint for product creation.
- Fixed issues around missing validation, duplicate SKUs, missing inventory handling, and warehouse linkage.
- Ensured atomic operations using SQLAlchemy’s session management and transaction rollback.

File: `API.py`

## Part 2: Schema Design for Inventory Tracking

- Designed normalized tables to represent:
  - Organizations with multiple warehouses
  - Products stored in various locations with quantities
  - Inventory change logs (for tracking restock/sales)
  - Supplier-product relationships and bundle support
- Highlighted missing business rules and questions for stakeholders (e.g., are prices global or supplier-specific?).

Schema: `SQLSchema.sql`  
Explanation: `README_Part2.md`

## Part 3: Low Stock Alert API

- Developed an endpoint to report low inventory products based on:
  - Recent sales (last 30 days)
  - Product-specific thresholds
  - Warehouse and supplier linkage
- Accounted for edge cases such as missing inventory, absent suppliers, and inactive products.

Code: `ApiImplementation.py`

## Assumptions & Clarifications

- “Recent” activity = last 30 days (adjustable)
- Threshold values are stored per product
- Products are not company-specific in current scope
- Supplier info is simplified to first linked supplier per product

## Tech Used

- Python (3.x)
- Flask + SQLAlchemy (ORM)

## Additional Notes

- `README_Part1.md`: Detailed problem breakdown for Part 1  
- `README_Part2.md`: Schema rationale and questions for product team  
- `README_Part3.md`: API logic, assumptions, and corner-case handling
