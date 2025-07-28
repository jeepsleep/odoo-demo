from models.models_user import UserOutModel
from tools.odoo_api import OdooAPI


def mcp_get_user(user_id: int) -> UserOutModel:
    """Obtiene el detalle de un usuario de Odoo por ID."""
    api = OdooAPI.from_config()
    user_detail = api.get_single(
        'res.users', 
        user_id, 
        query='{id,name,login,email,active}'
    )

    try:
        return UserOutModel(**user_detail)
    except Exception as e:
        print(f"❌ Error al parsear usuario con id={user_id}: {e}")
        raise e 
