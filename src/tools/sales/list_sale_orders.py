from models.models_sale import SaleOrderListOutModel, SaleOrderOutModel
from tools.odoo_api import OdooAPI


def mcp_list_sale_orders(page, page_size) -> SaleOrderListOutModel:
    """Lista los primeros pedidos de venta de Odoo."""
    api = OdooAPI.from_config()
    result = api.get(
        'sale.order', 
        query='{id,name,date_order,state,partner_id{name,email},user_id{name},amount_untaxed,amount_tax,amount_total,order_line{product_id{name},price_unit,product_uom_qty,price_total}}', 
        page=page,
        page_size=page_size
    )

    orders = []
    for o in result.get('result', []):
        if 'order_line' not in o:
            o['order_line'] = []
        orders.append(SaleOrderOutModel(**o))
    return SaleOrderListOutModel(orders=orders) 
