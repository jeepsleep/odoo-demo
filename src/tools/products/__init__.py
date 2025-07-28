from tools.products.get_product import mcp_get_product
from tools.products.list_products import mcp_list_products


def register_list_products(mcp):
    @mcp.tool("list_products", "Listar productos de Odoo")
    def list_products(page: int = 1, page_size: int = 5):
        return mcp_list_products(page, page_size)

def register_get_product(mcp):
    @mcp.tool("get_product", "Obtener detalle de producto de Odoo por ID")
    def get_product(product_id: int):
        return mcp_get_product(product_id)