from app.database.session import get_db_session
from app.models.event import Event
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime


# CRUD operations CREATE
def create_event(
    client_id: int,
    contract_id: int,
    support_id: int,
    event_start: datetime,
    event_end: datetime,
    location: str,
    attendees: int,
    notes: str = None
):
    session = get_db_session()

    try:
        if event_end <= event_start:
            print(f"Error: event_end ({event_end}) must be after event_start ({event_start})")
            return None
        if attendees < 0:
            print(f"Error: attendees must be a positive number")
            return None
        new_event = Event(
            client_id=client_id,
            contract_id=contract_id,
            support_id=support_id,
            event_start=event_start,
            event_end=event_end,
            location=location,
            attendees=attendees,
            notes=notes
        )
        session.add(new_event)
        session.commit()
        session.refresh(new_event)  
        print(f"Event for contract ID '{contract_id}' created successfully.")
        return new_event
    except Exception as e:
        session.rollback()
        print(f"Error creating event: {e}")
        return None
    finally:
        session.close()


# CRUD operations READ
def get_event_by_id(event_id: int):
    session = get_db_session()
    try:
        stmt = select(Event).where(Event.id == event_id).options(
            selectinload(Event.contract),
            selectinload(Event.client),
            selectinload(Event.support)
        )
        event = session.scalars(stmt).first()
        if event:
            print(f"Event with ID '{event_id}' retrieved successfully.")
        return event
    except Exception as e:
        print(f"Error retrieving event: {e}")
        return None
    finally:
        session.close()


def get_all_events():
    session = get_db_session()
    try:
        stmt = select(Event).options(
            selectinload(Event.contract),
            selectinload(Event.client),
            selectinload(Event.support)
        )
        events = session.scalars(stmt).all()
        print(f"Retrieved {len(events)} event(s) successfully.")
        return events
    except Exception as e:
        print(f"Error retrieving events: {e}")
        return []
    finally:
        session.close()


def get_events_by_contract(contract_id: int):
    session = get_db_session()
    try:
        stmt = select(Event).where(Event.contract_id == contract_id).options(
            selectinload(Event.contract),
            selectinload(Event.client),
            selectinload(Event.support)
        )
        events = session.scalars(stmt).all()
        print(f"Retrieved {len(events)} event(s) for contract ID '{contract_id}'.")
        return events
    except Exception as e:
        print(f"Error retrieving events by contract: {e}")
        return []
    finally:
        session.close()


def get_events_by_support(support_id: int):
    session = get_db_session()
    try:
        stmt = select(Event).where(Event.support_id == support_id).options(
            selectinload(Event.contract),
            selectinload(Event.client),
            selectinload(Event.support)
        )
        events = session.scalars(stmt).all()
        print(f"Retrieved {len(events)} event(s) for support ID '{support_id}'.")
        return events
    except Exception as e:
        print(f"Error retrieving events by support: {e}")
        return []
    finally:
        session.close()


# CRUD operations UPDATE
def update_event(
    event_id: int,
    event_start: datetime = None,
    event_end: datetime = None,
    location: str = None,
    attendees: int = None,
    notes: str = None,
    support_id: int = None
):
    session = get_db_session()
    try:
        event = session.get(Event, event_id)
        if not event:
            print(f"Event with ID '{event_id}' not found.")
            return None

        if event_start is not None:
            event.event_start = event_start
        
        if event_end is not None:
            event.event_end = event_end
        
        if event.event_end <= event.event_start:
            print(f"Error: event_end ({event.event_end}) must be after event_start ({event.event_start})")
            return None
        
        if location is not None:
            event.location = location
        
        if attendees is not None:
            if attendees < 0:
                print(f"Error: attendees must be a positive number")
                return None
            event.attendees = attendees
        
        if notes is not None:
            event.notes = notes
        
        if support_id is not None:
            event.support_id = support_id

        session.commit()
        session.refresh(event)  
        print(f"Event with ID '{event_id}' updated successfully.")
        return event
    except Exception as e:
        session.rollback()
        print(f"Error updating event: {e}")
        return None
    finally:
        session.close()


# CRUD operations DELETE
def delete_event(event_id: int):
    session = get_db_session()
    try:
        event = session.get(Event, event_id)
        if not event:
            print(f"Event with ID '{event_id}' not found.")
            return False

        session.delete(event)
        session.commit()
        print(f"Event with ID '{event_id}' deleted successfully.")
        return True
    except Exception as e:
        session.rollback()
        sentry_sdk.capture_exception(e)
        print(f"Error deleting event: {e}")
        return False
    finally:
        session.close()


