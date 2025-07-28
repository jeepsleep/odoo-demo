from models.models_product import ProductListOutModel, ProductOutModel
from tools.odoo_api import OdooAPI


def mcp_list_products(page, page_size) -> ProductListOutModel:
    """Lista los primeros productos de Odoo."""
    api = OdooAPI.from_config()
    result = api.get(
        'product.product', 
        query='{id,name,create_date,default_code,type,categ_id{name},uom_id{name},uom_po_id,list_price,standard_price,description_sale}', 
        page=page,
        page_size=page_size
    )

    products = []
    for p in result.get('result', []):
        if isinstance(p.get('uom_po_id'), int):
            p['uom_po_id'] = {'name': f"ID {p['uom_po_id']}"}

        if isinstance(p.get('description_sale'), bool):
            p['description_sale'] = None

        try:
            products.append(ProductOutModel(**p))
        except Exception as e:
            print(f"❌ Error al parsear producto con id={p.get('id')}: {e}")


    return ProductListOutModel(products=products)
