# from src.dependencies.collaborator_profile import CollaboratorProfileDepends
# from src.exceptions import ForbiddenException
# from src.utils.enums import OrgStructurePermissionsEnum
# from src.utils.get_permissions import get_all_permissions


# def check_list_alert_configurations_permission(
#     collaborator_profile: CollaboratorProfileDepends,
# ) -> None:
#     """
#     Verifica que el colaborador tenga permisos para listar configuraciones de alertas.
#     Args:
#         collaborator_profile: Perfil del colaborador

#     Raises:
#         ForbiddenException: Si no tiene los permisos necesarios
#     """
#     permission_codes = get_all_permissions(collaborator_profile)

#     required_permissions = {
#         OrgStructurePermissionsEnum.LIST_ALERT_CONFIGURATIONS.value,
#     }

#     if not required_permissions.issubset(permission_codes):
#         raise ForbiddenException(
#             "No tiene permisos para listar configuraciones de alertas."
#         )

# def check_create_alert_configuration_permission(
#     collaborator_profile: CollaboratorProfileDepends,
# ) -> None:
#     """
#     Verifica que el colaborador tenga permisos para crear configuraciones de alertas.
#     Args:
#         collaborator_profile: Perfil del colaborador

#     Raises:
#         ForbiddenException: Si no tiene los permisos necesarios
#     """
#     permission_codes = get_all_permissions(collaborator_profile)

#     required_permissions = {
#         OrgStructurePermissionsEnum.CREATE_ALERT_CONFIGURATION.value,
#     }

#     if not required_permissions.issubset(permission_codes):
#         raise ForbiddenException(
#             "No tiene permisos para crear configuraciones de alertas."
#         )


# def check_update_alert_configuration_status_permission(
#     collaborator_profile: CollaboratorProfileDepends,
# ) -> None:
#     """
#     Verifica que el colaborador tenga permisos para actualizar el estado de configuraciones de alertas.
#     Args:
#         collaborator_profile: Perfil del colaborador

#     Raises:
#         ForbiddenException: Si no tiene los permisos necesarios
#     """
#     permission_codes = get_all_permissions(collaborator_profile)

#     required_permissions = {
#         OrgStructurePermissionsEnum.UPDATE_ALERT_CONFIGURATION.value,
#     }

#     if not required_permissions.issubset(permission_codes):
#         raise ForbiddenException(
#             "No tiene permisos para actualizar el estado de configuraciones de alertas."
#         )
