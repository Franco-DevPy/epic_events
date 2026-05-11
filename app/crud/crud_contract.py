from app.database.session import get_db_session
from app.models.contract import Contract, EnumStatus
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# CRUD operations CREATE
def create_contract(
        client_id: int,
        commercial_id: int,
        total_amount: float,
        remaining_amount: float,
        status: EnumStatus):

    session = get_db_session()

    try:
        if remaining_amount > total_amount:
            print(
                f"Error: remaining_amount ({remaining_amount}) cannot be greater than total_amount ({total_amount})")
            return None
        if total_amount < 0 or remaining_amount < 0:
            print(f"Error: amounts must be positive values")
            return None
        new_contract = Contract(
            client_id=client_id,
            commercial_id=commercial_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            status=status
        )
        session.add(new_contract)
        session.commit()
        session.refresh(new_contract)
        print(f"Contract for client ID '{client_id}' created successfully.")
        return new_contract
    except Exception as e:
        session.rollback()
        print(f"Error creating contract: {e}")
        return None
    finally:
        session.close()


# CRUD operations READ
def get_contract_by_id(contract_id: int):
    session = get_db_session()
    try:
        contract = session.get(Contract, contract_id)
        if contract:
            print(f"Contract with ID '{contract_id}' retrieved successfully.")
        return contract
    except Exception as e:
        print(f"Error retrieving contract: {e}")
        return None
    finally:
        session.close()


def get_all_contracts():
    session = get_db_session()
    try:
        stmt = select(Contract).options(selectinload(Contract.client))
        contracts = session.scalars(stmt).all()
        return contracts
    except Exception as e:
        print(f"Error retrieving contracts: {e}")
        return []
    finally:
        session.close()


def get_unsigned_contracts():
    session = get_db_session()
    try:
        stmt = select(Contract).where(
            Contract.status == EnumStatus.unsigned
        ).options(selectinload(Contract.client))
        contracts = session.scalars(stmt).all()
        return contracts
    except Exception as e:
        print(f"Error retrieving unsigned contracts: {e}")
        return []
    finally:
        session.close()


def get_unpaid_contracts():
    session = get_db_session()
    try:
        stmt = select(Contract).where(
            Contract.remaining_amount > 0
        ).options(selectinload(Contract.client))
        contracts = session.scalars(stmt).all()
        return contracts
    except Exception as e:
        print(f"Error retrieving unpaid contracts: {e}")
        return []
    finally:
        session.close()

# CRUD operations UPDATE


def update_contract(
        contract_id: int,
        total_amount: float = None,
        remaining_amount: float = None,
        status: EnumStatus = None):
    session = get_db_session()
    try:
        contract = session.get(Contract, contract_id)
        if not contract:
            print(f"Contract with ID '{contract_id}' not found.")
            return None

        if total_amount is not None:
            if total_amount < 0:
                print(f"Error: total_amount must be positive")
                return None
            contract.total_amount = total_amount

        if remaining_amount is not None:
            if remaining_amount < 0:
                print(f"Error: remaining_amount must be positive")
                return None
            contract.remaining_amount = remaining_amount

        if contract.remaining_amount > contract.total_amount:
            print(
                f"Error: remaining_amount ({
                    contract.remaining_amount}) cannot be greater than total_amount ({
                    contract.total_amount})")
            return None

        if status is not None:
            contract.status = status

        session.commit()
        session.refresh(contract)
        print(f"Contract with ID '{contract_id}' updated successfully.")
        return contract
    except Exception as e:
        session.rollback()
        print(f"Error updating contract: {e}")
        return None
    finally:
        session.close()


# CRUD operations DELETE
def delete_contract(contract_id: int):
    session = get_db_session()
    try:
        contract = session.get(Contract, contract_id)
        if not contract:
            print(f"Contract with ID '{contract_id}' not found.")
            return False

        session.delete(contract)
        session.commit()
        print(f"Contract with ID '{contract_id}' deleted successfully.")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error deleting contract: {e}")
        return False
    finally:
        session.close()
