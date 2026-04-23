# from src.dependencies.collaborator_profile import CollaboratorProfileDepends
# from src.entities.alert_configuration.model import AlertConfiguration
# from src.entities.alert_configuration.repository import (
#     AlertConfigurationRepository,
# )
# from src.exceptions.bad_request import BadRequestException
# from src.exceptions.not_found import NotFoundException
# from src.routes.alert_configuration.requests import (
#     CreateAlertConfigurationRequest,
#     UpdateAlertConfigurationStatusRequest,
# )
# from src.utils.enums import AlertEventTypeEnum
# from src.utils.global_response import GlobalResponse


# class Service:


#     async def get_alert_configurations_by_event_type(
#         self,
#         event_type: str,
#         alert_configuration_repository: AlertConfigurationRepository,
#     ) -> list[AlertConfiguration]:
#         """
#         Obtiene las configuraciones de alertas activas para un tipo de evento específico (nuevos ingresos o promociones).

#         Args:
#             event_type: Tipo de evento de alerta.
#             alert_configuration_repository: Repositorio de configuraciones de alertas.

#         Returns:
#             Lista de AlertConfiguration encontradas.
#         """

#         # Validar que el tipo de evento sea válido
#         if event_type not in [e.value for e in AlertEventTypeEnum]:
#             raise BadRequestException(
#                 "Tipo de evento no encontrado."
#             )

#         return await alert_configuration_repository.get_active_by_event_type(event_type)

#     async def create_alert_configuration(
#         self,
#         request: CreateAlertConfigurationRequest,
#         collaborator_profile: CollaboratorProfileDepends,
#         alert_configuration_repository: AlertConfigurationRepository,
#     ) -> GlobalResponse:
#         """
#         Crea una nueva configuración de alerta.

#         Args:
#             request: Datos para crear la configuración de alerta.
#             collaborator_profile: Perfil del colaborador que crea la configuración.
#             alert_configuration_repository: Repositorio de configuraciones de alertas.

#         Returns:
#             AlertConfiguration creada.
#         """
#         new_configuration = AlertConfiguration(
#             event_type=request.event_type,
#             is_active=request.is_active,
#             days=request.days,
#             created_by=collaborator_profile.collaborator.id,
#             modified_by=collaborator_profile.collaborator.id,
#         )

#         await alert_configuration_repository.create(new_configuration)

#         await alert_configuration_repository.commit()


#     async def update_status_by_event_type(
#         self,
#         event_type: AlertEventTypeEnum,
#         payload: UpdateAlertConfigurationStatusRequest,
#         collaborator_profile: CollaboratorProfileDepends,
#         alert_configuration_repository: AlertConfigurationRepository,
#     ):
#         """
#         Actualiza el estado (activo/inactivo) de todas las configuraciones de alertas para un tipo de evento específico.

#         Args:
#             payload: Datos para actualizar el estado de las configuraciones de alerta.
#             collaborator_profile: Perfil del colaborador que actualiza las configuraciones.
#             alert_configuration_repository: Repositorio de configuraciones de alertas.

#         Returns:
#             GlobalResponse indicando el resultado de la operación.

#         Raises:
#             BadRequestException: Si el tipo de evento no es válido.
#         """

#         # Validar que el tipo de evento sea válido
#         if event_type not in [e.value for e in AlertEventTypeEnum]:
#             raise BadRequestException(
#                 "El tipo de evento no es válido."
#             )

#         await alert_configuration_repository.update_status_by_event_type(
#             event_type,
#             payload.is_active,
#             collaborator_profile.collaborator.id,
#         )

#         await alert_configuration_repository.commit()


#     async def update_alert_configuration_status(
#         self,
#         alert_configuration_id: int,
#         request: UpdateAlertConfigurationStatusRequest,
#         collaborator_profile: CollaboratorProfileDepends,
#         alert_configuration_repository: AlertConfigurationRepository,
#     ) -> AlertConfiguration:
#         """
#         Actualiza el estado de una configuración de alerta.

#         Args:
#             alert_configuration_id: ID de la configuración de alerta.
#             request: Datos para actualizar la configuración de alerta.
#             collaborator_profile: Perfil del colaborador que actualiza la configuración.
#             alert_configuration_repository: Repositorio de configuraciones de alertas.

#         Returns:
#             AlertConfiguration actualizada.

#         Raises:
#             NotFoundException: Si no se encuentra la configuración de alerta.
#         """
#         configuration = await alert_configuration_repository.get_by_id(alert_configuration_id)

#         if not configuration:
#             raise NotFoundException(
#                 "Configuración de alerta no encontrada."
#             )

#         configuration.is_active = request.is_active
#         configuration.modified_by = collaborator_profile.collaborator.id

#         await alert_configuration_repository.update(configuration)

#         await alert_configuration_repository.commit()
