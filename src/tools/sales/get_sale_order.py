from models.models_sale import SaleOrderOutModel
from tools.odoo_api import OdooAPI


def mcp_get_sale_order(order_id: int) -> SaleOrderOutModel:
    """Obtiene el detalle de un pedido de venta de Odoo por ID."""
    api = OdooAPI.from_config()

    detail = api.get_single(
        'sale.order', 
        order_id, 
        query='{id,name,date_order,partner_id{name},user_id{name},amount_total,state,order_line{product_id{name},product_uom_qty,price_total,price_unit}}'
    )
    
    for line in detail.get('order_line', []):
        if 'price_unit' not in line:
            line['price_unit'] = None 
    
    try:
        return SaleOrderOutModel(**detail)
    except Exception as e:
        print(f"❌ Error al parsear pedido de venta con id={order_id}: {e}")
        raise e
