from __future__ import annotations

import math
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field, computed_field


Gender = Literal["male", "female", "other"]


class PatientBase(BaseModel):
    name: Annotated[str, Field(..., min_length=1, description="Full name")]
    age: Annotated[int, Field(..., ge=0, le=120, description="Age in years")]
    gender: Annotated[Gender, Field(..., description="Gender")]
    home_town: Annotated[str, Field(..., min_length=1, description="Home town")]

    # Core measurements (these are the only ones truly needed for calculations below)
    height_m: Annotated[float, Field(..., gt=0, le=2.7, description="Height in meters")]
    weight_kg: Annotated[float, Field(..., gt=0, le=500, description="Weight in kilograms")]


class PatientCreate(PatientBase):
    pass
    


class PatientUpdate(BaseModel):
    # Partial update fields
    name: Optional[str] = Field(default=None, min_length=1)
    age: Optional[int] = Field(default=None, ge=0, le=120)
    gender: Optional[Gender] = None
    home_town: Optional[str] = Field(default=None, min_length=1)

    height_m: Optional[float] = Field(default=None, gt=0, le=2.7)
    weight_kg: Optional[float] = Field(default=None, gt=0, le=500)


class PatientOut(PatientBase):
    id: str

    # ----------------------------
    # CALCULATIONS (computed_field)
    # ----------------------------

    @computed_field
    @property
    def height_cm(self) -> float:
        """Height in centimeters (derived from meters)."""
        return round(self.height_m * 100.0, 1)

    @computed_field
    @property
    def bmi(self) -> float:
        """
        Real BMI formula:
        BMI = weight_kg / (height_m ** 2)
        """
        return round(self.weight_kg / (self.height_m ** 2), 2)

    @computed_field
    @property
    def bmi_category(self) -> str:
        """Standard WHO BMI categories."""
        b = self.bmi
        if b < 18.5:
            return "Underweight"
        if b < 25:
            return "Normal"
        if b < 30:
            return "Overweight"
        return "Obese"

    @computed_field
    @property
    def bmr_kcal_day(self) -> float:
        """
        Basal Metabolic Rate (BMR) using Mifflin–St Jeor equation:
        - Male:   BMR = 10W + 6.25H - 5A + 5
        - Female: BMR = 10W + 6.25H - 5A - 161
        - Other:  Uses midpoint constant (-78) as a practical estimate.
        Where:
          W = weight_kg, H = height_cm, A = age
        """
        h = self.height_cm
        w = self.weight_kg
        a = self.age

        if self.gender == "male":
            s = 5
        elif self.gender == "female":
            s = -161
        else:
            s = -78  # midpoint estimate

        bmr = 10 * w + 6.25 * h - 5 * a + s
        return round(bmr, 0)

    @computed_field
    @property
    def bsa_m2(self) -> float:
        """
        Body Surface Area (BSA) using Mosteller formula:
        BSA (m^2) = sqrt( (height_cm * weight_kg) / 3600 )
        """
        bsa = math.sqrt((self.height_cm * self.weight_kg) / 3600.0)
        return round(bsa, 2)

    @computed_field
    @property
    def ibw_kg_est(self) -> float:
        """
        Ideal Body Weight (IBW) estimate using Devine formula (adult-oriented):
        - Male:   50.0 + 2.3*(inches_over_5ft)
        - Female: 45.5 + 2.3*(inches_over_5ft)
        - Other:  midpoint base (47.75) + 2.3*(inches_over_5ft)

        inches_over_5ft = (height_in_inches - 60)
        """
        inches = self.height_cm / 2.54
        inches_over_5ft = inches - 60.0

        if self.gender == "male":
            base = 50.0
        elif self.gender == "female":
            base = 45.5
        else:
            base = 47.75

        ibw = base + 2.3 * inches_over_5ft
        return round(ibw, 1)
    
    @computed_field
    @property
    def created_at(self) -> str:
        """Creation timestamp in ISO format."""
        # automaticaly create timestamp
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
    
    id: str