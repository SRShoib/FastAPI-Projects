from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status

from app.models import PatientCreate, PatientOut, PatientUpdate
from app.storage import load_db, save_db

router = APIRouter(prefix="/patients", tags=["patients"])

SortField = Literal["height_m", "weight_kg", "bmi", "age", "name", "home_town"]
SortOrder = Literal["asc", "desc"]

_ID_RE = re.compile(r"^patient_(\d{3})$")


def _to_out(patient_id: str, data: Dict) -> PatientOut:
    return PatientOut(id=patient_id, **data)


def next_patient_id(db: Dict) -> str:
    max_n = 0
    for key in db.keys():
        m = _ID_RE.match(key)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return f"patient_{max_n + 1:03d}"


def resequence_ids(db: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Rebuild IDs to be continuous: patient_001, patient_002, ...
    Keeps data the same, only changes the keys.
    Order: by old numeric suffix if possible, otherwise stable insertion order.
    """
    def sort_key(pid: str):
        m = _ID_RE.match(pid)
        return int(m.group(1)) if m else 10**9

    items = list(db.items())
    items.sort(key=lambda kv: sort_key(kv[0]))

    new_db: Dict[str, Dict] = {}
    for i, (_, record) in enumerate(items, start=1):
        new_id = f"patient_{i:03d}"
        # recompute + save computed fields using PatientOut
        record["created_at"] = record.get("created_at") or datetime.now(timezone.utc).isoformat()
        patient_out = PatientOut(id=new_id, **record)
        new_db[new_id] = patient_out.model_dump(exclude={"id"})
    return new_db


@router.get("", response_model=List[PatientOut])
def list_patients(
    sort_by: Optional[SortField] = Query(default=None),
    order: SortOrder = Query(default="asc"),
):
    db = load_db()
    patients = [_to_out(pid, pdata) for pid, pdata in db.items()]
    if sort_by:
        reverse = order == "desc"
        patients.sort(key=lambda p: getattr(p, sort_by), reverse=reverse)
    return patients


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: str = Path(..., pattern=r"^patient_\d{3}$")):
    db = load_db()
    if patient_id not in db:
        raise HTTPException(status_code=404, detail="Patient not found")
    return _to_out(patient_id, db[patient_id])


@router.post("", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate):
    db = load_db()
    new_id = next_patient_id(db)

    record = payload.model_dump()
    record["created_at"] = datetime.now(timezone.utc).isoformat()

    patient_out = PatientOut(id=new_id, **record)
    db[new_id] = patient_out.model_dump(exclude={"id"})
    save_db(db)

    return patient_out


@router.put("/{patient_id}", response_model=PatientOut)
def replace_patient(
    patient_id: str = Path(..., pattern=r"^patient_\d{3}$"),
    payload: PatientCreate = ...,
):
    db = load_db()
    if patient_id not in db:
        raise HTTPException(status_code=404, detail="Patient not found")

    # IMPORTANT: ID never changes (we overwrite the record at the same key)
    record = payload.model_dump()
    record["created_at"] = db[patient_id].get("created_at") or datetime.now(timezone.utc).isoformat()

    patient_out = PatientOut(id=patient_id, **record)
    db[patient_id] = patient_out.model_dump(exclude={"id"})
    save_db(db)

    return patient_out


@router.patch("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: str = Path(..., pattern=r"^patient_\d{3}$"),
    payload: PatientUpdate = ...,
):
    db = load_db()
    if patient_id not in db:
        raise HTTPException(status_code=404, detail="Patient not found")

    # IMPORTANT: ID never changes (same key)
    existing = db[patient_id]
    existing.update(payload.model_dump(exclude_unset=True))
    existing["created_at"] = existing.get("created_at") or datetime.now(timezone.utc).isoformat()

    patient_out = PatientOut(id=patient_id, **existing)
    db[patient_id] = patient_out.model_dump(exclude={"id"})
    save_db(db)

    return patient_out


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: str = Path(..., pattern=r"^patient_\d{3}$")):
    db = load_db()
    if patient_id not in db:
        raise HTTPException(status_code=404, detail="Patient not found")

    # delete requested id
    del db[patient_id]

    # resequence IDs to remove gaps
    db = resequence_ids(db)
    save_db(db)

    return None