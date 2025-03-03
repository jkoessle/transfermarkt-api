import re
import locale
from datetime import datetime
from typing import Optional

from dateutil import parser
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class AuditMixin(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.now)


class TransfermarktBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    @field_validator(
        "date_of_birth",
        "joined_on",
        "contract",
        "founded_on",
        "members_date",
        "from_date",
        "until_date",
        "date",
        "contract_expires",
        "joined",
        "retired_since",
        mode="before",
        check_fields=False,
    )
    def parse_str_to_date(cls, v: str):
        try:
            return parser.parse(v).date() if v else None
        except parser.ParserError:
            return None

    @field_validator(
        "current_market_value",
        "current_transfer_record",
        "market_value",
        "mean_market_value",
        "members",
        "total_market_value",
        "age",
        "goals",
        "assists",
        "yellow_cards",
        "red_cards",
        "minutes_played",
        "fee",
        "appearances",
        "games_missed",
        mode="before",
        check_fields=False,
    )
    def parse_str_to_int(cls, v: str) -> Optional[int]:
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
        if not v or not any(char.isdigit() for char in v):
            return None

        # Remove unwanted characters and normalize the string
        value_str = v.lower().replace("€", "").replace("+", "").replace("'", "").strip()

        # Regular expression to extract the first occurrence of a German-formatted number
        match = re.search(r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b', value_str)
        if match:
            number_str = match.group()
            number_float = locale.atof(number_str)
        else:
            match = re.search(r'\b\d+(\.\d+)?\b', value_str)
            if match:
                number_str = match.group()
                number_float = float(number_str)
            else:
                return None
            
        if "tsd." in value_str:
            return int(float(number_float) * 1_000)
        elif "mio." in value_str:
            return int(float(number_float) * 1_000_000)
        elif "mrd." in value_str:
            return int(float(number_float) * 1_000_000_000)
        elif "bill." in value_str:
            return int(float(number_float) * 1_000_000_000)
        else:
            return int(float(number_float))

    @field_validator("height", mode="before", check_fields=False)
    def parse_height(cls, v: str) -> Optional[int]:
        if not v or not any(char.isdigit() for char in v):
            return None
        return int(v.replace(",", "").replace("m", ""))

    @field_validator("days", mode="before", check_fields=False)
    def parse_days(cls, v: str) -> Optional[int]:
        days = "".join(filter(str.isdigit, v))
        return int(days) if days else None
    
    def parse_german_number(v: str):
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
        if not v or not any(char.isdigit() for char in v):
            return None

        # Remove unwanted characters and normalize the string
        value_str = v.lower().replace("€", "").replace("+", "").replace("'", "").strip()

        # Regular expression to extract the first occurrence of a German-formatted number
        match = re.search(r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b', value_str)
        if match:
            number_str = match.group()
            number_float = locale.atof(number_str)
        else:
            match = re.search(r'\b\d+(\.\d+)?\b', value_str)
            if match:
                number_str = match.group()
                number_float = float(number_str)
            else:
                return None
