# from pydantic import Field
# from typing_extensions import Annotated

# from src.entities import SerializerModel
# from src.utils.enums import AlertEventTypeEnum


# class CreateAlertConfigurationRequest(SerializerModel):
#     event_type: Annotated[AlertEventTypeEnum, Field(alias="eventType")]
#     is_active: Annotated[bool, Field(alias="isActive")] = True
#     days: int


# class UpdateAlertConfigurationStatusRequest(SerializerModel):
#     is_active: Annotated[bool, Field(alias="isActive")]
