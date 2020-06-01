import json

from rest_framework.viewsets import ModelViewSet

from VueAdmin.basic import CassResponse
from VueAdmin.code import CREATED
from rbac.models import Role
from rbac.serializers.role_serializer import RoleListSerializer, RoleModifySerializer
from common.custom import CommonPagination, RbacPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class RoleViewSet(ModelViewSet):
    """
    角色管理：增删改查
    """
    perms_map = ({'*': 'admin'}, {'*': 'role_all'}, {'get': 'role_list'}, {'post': 'role_create'}, {'put': 'role_edit'},
                 {'delete': 'role_delete'})
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleModifySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        environment = data.get("environment", "")
        if environment:
            data['environment'] = json.dumps(environment)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CassResponse(serializer.data, status=CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data
        environment = data.get("environment", None)
        if environment:
            data['environment'] = json.dumps(environment)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return CassResponse(serializer.data, status=CREATED)
