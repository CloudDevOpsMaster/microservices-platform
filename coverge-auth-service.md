dev@dev-Inspiron-15-3567:~/Repos/microservices-platform$ docker exec auth-service env PYTHONPATH=/app pytest --cov=app --cov-report=term tests/
============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-7.4.4, pluggy-1.6.0
rootdir: /app
plugins: anyio-4.12.0, cov-4.1.0, asyncio-0.23.3
asyncio: mode=Mode.STRICT
collected 13 items

tests/e2e/test_auth_endpoints.py ..                                      [ 15%]
tests/integration/test_login_use_case.py ....                            [ 46%]
tests/integration/test_refresh_token_use_case.py ..                      [ 61%]
tests/integration/test_register_use_case.py ..                           [ 76%]
tests/unit/test_user_entity.py ...                                       [100%]

=============================== warnings summary ===============================
../usr/local/lib/python3.11/site-packages/pydantic/_internal/_config.py:271
  /usr/local/lib/python3.11/site-packages/pydantic/_internal/_config.py:271: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.5/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

app/application/dtos/auth_dto.py:31
  /app/app/application/dtos/auth_dto.py:31: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.5/migration/
    @validator('password')

../usr/local/lib/python3.11/site-packages/passlib/utils/__init__.py:854
  /usr/local/lib/python3.11/site-packages/passlib/utils/__init__.py:854: DeprecationWarning: 'crypt' is deprecated and slated for removal in Python 3.13
    from crypt import crypt as _crypt

tests/e2e/test_auth_endpoints.py::test_health_endpoint
  /usr/local/lib/python3.11/site-packages/pytest_asyncio/plugin.py:749: DeprecationWarning: The event_loop fixture provided by pytest-asyncio has been redefined in
  /app/tests/conftest.py:9
  Replacing the event_loop fixture with a custom implementation is deprecated
  and will lead to errors in the future.
  If you want to request an asyncio event loop with a scope other than function
  scope, use the "scope" argument to the asyncio mark when marking the tests.
  If you want to return different types of event loops, use the event_loop_policy
  fixture.
  
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

---------- coverage: platform linux, python 3.11.14-final-0 ----------
Name                                                  Stmts   Miss  Cover
-------------------------------------------------------------------------
app/application/__init__.py                               0      0   100%
app/application/dtos/__init__.py                          0      0   100%
app/application/dtos/auth_dto.py                         34      3    91%
app/application/use_cases/__init__.py                     0      0   100%
app/application/use_cases/login_use_case.py              48      0   100%
app/application/use_cases/refresh_token_use_case.py      35      6    83%
app/application/use_cases/register_use_case.py           23      0   100%
app/config.py                                            22      0   100%
app/domain/__init__.py                                    0      0   100%
app/domain/entities/__init__.py                           0      0   100%
app/domain/entities/token.py                             22      3    86%
app/domain/entities/user.py                              28      4    86%
app/domain/entities/user_repository.py                   19     19     0%
app/domain/repositories/__init__.py                       0      0   100%
app/domain/repositories/user_repository.py               19      5    74%
app/infrastructure/__init__.py                            0      0   100%
app/infrastructure/cache/__init__.py                      0      0   100%
app/infrastructure/cache/redis_client.py                 33     20    39%
app/infrastructure/database/__init__.py                   0      0   100%
app/infrastructure/database/connection.py                37     23    38%
app/infrastructure/database/models.py                    15      0   100%
app/infrastructure/database/user_repository_impl.py      52     35    33%
app/infrastructure/messaging/__init__.py                  0      0   100%
app/infrastructure/messaging/rabbitmq_publisher.py       38     28    26%
app/main.py                                              37     17    54%
app/presentation/__init__.py                              0      0   100%
app/presentation/dependencies.py                         27      9    67%
app/presentation/middleware/__init__.py                   0      0   100%
app/presentation/middleware/auth_middleware.py           23     23     0%
app/presentation/routes/__init__.py                       0      0   100%
app/presentation/routes/auth_routes.py                   38     19    50%
-------------------------------------------------------------------------
TOTAL                                                   550    214    61%

======================== 13 passed, 4 warnings in 6.11s ========================