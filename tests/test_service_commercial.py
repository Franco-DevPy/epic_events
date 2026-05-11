from unittest.mock import patch
from app.models.client import Client
from app.models.contract import Contract, EnumStatus
from app.services.client_service import create_client_service
from sqlalchemy.orm import sessionmaker


def test_commercial_can_create_client(
        db_session,
        commercial_user,
        commercial_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_client.get_db_session') as mock_crud_session:

        mock_get_session.return_value = db_session
        mock_crud_session.return_value = db_session
        db_session.close = lambda: None

        result = create_client_service(
            full_name="Real Client",
            email="real@test.com",
            phone="123456789",
            company_name="Real Corp",
            token=commercial_token
        )

        assert result is not None, "Service should return a client"

        found = db_session.query(Client).filter_by(
            email="real@test.com").first()
        assert found is not None, "Client should exist in database"
        assert found.full_name == "Real Client"
        assert found.commercial_id == commercial_user.id

        print(f"Client created successfully: {found.full_name}")


def test_commercial_can_see_only_his_clients(
        db_session, commercial_user, commercial_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    from app.models.user import User, EnumRole
    from app.services.auth_service import hash_password

    other_commercial = User(
        full_name="Other Commercial",
        email="other_commercial@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add(other_commercial)
    db_session.commit()
    db_session.refresh(other_commercial)

    his_client = Client(
        full_name="His Client",
        email="his@test.com",
        phone="111",
        company_name="His Corp",
        commercial_id=commercial_user.id
    )
    other_client = Client(
        full_name="Other Client",
        email="other@test.com",
        phone="222",
        company_name="Other Corp",
        commercial_id=other_commercial.id
    )

    db_session.add_all([his_client, other_client])
    db_session.commit()

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_client.get_db_session') as mock_crud_session, \
            patch('app.services.client_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_session.return_value = db_session
        mock_current_user.return_value = commercial_user
        db_session.close = lambda: None

        from app.services.client_service import get_all_clients_service
        result = get_all_clients_service(token=commercial_token)

        assert len(result) == 1, f"Commercial should see only 1 client, saw {
            len(result)}"
        assert result[0].email == "his@test.com"
        assert result[0].commercial_id == commercial_user.id

        print(f"Commercial sees only their client: {result[0].full_name}")


def test_commercial_can_update_his_own_client(
        db_session, commercial_user, commercial_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    his_client = Client(
        full_name="Original Name",
        email="update@test.com",
        phone="111",
        company_name="Original Corp",
        commercial_id=commercial_user.id
    )
    db_session.add(his_client)
    db_session.commit()
    db_session.refresh(his_client)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_client.get_db_session') as mock_crud_session, \
            patch('app.services.client_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_session.return_value = db_session
        mock_current_user.return_value = commercial_user
        db_session.close = lambda: None

        from app.services.client_service import update_client_service
        result = update_client_service(
            client_id=his_client.id,
            full_name="Updated Name",
            email="updated@test.com",
            phone="999",
            token=commercial_token
        )

        assert result is not None, "Commercial should be able to update their client"

        found = db_session.query(Client).filter_by(id=his_client.id).first()
        assert found.full_name == "Updated Name"
        assert found.email == "updated@test.com"
        assert found.phone == "999"

        print(f"Commercial updated their client: {found.full_name}")


def test_commercial_cannot_update_other_client(
        db_session, commercial_user, commercial_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    from app.models.user import User, EnumRole
    from app.services.auth_service import hash_password

    other_commercial = User(
        full_name="Other Commercial",
        email="other_update@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add(other_commercial)
    db_session.commit()
    db_session.refresh(other_commercial)

    other_client = Client(
        full_name="Other Client",
        email="other_client@test.com",
        phone="111",
        company_name="Other Corp",
        commercial_id=other_commercial.id
    )
    db_session.add(other_client)
    db_session.commit()
    db_session.refresh(other_client)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_client.get_db_session') as mock_crud_session, \
            patch('app.services.client_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_session.return_value = db_session
        mock_current_user.return_value = commercial_user
        db_session.close = lambda: None

        from app.services.client_service import update_client_service
        result = update_client_service(
            client_id=other_client.id,
            full_name="Hacked Name",
            email="hacked@test.com",
            phone="999",
            token=commercial_token
        )

        assert result is None, "Commercial should not be able to update another commercial's client"

        found = db_session.query(Client).filter_by(id=other_client.id).first()
        assert found.full_name == "Other Client"
        assert found.email == "other_client@test.com"

        print(f"Permission correctly denied: {found.full_name} was not modified")


def test_commercial_can_create_contract_for_his_client(
        db_session, commercial_user, commercial_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    his_client = Client(
        full_name="Client For Contract",
        email="contract@test.com",
        phone="111",
        company_name="Contract Corp",
        commercial_id=commercial_user.id
    )
    db_session.add(his_client)
    db_session.commit()
    db_session.refresh(his_client)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_client.get_db_session') as mock_crud_client, \
            patch('app.crud.crud_contract.get_db_session') as mock_crud_contract, \
            patch('app.services.contract_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_client.return_value = db_session
        mock_crud_contract.return_value = db_session
        mock_current_user.return_value = commercial_user
        db_session.close = lambda: None

        from app.services.contract_service import create_contract_service
        result = create_contract_service(
            client_id=his_client.id,
            total_amount=10000.0,
            remaining_amount=5000.0,
            status=EnumStatus.signed,
            token=commercial_token
        )

        assert result is not None, "Commercial should be able to create contract for their client"

        found = db_session.query(Contract).filter_by(
            client_id=his_client.id).first()
        assert found is not None, "Contract should exist in database"
        assert found.total_amount == 10000.0
        assert found.remaining_amount == 5000.0
        assert found.commercial_id == commercial_user.id
        assert found.status == EnumStatus.signed

        print(f"Contract created: {found.total_amount}€ for client {his_client.full_name}")


def test_commercial_cannot_create_contract_for_other_client(
        db_session, commercial_user, commercial_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    from app.models.user import User, EnumRole
    from app.services.auth_service import hash_password

    other_commercial = User(
        full_name="Other Commercial",
        email="other_commercial_contract@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add(other_commercial)
    db_session.commit()
    db_session.refresh(other_commercial)

    other_client = Client(
        full_name="Other Client Contract",
        email="other_contract@test.com",
        phone="222",
        company_name="Other Contract Corp",
        commercial_id=other_commercial.id
    )
    db_session.add(other_client)
    db_session.commit()
    db_session.refresh(other_client)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_client.get_db_session') as mock_crud_client, \
            patch('app.crud.crud_contract.get_db_session') as mock_crud_contract, \
            patch('app.services.contract_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_client.return_value = db_session
        mock_crud_contract.return_value = db_session
        mock_current_user.return_value = commercial_user
        db_session.close = lambda: None

        from app.services.contract_service import create_contract_service
        result = create_contract_service(
            client_id=other_client.id,
            total_amount=10000.0,
            remaining_amount=5000.0,
            status=EnumStatus.signed,
            token=commercial_token
        )

        assert result is None, "Commercial should not be able to create contract for another commercial's client"

        found = db_session.query(Contract).filter_by(
            client_id=other_client.id).first()
        assert found is None, "Contract should not exist in database"

        print("Permission correctly denied: contract not created for another commercial's client")


def test_commercial_can_see_only_his_contracts(
        db_session, commercial_user, commercial_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    from app.models.user import User, EnumRole
    from app.services.auth_service import hash_password

    other_commercial = User(
        full_name="Other Commercial",
        email="other_commercial_list@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add(other_commercial)
    db_session.commit()
    db_session.refresh(other_commercial)

    his_client = Client(
        full_name="His Client",
        email="his_client_contract@test.com",
        phone="111",
        company_name="His Corp",
        commercial_id=commercial_user.id
    )
    other_client = Client(
        full_name="Other Client",
        email="other_client_contract@test.com",
        phone="222",
        company_name="Other Corp",
        commercial_id=other_commercial.id
    )
    db_session.add_all([his_client, other_client])
    db_session.commit()
    db_session.refresh(his_client)
    db_session.refresh(other_client)

    his_contract = Contract(
        client_id=his_client.id,
        commercial_id=commercial_user.id,
        total_amount=10000.0,
        remaining_amount=5000.0,
        status=EnumStatus.signed
    )
    other_contract = Contract(
        client_id=other_client.id,
        commercial_id=other_commercial.id,
        total_amount=20000.0,
        remaining_amount=10000.0,
        status=EnumStatus.signed
    )
    db_session.add_all([his_contract, other_contract])
    db_session.commit()

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_contract.get_db_session') as mock_crud_session, \
            patch('app.services.contract_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_session.return_value = db_session
        mock_current_user.return_value = commercial_user
        db_session.close = lambda: None

        from app.services.contract_service import get_all_contracts_service
        result = get_all_contracts_service(token=commercial_token)

        assert len(result) == 1, f"Commercial should see only 1 contract, saw {len(result)}"
        assert result[0].commercial_id == commercial_user.id
        assert result[0].total_amount == 10000.0

        print(f"Commercial sees only their contract: {len(result)} contract(s)")
