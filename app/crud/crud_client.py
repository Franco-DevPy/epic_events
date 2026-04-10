from app.database.session import get_db_session
from app.models.client import Client
from sqlalchemy import select
from app.models.user import EnumRole

# CRUD operations CREATE
def create_client(full_name: str, email: str, phone: str, company_name: str, commercial_id: int):

    session = get_db_session()

    try:
        new_client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            commercial_id=commercial_id
        )
        session.add(new_client)
        session.commit()
        print(f"Client '{full_name}' created successfully.")
        return new_client
    except Exception as e:
        session.rollback()
        print(f"Error creating client: {e}")
        return None
    finally:
        session.close()


# CRUD operations READ
def get_all_clients(current_user):
    session = get_db_session()
    try:
        clients = session.execute(select(Client)).scalars().all()
        if current_user.role == EnumRole.management.value:
            return clients
        elif current_user.role == EnumRole.commercial.value:
            clients = [c for c in clients if c.commercial_id == current_user.id]
        return clients
    except Exception as e:
        print(f"Error retrieving clients: {e}")
        return []
    finally:
        session.close()


def get_client_by_email(email: str):
    session = get_db_session()
    try:
        client = session.execute(select(Client).where(Client.email == email)).scalar_one_or_none()
        print(f"Client with email '{email}' retrieved successfully.")
        return client
    except Exception as e:
        print(f"Error retrieving client: {e}")
    finally:
        session.close()


def get_client_by_id(client_id: int):
    session = get_db_session()
    try:
        client = session.get(Client, client_id)
        print(f"Client with ID '{client_id}' retrieved successfully.")
        return client
    except Exception as e:
        print(f"Error retrieving client: {e}")
    finally:
        session.close()


# CRUD operations UPDATE
def update_client(client_id: int, full_name: str = None, email: str = None, phone: str = None):
    session = get_db_session()
    try:
        client = session.get(Client, client_id)
        if not client:
            print(f"Client with ID {client_id} not found.")
            return None

        if full_name:
            client.full_name = full_name
        if email:
            client.email = email
        if phone:
            client.phone = phone

        session.commit()
        print(f"Client with ID '{client_id}' updated successfully.")
        return client
    except Exception as e:
        session.rollback()
        print(f"Error updating client: {e}")
        return None
    finally:
        session.close()

# CRUD operations DELETE
def delete_client(client_id: int):
    session = get_db_session()
    try:
        client = session.get(Client, client_id)
        if not client:
            print(f"Client with ID {client_id} not found.")
            return False

        session.delete(client)
        session.commit()
        print(f"Client with ID '{client_id}' deleted successfully.")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error deleting client: {e}")
        return False
    

