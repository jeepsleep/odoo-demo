from models.models_user import UserListOutModel, UserOutModel
from tools.odoo_api import OdooAPI


def mcp_list_users(page, page_size) -> UserListOutModel:
    """Lista los primeros usuarios de Odoo."""
    api = OdooAPI.from_config()
    result = api.get(
        'res.users', 
        query='{id,name,login,email,active}', 
        page=page,
        page_size=page_size
    )

    users = []
    for u in result.get('result', []):
        try:
            users.append(UserOutModel(**u))
        except Exception as e:
            print(f"❌ Error al parsear usuario con id={u.get('id')}: {e}")

    return UserListOutModel(users=users)
