from unittest.mock import patch
from app.models.client import Client
from app.models.contract import Contract, EnumStatus
from app.models.event import Event
from app.models.user import User, EnumRole
from app.services.auth_service import hash_password
from sqlalchemy.orm import sessionmaker
from datetime import datetime


def test_management_can_see_all_clients(
        db_session,
        management_user,
        management_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    commercial1 = User(
        full_name="Commercial 1",
        email="commercial1@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    commercial2 = User(
        full_name="Commercial 2",
        email="commercial2@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add_all([commercial1, commercial2])
    db_session.commit()
    db_session.refresh(commercial1)
    db_session.refresh(commercial2)

    client1 = Client(
        full_name="Client 1",
        email="client1_mgmt@test.com",
        phone="111",
        company_name="Corp 1",
        commercial_id=commercial1.id
    )
    client2 = Client(
        full_name="Client 2",
        email="client2_mgmt@test.com",
        phone="222",
        company_name="Corp 2",
        commercial_id=commercial2.id
    )
    client3 = Client(
        full_name="Client 3",
        email="client3_mgmt@test.com",
        phone="333",
        company_name="Corp 3",
        commercial_id=commercial1.id
    )
    db_session.add_all([client1, client2, client3])
    db_session.commit()

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_client.get_db_session') as mock_crud_client, \
            patch('app.services.client_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_client.return_value = db_session
        mock_current_user.return_value = management_user
        db_session.close = lambda: None

        from app.services.client_service import get_all_clients_service
        result = get_all_clients_service(token=management_token)

        assert len(result) == 3, f"Management should see all clients (3), saw {
            len(result)}"

        emails = {c.email for c in result}
        assert "client1_mgmt@test.com" in emails
        assert "client2_mgmt@test.com" in emails
        assert "client3_mgmt@test.com" in emails

        print(f"Management sees all clients: {len(result)}")


def test_management_can_see_all_events(
        db_session,
        management_user,
        management_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    commercial = User(
        full_name="Commercial User",
        email="commercial_events@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    support1 = User(
        full_name="Support 1",
        email="support1_events@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.support
    )
    support2 = User(
        full_name="Support 2",
        email="support2_events@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.support
    )
    db_session.add_all([commercial, support1, support2])
    db_session.commit()
    db_session.refresh(commercial)
    db_session.refresh(support1)
    db_session.refresh(support2)

    client1 = Client(
        full_name="Client Event 1",
        email="client_event1_mgmt@test.com",
        phone="111",
        company_name="Event Corp 1",
        commercial_id=commercial.id
    )
    client2 = Client(
        full_name="Client Event 2",
        email="client_event2_mgmt@test.com",
        phone="222",
        company_name="Event Corp 2",
        commercial_id=commercial.id
    )
    db_session.add_all([client1, client2])
    db_session.commit()
    db_session.refresh(client1)
    db_session.refresh(client2)

    contract1 = Contract(
        client_id=client1.id,
        commercial_id=commercial.id,
        total_amount=5000.0,
        remaining_amount=0.0,
        status=EnumStatus.signed
    )
    contract2 = Contract(
        client_id=client2.id,
        commercial_id=commercial.id,
        total_amount=3000.0,
        remaining_amount=0.0,
        status=EnumStatus.signed
    )
    db_session.add_all([contract1, contract2])
    db_session.commit()
    db_session.refresh(contract1)
    db_session.refresh(contract2)

    event1 = Event(
        client_id=client1.id,
        contract_id=contract1.id,
        support_id=support1.id,
        event_start=datetime(2026, 6, 1, 10, 0),
        event_end=datetime(2026, 6, 1, 18, 0),
        location="Location 1",
        attendees=50,
        notes="Event 1"
    )
    event2 = Event(
        client_id=client2.id,
        contract_id=contract2.id,
        support_id=support2.id,
        event_start=datetime(2026, 7, 1, 10, 0),
        event_end=datetime(2026, 7, 1, 18, 0),
        location="Location 2",
        attendees=30,
        notes="Event 2"
    )
    db_session.add_all([event1, event2])
    db_session.commit()

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_event.get_db_session') as mock_crud_event, \
            patch('app.services.event_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_event.return_value = db_session
        mock_current_user.return_value = management_user
        db_session.close = lambda: None

        from app.services.event_service import get_all_events_service
        result = get_all_events_service(token=management_token)

        assert len(result) == 2, f"Management should see all events (2), saw {
            len(result)}"

        locations = {e.location for e in result}
        assert "Location 1" in locations
        assert "Location 2" in locations

        print(f"Management sees all events: {len(result)}")


def test_management_can_create_user(
        db_session,
        management_user,
        management_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_user.get_db_session') as mock_crud_user, \
            patch('app.services.user_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_user.return_value = db_session
        mock_current_user.return_value = management_user
        db_session.close = lambda: None

        from app.services.user_service import create_user_service
        result = create_user_service(
            full_name="New Commercial",
            email="new_commercial@test.com",
            password="password123",
            role="commercial",
            token=management_token
        )

        assert result is not None, "Management should be able to create users"

        found = db_session.query(User).filter_by(
            email="new_commercial@test.com").first()
        assert found is not None, "User should exist in database"
        assert found.full_name == "New Commercial"
        assert found.role == EnumRole.commercial

        print(f"Management created user: {found.full_name} ({found.role})")


def test_management_can_update_event_support(
        db_session, management_user, management_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    commercial = User(
        full_name="Commercial User",
        email="commercial_assign@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    support1 = User(
        full_name="Support 1",
        email="support1_assign@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.support
    )
    support2 = User(
        full_name="Support 2",
        email="support2_assign@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.support
    )
    db_session.add_all([commercial, support1, support2])
    db_session.commit()
    db_session.refresh(commercial)
    db_session.refresh(support1)
    db_session.refresh(support2)

    client = Client(
        full_name="Client Assign",
        email="client_assign@test.com",
        phone="111",
        company_name="Assign Corp",
        commercial_id=commercial.id
    )
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)

    contract = Contract(
        client_id=client.id,
        commercial_id=commercial.id,
        total_amount=5000.0,
        remaining_amount=0.0,
        status=EnumStatus.signed
    )
    db_session.add(contract)
    db_session.commit()
    db_session.refresh(contract)

    event = Event(
        client_id=client.id,
        contract_id=contract.id,
        support_id=support1.id,
        event_start=datetime(2026, 6, 1, 10, 0),
        event_end=datetime(2026, 6, 1, 18, 0),
        location="Location Assign",
        attendees=50,
        notes="Original support"
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_event.get_db_session') as mock_crud_event, \
            patch('app.crud.crud_contract.get_db_session') as mock_crud_contract, \
            patch('app.crud.crud_user.get_db_session') as mock_crud_user, \
            patch('app.services.event_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_event.return_value = db_session
        mock_crud_contract.return_value = db_session
        mock_crud_user.return_value = db_session
        mock_current_user.return_value = management_user
        db_session.close = lambda: None

        from app.services.event_service import update_event_service
        result = update_event_service(
            event_id=event.id,
            support_id=support2.id,
            token=management_token
        )

        assert result is not None, "Management should be able to assign support"

        found = db_session.query(Event).filter_by(id=event.id).first()
        assert found.support_id == support2.id, "Support should have changed"

        print(f"Management assigned new support: {support2.full_name}")


def test_management_can_see_events_without_support(
        db_session, management_user, management_token):
    TestSessionLocal = sessionmaker(bind=db_session.bind)

    commercial = User(
        full_name="Commercial User",
        email="commercial_nosupport@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    support = User(
        full_name="Support User",
        email="support_nosupport@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.support
    )
    db_session.add_all([commercial, support])
    db_session.commit()
    db_session.refresh(commercial)
    db_session.refresh(support)

    client1 = Client(
        full_name="Client 1",
        email="client1_nosupport@test.com",
        phone="111",
        company_name="Corp 1",
        commercial_id=commercial.id
    )
    client2 = Client(
        full_name="Client 2",
        email="client2_nosupport@test.com",
        phone="222",
        company_name="Corp 2",
        commercial_id=commercial.id
    )
    db_session.add_all([client1, client2])
    db_session.commit()
    db_session.refresh(client1)
    db_session.refresh(client2)

    contract1 = Contract(
        client_id=client1.id,
        commercial_id=commercial.id,
        total_amount=5000.0,
        remaining_amount=0.0,
        status=EnumStatus.signed
    )
    contract2 = Contract(
        client_id=client2.id,
        commercial_id=commercial.id,
        total_amount=3000.0,
        remaining_amount=0.0,
        status=EnumStatus.signed
    )
    db_session.add_all([contract1, contract2])
    db_session.commit()
    db_session.refresh(contract1)
    db_session.refresh(contract2)

    event_without = Event(
        client_id=client1.id,
        contract_id=contract1.id,
        support_id=None,
        event_start=datetime(2026, 6, 1, 10, 0),
        event_end=datetime(2026, 6, 1, 18, 0),
        location="No Support Location",
        attendees=50,
        notes="No support"
    )
    event_with = Event(
        client_id=client2.id,
        contract_id=contract2.id,
        support_id=support.id,
        event_start=datetime(2026, 7, 1, 10, 0),
        event_end=datetime(2026, 7, 1, 18, 0),
        location="With Support Location",
        attendees=30,
        notes="With support"
    )
    db_session.add_all([event_without, event_with])
    db_session.commit()

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_event.get_db_session') as mock_crud_event, \
            patch('app.services.event_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_event.return_value = db_session
        mock_current_user.return_value = management_user
        db_session.close = lambda: None

        from app.services.event_service import get_events_without_support_service
        result = get_events_without_support_service(token=management_token)

        assert len(result) == 1, f"Should see 1 event without support, saw {
            len(result)}"
        assert result[0].support_id is None
        assert result[0].location == "No Support Location"

        print(f"Management sees events without support: {len(result)}")


def test_management_can_see_all_contracts(
        db_session, management_user, management_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    commercial1 = User(
        full_name="Commercial 1",
        email="commercial1_contracts@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    commercial2 = User(
        full_name="Commercial 2",
        email="commercial2_contracts@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add_all([commercial1, commercial2])
    db_session.commit()
    db_session.refresh(commercial1)
    db_session.refresh(commercial2)

    client1 = Client(
        full_name="Client 1",
        email="client1_contracts@test.com",
        phone="111",
        company_name="Corp 1",
        commercial_id=commercial1.id
    )
    client2 = Client(
        full_name="Client 2",
        email="client2_contracts@test.com",
        phone="222",
        company_name="Corp 2",
        commercial_id=commercial2.id
    )
    db_session.add_all([client1, client2])
    db_session.commit()
    db_session.refresh(client1)
    db_session.refresh(client2)

    contract1 = Contract(
        client_id=client1.id,
        commercial_id=commercial1.id,
        total_amount=10000.0,
        remaining_amount=5000.0,
        status=EnumStatus.signed
    )
    contract2 = Contract(
        client_id=client2.id,
        commercial_id=commercial2.id,
        total_amount=20000.0,
        remaining_amount=10000.0,
        status=EnumStatus.unsigned
    )
    db_session.add_all([contract1, contract2])
    db_session.commit()

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_contract.get_db_session') as mock_crud_session, \
            patch('app.services.contract_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_session.return_value = db_session
        mock_current_user.return_value = management_user
        db_session.close = lambda: None

        from app.services.contract_service import get_all_contracts_service
        result = get_all_contracts_service(token=management_token)

        assert len(result) == 2, f"Management should see all contracts (2), saw {len(result)}"
        
        commercial_ids = {c.commercial_id for c in result}
        assert len(commercial_ids) == 2, "Should have contracts from 2 different commercials"

        print(f"Management sees all contracts: {len(result)} contract(s)")
