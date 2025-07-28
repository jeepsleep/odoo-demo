from tools.users.get_user import mcp_get_user
from tools.users.list_users import mcp_list_users


def register_list_users(mcp):
    @mcp.tool("list_users", "Listar usuarios de Odoo")
    def list_users(page: int = 1, page_size: int = 5):
        return mcp_list_users(page, page_size)

def register_get_user(mcp):
    @mcp.tool("get_user", "Obtener detalle de usuario de Odoo por ID")
    def get_user(user_id: int):
        return mcp_get_user(user_id)
