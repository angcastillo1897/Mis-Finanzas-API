# from fastapi import APIRouter, Depends

# from src.dependencies.auth_token import get_auth_token
# from src.exceptions import docs
# from src.utils.global_response import GlobalResponse

# from .controller import Controller
# from .permissions import (
#     check_create_alert_configuration_permission,
#     check_list_alert_configurations_permission,
#     check_update_alert_configuration_status_permission,
# )
# from .responses import (
#     GetAlertConfigurationsResponse,
# )

# alert_configurations_router: APIRouter = APIRouter(
#     prefix="/alert-configurations",
#     tags=["Alert Configurations"],
#     dependencies=[Depends(get_auth_token)],
#     responses={
#         401: {"model": docs.UnAuthorizedException},
#     },
# )

# controller: Controller = Controller()

# alert_configurations_router.add_api_route(
#     "/{event_type}",
#     controller.get_alert_configurations_by_event_type,
#     methods=["GET"],
#     response_model=GetAlertConfigurationsResponse,
#     dependencies=[Depends(check_list_alert_configurations_permission)],
#     summary="Obtener configuraciones de alertas por tipo de evento",
#     description="Obtiene las configuraciones de alertas activas para un tipo de evento específico (nuevos ingresos o promociones).",
# )

# alert_configurations_router.add_api_route(
#     "",
#     controller.create_alert_configuration,
#     methods=["POST"],
#     response_model=GlobalResponse,
#     dependencies=[Depends(check_create_alert_configuration_permission)],
#     summary="Crear nueva configuración de alerta",
#     description="Crea una nueva configuración de alerta de período de prueba. Permite configurar alertas para nuevos ingresos o promociones con N días de anticipación.",
# )

# alert_configurations_router.add_api_route(
#     "/group/{event_type}/status",
#     controller.update_status_by_event_type,
#     methods=["PATCH"],
#     response_model=GlobalResponse,
#     dependencies=[Depends(check_update_alert_configuration_status_permission)],
#     summary="Actualizar estado de configuraciones de alerta por tipo de evento",
#     description="Actualiza el estado (activo/inactivo) de las configuraciones de alerta para un tipo de evento específico.",
# )

# alert_configurations_router.add_api_route(
#     "/{id}/status",
#     controller.update_alert_configuration_status,
#     methods=["PATCH"],
#     response_model=GlobalResponse,
#     dependencies=[Depends(check_update_alert_configuration_status_permission)],
#     summary="Actualizar estado de configuración de alerta",
#     description="Actualiza el estado (activo/inactivo) de una configuración de alerta existente.",
# )
