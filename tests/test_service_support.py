from unittest.mock import patch
from app.models.client import Client
from app.models.contract import Contract, EnumStatus
from app.models.event import Event
from app.models.user import User, EnumRole
from app.services.auth_service import hash_password
from sqlalchemy.orm import sessionmaker
from datetime import datetime


def test_support_can_see_only_his_events(
        db_session, support_user, support_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    other_support = User(
        full_name="Other Support",
        email="other_support@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.support
    )
    db_session.add(other_support)
    db_session.commit()
    db_session.refresh(other_support)

    commercial = User(
        full_name="Commercial User",
        email="commercial_event@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add(commercial)
    db_session.commit()
    db_session.refresh(commercial)

    client1 = Client(
        full_name="Client 1",
        email="client1_event@test.com",
        phone="111",
        company_name="Corp 1",
        commercial_id=commercial.id
    )
    client2 = Client(
        full_name="Client 2",
        email="client2_event@test.com",
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

    his_event = Event(
        client_id=client1.id,
        contract_id=contract1.id,
        support_id=support_user.id,
        event_start=datetime(2026, 6, 1, 10, 0),
        event_end=datetime(2026, 6, 1, 18, 0),
        location="His Location",
        attendees=50,
        notes="His event"
    )
    other_event = Event(
        client_id=client2.id,
        contract_id=contract2.id,
        support_id=other_support.id,
        event_start=datetime(2026, 7, 1, 10, 0),
        event_end=datetime(2026, 7, 1, 18, 0),
        location="Other Location",
        attendees=30,
        notes="Other event"
    )
    db_session.add_all([his_event, other_event])
    db_session.commit()

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_event.get_db_session') as mock_crud_event, \
            patch('app.services.event_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_event.return_value = db_session
        mock_current_user.return_value = support_user
        db_session.close = lambda: None

        from app.services.event_service import get_all_events_service
        result = get_all_events_service(token=support_token)

        assert len(result) == 1, f"Support should see only 1 event, saw {
            len(result)}"
        assert result[0].support_id == support_user.id
        assert result[0].location == "His Location"

        print(f"Support sees only their event: {result[0].location}")


def test_support_can_update_his_own_event(
        db_session, support_user, support_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    commercial = User(
        full_name="Commercial User",
        email="commercial_update@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add(commercial)
    db_session.commit()
    db_session.refresh(commercial)

    client = Client(
        full_name="Client Event",
        email="client_event_update@test.com",
        phone="111",
        company_name="Event Corp",
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

    his_event = Event(
        client_id=client.id,
        contract_id=contract.id,
        support_id=support_user.id,
        event_start=datetime(2026, 6, 1, 10, 0),
        event_end=datetime(2026, 6, 1, 18, 0),
        location="Original Location",
        attendees=50,
        notes="Original notes"
    )
    db_session.add(his_event)
    db_session.commit()
    db_session.refresh(his_event)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_event.get_db_session') as mock_crud_event, \
            patch('app.services.event_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_event.return_value = db_session
        mock_current_user.return_value = support_user
        db_session.close = lambda: None

        from app.services.event_service import update_event_service
        result = update_event_service(
            event_id=his_event.id,
            location="Updated Location",
            attendees=100,
            notes="Updated notes",
            token=support_token
        )

        assert result is not None, "Support should be able to update their event"

        found = db_session.query(Event).filter_by(id=his_event.id).first()
        assert found.location == "Updated Location"
        assert found.attendees == 100
        assert found.notes == "Updated notes"

        print(f"Support updated their event: {found.location}")


def test_support_cannot_update_other_event(
        db_session, support_user, support_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    other_support = User(
        full_name="Other Support",
        email="other_support_update@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.support
    )
    db_session.add(other_support)
    db_session.commit()
    db_session.refresh(other_support)

    commercial = User(
        full_name="Commercial User",
        email="commercial_noupdate@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add(commercial)
    db_session.commit()
    db_session.refresh(commercial)

    client = Client(
        full_name="Client Event",
        email="client_event_noupdate@test.com",
        phone="111",
        company_name="Event Corp",
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

    other_event = Event(
        client_id=client.id,
        contract_id=contract.id,
        support_id=other_support.id,
        event_start=datetime(2026, 6, 1, 10, 0),
        event_end=datetime(2026, 6, 1, 18, 0),
        location="Other Location",
        attendees=50,
        notes="Other notes"
    )
    db_session.add(other_event)
    db_session.commit()
    db_session.refresh(other_event)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_event.get_db_session') as mock_crud_event, \
            patch('app.services.event_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_event.return_value = db_session
        mock_current_user.return_value = support_user
        db_session.close = lambda: None

        from app.services.event_service import update_event_service
        result = update_event_service(
            event_id=other_event.id,
            location="Hacked Location",
            attendees=999,
            token=support_token
        )

        assert result is None, "Support should not be able to update another support's event"

        found = db_session.query(Event).filter_by(id=other_event.id).first()
        assert found.location == "Other Location"
        assert found.attendees == 50

        print(f"Permission correctly denied: event was not modified")


def test_support_cannot_create_client(db_session, support_user, support_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_client.get_db_session') as mock_crud_client, \
            patch('app.services.client_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_client.return_value = db_session
        mock_current_user.return_value = support_user
        db_session.close = lambda: None

        from app.services.client_service import create_client_service
        result = create_client_service(
            full_name="Unauthorized Client",
            email="unauthorized@test.com",
            phone="999",
            company_name="Unauthorized Corp",
            token=support_token
        )

        assert result is None, "Support should not be able to create clients"

        found = db_session.query(Client).filter_by(
            email="unauthorized@test.com").first()
        assert found is None, "Client should not exist in database"

        print(f"Permission correctly denied: Support cannot create clients")


def test_support_cannot_create_contract(
        db_session,
        support_user,
        support_token,
        commercial_user):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    client = Client(
        full_name="Test Client",
        email="testcontract@test.com",
        phone="111",
        company_name="Test Corp",
        commercial_id=commercial_user.id
    )
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_client.get_db_session') as mock_crud_client, \
            patch('app.crud.crud_contract.get_db_session') as mock_crud_contract, \
            patch('app.services.contract_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_client.return_value = db_session
        mock_crud_contract.return_value = db_session
        mock_current_user.return_value = support_user
        db_session.close = lambda: None

        from app.services.contract_service import create_contract_service
        result = create_contract_service(
            client_id=client.id,
            total_amount=10000.0,
            remaining_amount=5000.0,
            status=EnumStatus.signed,
            token=support_token
        )

        assert result is None, "Support should not be able to create contracts"

        found = db_session.query(Contract).filter_by(
            client_id=client.id).first()
        assert found is None, "Contract should not exist in database"

        print(f"Permission correctly denied: Support cannot create contracts")


def test_support_cannot_see_contracts(
        db_session, support_user, support_token):

    TestSessionLocal = sessionmaker(bind=db_session.bind)

    commercial = User(
        full_name="Commercial User",
        email="commercial_contracts@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add(commercial)
    db_session.commit()
    db_session.refresh(commercial)

    client = Client(
        full_name="Client Contract",
        email="client_contract@test.com",
        phone="111",
        company_name="Contract Corp",
        commercial_id=commercial.id
    )
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)

    contract = Contract(
        client_id=client.id,
        commercial_id=commercial.id,
        total_amount=10000.0,
        remaining_amount=5000.0,
        status=EnumStatus.signed
    )
    db_session.add(contract)
    db_session.commit()

    with patch('app.database.session.get_db_session') as mock_get_session, \
            patch('app.database.session.SessionLocal', TestSessionLocal), \
            patch('app.crud.crud_contract.get_db_session') as mock_crud_session, \
            patch('app.services.contract_service.get_current_user') as mock_current_user:

        mock_get_session.return_value = db_session
        mock_crud_session.return_value = db_session
        mock_current_user.return_value = support_user
        db_session.close = lambda: None

        from app.services.contract_service import get_all_contracts_service
        result = get_all_contracts_service(token=support_token)

        assert len(result) == 0, "Support should not be able to see contracts"

        print("Permission correctly denied: Support cannot see contracts")
