import graphene


class CustomNode(graphene.Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type_, id):
        return id

    @staticmethod
    def get_node_from_global_id(info, global_id, only_type=None):
        type_, id = global_id.split(':')
        if only_type:
            # We assure that the node type that we want to retrieve
            # is the same that was indicated in the field type
            assert type_ == only_type._meta.name, 'Received not compatible node.'
