from .base import *

env_name = os.getenv('COMPOSE_PROJECT_NAME')

if env_name == 'prod':
    from .prod import *
elif env_name == 'rel':
    from .rel import *
else:
    from .dev import *