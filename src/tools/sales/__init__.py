from tools.sales.get_sale_order import mcp_get_sale_order
from tools.sales.list_sale_orders import mcp_list_sale_orders


def register_list_sale_orders(mcp):
    @mcp.tool("list_sale_orders", "Listar pedidos de venta de Odoo")
    def list_sale_orders(page: int = 1, page_size: int = 5):
        return mcp_list_sale_orders(page, page_size)

def register_get_sale_order(mcp):
    @mcp.tool("get_sale_order", "Obtener detalle de pedido de venta de Odoo por ID")
    def get_sale_order(order_id: int):
        return mcp_get_sale_order(order_id)