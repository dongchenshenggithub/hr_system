"""HR 系统应用入口。

负责组装各功能模块的路由、挂载静态资源、提供页面入口和健康检查。
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine
from app.features.auth.router import router as auth_router
from app.features.employees.router import router as employees_router

# 根据所有继承了 Base 的模型，在数据库中创建对应的表。
# 表已存在时不会重复创建，也不会修改已有表结构。
# 后续改表结构时，应改用 Alembic 迁移，不再依赖这一行。
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用实例，title 会显示在 /docs 文档顶部。
app = FastAPI(title="HR System")

# 挂载各功能模块的路由。
# 每个模块在自己的 router.py 里定义 APIRouter，
# 这里统一 include，保证 main.py 只做组装，不写业务逻辑。
app.include_router(auth_router)
app.include_router(employees_router)

# 把 app/static 目录挂到 /static 路径下。
# 以后加 CSS、JS、图片等静态资源，直接放 app/static 即可通过 /static/... 访问。
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/health")
def health():
    """健康检查接口，用于确认服务存活。Jenkins 部署后可用它做存活探测。"""
    return {"status": "ok"}


@app.get("/login")
def login_page():
    """返回登录页 HTML。"""
    return FileResponse("app/static/login.html")


@app.get("/employees")
def employees_page():
    """返回员工管理页 HTML。"""
    return FileResponse("app/static/employees.html")
