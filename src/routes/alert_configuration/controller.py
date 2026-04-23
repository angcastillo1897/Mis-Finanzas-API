# from src.dependencies.async_bd import AsyncSessionDepends
# from src.dependencies.collaborator_profile import CollaboratorProfileDepends
# from src.entities.alert_configuration.repository import (
#     AlertConfigurationRepository,
# )
# from src.entities.alert_configuration.serializer import AlertConfigurationSerializer
# from src.routes.alert_configuration.requests import (
#     CreateAlertConfigurationRequest,
#     UpdateAlertConfigurationStatusRequest,
# )
# from src.routes.alert_configuration.service import Service
# from src.utils.enums import AlertEventTypeEnum
# from src.utils.global_response import GlobalResponse


# class Controller:
#     def __init__(self):
#         self.service = Service()


#     async def get_alert_configurations_by_event_type(
#         self,
#         event_type: AlertEventTypeEnum,
#         async_session: AsyncSessionDepends,
#     ):
#         """
#         Obtiene las configuraciones de alertas activas para un tipo de evento específico (nuevos ingresos o promociones).
#         """

#         alert_configurations = await self.service.get_alert_configurations_by_event_type(
#             event_type.value,
#             AlertConfigurationRepository(async_session),
#         )

#         serialized = [
#             AlertConfigurationSerializer.model_validate(config)
#             for config in alert_configurations
#         ]

#         return dict(data=serialized)

#     async def create_alert_configuration(
#         self,
#         request: CreateAlertConfigurationRequest,
#         async_session: AsyncSessionDepends,
#         collaborator_profile: CollaboratorProfileDepends,
#     ) -> GlobalResponse:
#         """
#         Crea una nueva configuración de alerta.
#         """

#         await self.service.create_alert_configuration(
#             request,
#             collaborator_profile,
#             AlertConfigurationRepository(async_session),
#         )

#         return GlobalResponse(
#             message="Configuración de alerta creada exitosamente.",
#         )

#     async def update_status_by_event_type(
#         self,
#         event_type: AlertEventTypeEnum,
#         payload: UpdateAlertConfigurationStatusRequest,
#         async_session: AsyncSessionDepends,
#         collaborator_profile: CollaboratorProfileDepends,
#     ) -> GlobalResponse:
#         """
#         Actualiza el estado (activo/inactivo) de todas las configuraciones de alertas para un tipo de evento específico.
#         """

#         await self.service.update_status_by_event_type(
#             event_type.value,
#             payload,
#             collaborator_profile,
#             AlertConfigurationRepository(async_session),
#         )

#         return GlobalResponse(
#             message="Estado de configuraciones de alerta actualizados exitosamente."
#         )

#     async def update_alert_configuration_status(
#         self,
#         id: int,
#         request: UpdateAlertConfigurationStatusRequest,
#         async_session: AsyncSessionDepends,
#         collaborator_profile: CollaboratorProfileDepends,
#     ) -> GlobalResponse:
#         """
#         Actualiza el estado (activo/inactivo) de una configuración de alerta.
#         """

#         await self.service.update_alert_configuration_status(
#                 id,
#                 request,
#                 collaborator_profile,
#                 AlertConfigurationRepository(async_session),
#             )

#         return GlobalResponse(
#             message="Estado de configuración de alerta actualizada exitosamente."
#         )
