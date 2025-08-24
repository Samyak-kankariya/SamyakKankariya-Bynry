from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from your_app import app, db
from your_app.models import Product, Inventory, Warehouse

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    
    required_fields = ['sku', 'name', 'warehouse_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    
    sku = data['sku'].strip()
    name = data['name'].strip()
    warehouse_id = data['warehouse_id']
    price = data.get('price', None)
    initial_quantity = data.get('initial_quantity', 0)
    
    if not sku:
        return jsonify({"error": "SKU cannot be empty"}), 400
    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400
    
    try:
        warehouse_id = int(warehouse_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid warehouse_id"}), 400
    
    try:
        if price is not None:
            price = float(price)
            if price < 0:
                return jsonify({"error": "Price must be positive"}), 400
    except ValueError:
        return jsonify({"error": "Price must be a decimal value"}), 400
    
    try:
        initial_quantity = int(initial_quantity)
        if initial_quantity < 0:
            return jsonify({"error": "Initial quantity must be non-negative"}), 400
    except ValueError:
        return jsonify({"error": "Initial quantity must be an integer"}), 400

    warehouse = Warehouse.query.get(warehouse_id)
    if not warehouse:
        return jsonify({"error": "Warehouse not found"}), 400
    try:
        product = Product.query.filter_by(sku=sku).first()
        if product is None:
            product = Product(name=name, sku=sku, price=price)
            db.session.add(product)
            db.session.flush()  # Get product.id without commit
        else:
            if product.name != name:
                return jsonify({"error": "Product SKU already exists with a different name"}), 409
        existing_inventory = Inventory.query.filter_by(
            product_id=product.id,
            warehouse_id=warehouse_id
        ).first()
        if existing_inventory:
            return jsonify({"error": "Inventory for this product in this warehouse already exists"}), 409
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=warehouse_id,
            quantity=initial_quantity
        )
        db.session.add(inventory)
        db.session.commit()
        return jsonify({
            "message": "Product and inventory created or updated successfully",
            "product_id": product.id,
            "inventory_id": inventory.id
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error, possibly duplicate SKU"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500