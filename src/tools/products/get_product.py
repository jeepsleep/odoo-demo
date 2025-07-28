from models.models_product import ProductOutModel
from tools.odoo_api import OdooAPI


def mcp_get_product(product_id: int) -> ProductOutModel:
    """Obtiene el detalle de un producto de Odoo por ID."""
    api = OdooAPI.from_config()
    product_detail = api.get_single(
        'product.product', 
        product_id, 
        query='{id,name,create_date,default_code,type,categ_id{name},uom_id{name},uom_po_id,list_price,standard_price,description_sale}'
    )

    if isinstance(product_detail.get('uom_po_id'), int):
        product_detail['uom_po_id'] = {'name': f"ID {product_detail['uom_po_id']}"}

    if isinstance(product_detail.get('description_sale'), bool):
        product_detail['description_sale'] = None

    try:
        return ProductOutModel(**product_detail)
    except Exception as e:
        print(f"❌ Error al parsear producto con id={product_id}: {e}")
        raise e
