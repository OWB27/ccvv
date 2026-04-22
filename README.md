# CCVV - AI Resume Analyzer

AI 赋能的智能简历分析系统。当前仓库处于 Stage 4：简历关键信息提取。

## 当前阶段

Stage 1 已完成基础工程结构：

- FastAPI 后端项目骨架
- React + Vite 前端项目骨架
- `/api/health` 健康检查接口
- 基础依赖文件
- 后续测试、CI/CD、部署扩展的目录预留

Stage 2 已完成前端最小壳子：

- PDF 文件选择控件
- JD 文本输入区域
- 提交分析按钮
- 分析结果占位区
- 前端调用后端 `/api/health` 并展示联调状态

Stage 3 已完成 PDF 上传与文本提取：

- 单个 PDF 上传接口
- PDF 文件类型和空文件校验
- 使用 PyMuPDF 提取多页文本
- 基础文本清洗
- 返回原始文本、清洗后文本预览和基础元数据
- 前端最小接入上传解析接口

Stage 4 已完成简历关键信息提取：

- 设计结构化简历输出 schema
- 新增 AI 提取服务
- 支持姓名、电话、邮箱、地址等核心字段
- 补充求职意向、期望薪资、工作年限、学历背景、工作经历、项目经历
- 未配置 AI key 或模型响应异常时提供规则 fallback
- 前端展示结构化结果

## 项目结构

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   └── resumes.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── schemas/
│   │   │   └── resume.py
│   │   ├── services/
│   │   │   ├── pdf_parser.py
│   │   │   ├── resume_extractor.py
│   │   │   └── text_cleaner.py
│   │   └── main.py
│   ├── tests/
│   │   └── .gitkeep
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── health.js
│   │   │   └── resume.js
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 后端接口

健康检查：

```text
GET /api/health
```

PDF 解析：

```text
POST /api/resumes/parse
Content-Type: multipart/form-data
file: PDF 文件
```

响应包含：

- `filename`
- `page_count`
- `raw_text`
- `cleaned_text_preview`
- `raw_text_length`
- `cleaned_text_length`

简历信息提取：

```text
POST /api/resumes/extract
Content-Type: multipart/form-data
file: PDF 文件
```

响应包含：

- `filename`
- `page_count`
- `data`
- `cleaned_text_preview`
- `extraction_method`
- `warnings`

AI 配置：

```text
AI_API_KEY=your_api_key
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```

也兼容使用 `OPENAI_API_KEY` 作为 API key 环境变量。

## 本地启动

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
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

如需修改前端访问的后端地址，可设置：

```text
VITE_API_BASE_URL=http://localhost:8000
```

## 后续阶段建议

Stage 5 适合实现 JD 匹配评分，将结构化简历结果和岗位描述一起输入模型，返回匹配分数、匹配理由和改进建议。
