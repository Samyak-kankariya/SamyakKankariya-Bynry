from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError
from models import db, Company, Warehouse, Product, Inventory, Supplier, SupplierProducts, Orders, OrderItems

app = Flask(__name__)

DEFAULT_RECENT_DAYS = 30
DEFAULT_LOW_STOCK_THRESHOLD = 20  # Used if product-specific threshold doesn't exist


@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    """
    Endpoint returns low stock alerts for a given company,
    including only products with recent sales activity,
    considers multiple warehouses, and includes supplier info.
    """
    try:
        # Validate company existence
        company = Company.query.get(company_id)
        if not company:
            return jsonify({"error": "Company not found"}), 404

        # Parse optional query parameter for recent sales lookback days
        try:
            recent_days = int(request.args.get('recent_days', DEFAULT_RECENT_DAYS))
            if recent_days < 0:
                return jsonify({"error": "recent_days must be non-negative"}), 400
        except ValueError:
            return jsonify({"error": "Invalid recent_days value"}), 400

        # Calculate cutoff datetime for recent sales
        recent_cutoff = datetime.utcnow() - timedelta(days=recent_days)

        # Get warehouses belonging to the company
        warehouses = Warehouse.query.filter_by(company_id=company_id).all()
        if not warehouses:
            # No warehouses means no stock, so no alerts
            return jsonify({"alerts": [], "total_alerts": 0})

        warehouse_ids = [w.warehouse_id for w in warehouses]

        # Subquery: products with recent sales in these warehouses over recent_days period with total sold quantity
        recent_sales_subq = (
            db.session.query(
                OrderItems.product_id,
                func.sum(OrderItems.quantity).label('total_sold')
            )
            .join(Orders, OrderItems.order_id == Orders.order_id)
            .filter(
                and_(
                    Orders.warehouse_id.in_(warehouse_ids),
                    Orders.order_date >= recent_cutoff,
                    Orders.status == 'completed'  # Only completed sales count
                )
            )
            .group_by(OrderItems.product_id)
            .subquery()
        )

        # Query inventory entries joined with products, warehouses, suppliers, and recent sales data
        # Filtering inventory qty <= product-specific threshold or default threshold
        query = (
            db.session.query(
                Inventory,
                Product,
                Warehouse,
                Supplier,
                SupplierProducts,
                recent_sales_subq.c.total_sold,
            )
            .join(Product, Inventory.product_id == Product.product_id)
            .join(Warehouse, Inventory.warehouse_id == Warehouse.warehouse_id)
            .join(SupplierProducts, SupplierProducts.product_id == Product.product_id)
            .join(Supplier, Supplier.supplier_id == SupplierProducts.supplier_id)
            .join(recent_sales_subq, recent_sales_subq.c.product_id == Product.product_id)
            .filter(Inventory.warehouse_id.in_(warehouse_ids))
            .filter(
                Inventory.quantity
                <= func.coalesce(Product.low_stock_threshold, DEFAULT_LOW_STOCK_THRESHOLD)
            )
            .order_by(Inventory.quantity.asc())
        )

        alerts = []

        for inventory, product, warehouse, supplier, supplier_product, total_sold in query.all():
            # Defensive: coalesce low_stock_threshold, use default if absent or null
            threshold = getattr(product, 'low_stock_threshold', None)
            if threshold is None:
                threshold = DEFAULT_LOW_STOCK_THRESHOLD

            # Calculate average daily sales over recent_days
            daily_sales = total_sold / recent_days if total_sold and recent_days > 0 else 0

            # Calculate estimated days until stockout; None if no sales
            days_until_stockout = None
            if daily_sales > 0:
                days_until_stockout = int(inventory.quantity / daily_sales)

            alerts.append({
                "product_id": product.product_id,
                "product_name": product.name,
                "sku": product.sku,
                "warehouse_id": warehouse.warehouse_id,
                "warehouse_name": warehouse.name,
                "current_stock": inventory.quantity,
                "threshold": threshold,
                "days_until_stockout": days_until_stockout,
                "supplier": {
                    "id": supplier.supplier_id,
                    "name": supplier.name,
                    "contact_email": supplier.contact_info  # Assumed to be email
                }
            })

        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts)
        }), 200

    except SQLAlchemyError as e:
        # Catch DB errors (connection, query execution, etc.)
        db.session.rollback()  # rollback any pending transaction
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        # Catch-all for unexpected exceptions
        return jsonify({"error": "Internal server error", "details": str(e)}), 500