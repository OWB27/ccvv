# AI Resume Analyzer

AI 赋能的智能简历分析系统。当前仓库处于 Stage 1：项目骨架初始化。

## 当前阶段

Stage 1 只完成基础工程结构：

- FastAPI 后端项目骨架
- React + Vite 前端项目骨架
- `/api/health` 健康检查接口
- 基础依赖文件
- 后续测试、CI/CD、部署扩展的目录预留

## 项目结构

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   └── health.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── schemas/
│   │   │   └── .gitkeep
│   │   ├── services/
│   │   │   └── .gitkeep
│   │   └── main.py
│   ├── tests/
│   │   └── .gitkeep
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
└── README.md
```

## 本地启动

### 后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

健康检查：

```text
GET http://localhost:8000/api/health
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

默认访问：

```text
http://localhost:5173
```

## 后续阶段建议

Stage 2 适合实现单个 PDF 简历上传接口和基础文件校验，但仍不接入 AI。
