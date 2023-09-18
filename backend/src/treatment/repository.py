from sqlalchemy import select
from src.treatment.models import Treatment
from src.init_database import Session


class TreatmentRepository:
    def __init__(self):
        self.model = Treatment

    def save_new_treatment(self, new_treatment):
        with Session() as session:
            new_treatment = self.model(**new_treatment)
            session.add(new_treatment)
            session.commit()

    def get_all_treatments(self):
        stmt = select(self.model).order_by(self.model.creation_date)
        with Session() as session:
            all_treatments = session.execute(stmt)
            return all_treatments.fetchall()
