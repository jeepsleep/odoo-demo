# Tools de usuario, producto y ventas

from tools.products import register_get_product, register_list_products
from tools.sales import register_get_sale_order, register_list_sale_orders
from tools.users import register_get_user, register_list_users


def register_tools(mcp):
    """Register all MCP tools."""
    register_list_users(mcp)
    register_get_user(mcp)
    register_list_products(mcp)
    register_get_product(mcp)
    register_list_sale_orders(mcp)
    register_get_sale_order(mcp)
