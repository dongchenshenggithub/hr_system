#pytest 共享 fixture：测试数据库、依赖覆盖、测试客户端。

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

# 使用 SQLite 内存数据库，测试结束即销毁，不碰本地 hr.db
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    # SQLite 默认不允许跨线程共享连接，FastAPI 测试时会跨线程，必须关闭该检查
    connect_args={"check_same_thread": False},
    # StaticPool 让所有连接共享同一个内存数据库实例
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
#    替代生产环境的 get_db，让应用在测试时使用内存数据库。
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
#    每个测试前建表，测试后删表，保证用例之间互不影响。
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
#    提供 TestClient，并临时把应用的数据库依赖替换成测试数据库。
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # 测试结束后清除覆盖，避免影响其他测试
    app.dependency_overrides.clear()
