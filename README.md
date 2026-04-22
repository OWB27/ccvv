# CCVV - AI Resume Analyzer

AI 赋能的智能简历分析系统。项目实现了从 PDF 简历上传、文本解析、结构化信息提取，到 JD 分析与匹配评分的完整主链路。

## 功能说明

- 上传单个 PDF 简历
- 使用 PyMuPDF 提取多页 PDF 文本
- 对简历文本做基础清洗
- 使用 LLM 提取简历结构化信息，失败时规则 fallback
- 提取字段包括姓名、电话、邮箱、地址、求职意向、期望薪资、工作年限、学历背景、工作经历、项目经历
- 输入岗位 JD 并提取关键词、学历要求、经验要求和核心要求
- 优先使用 LLM 计算 JD 与简历匹配分，失败时 fallback 到可解释规则评分
- 对 PDF 解析和简历 + JD 匹配结果做简单 hash 缓存
- 统一错误响应格式
- React + TailwindCSS 前端展示完整分析结果
- GitHub Actions 自动安装依赖、运行后端测试、构建前端

## 技术栈

后端：

- Python 3.12
- FastAPI

前端：

- React
- JavaScript
- TailwindCSS

工程化：

- GitHub Actions
- 简单内存缓存
- 统一错误处理
- 分层目录结构

## 项目结构

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   ├── jobs.py
│   │   │   │   └── resumes.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── error_handlers.py
│   │   ├── schemas/
│   │   │   ├── error.py
│   │   │   ├── match.py
│   │   │   └── resume.py
│   │   ├── services/
│   │   │   ├── ai_client.py
│   │   │   ├── ai_match_scorer.py
│   │   │   ├── ai_resume_extractor.py
│   │   │   ├── hash_utils.py
│   │   │   ├── pdf_text_extractor.py
│   │   │   ├── resume_cache.py
│   │   │   ├── resume_extraction_service.py
│   │   │   ├── resume_match_service.py
│   │   │   ├── resume_text_cleaner.py
│   │   │   ├── rule_jd_extractor.py
│   │   │   ├── rule_match_scorer.py
│   │   │   └── rule_resume_extractor.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_health_api.py
│   │   ├── test_rule_match_scorer.py
│   │   └── test_text_cleaner.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── feedback/
│   │   │   ├── forms/
│   │   │   ├── layout/
│   │   │   ├── results/
│   │   │   └── workspace/
│   │   ├── pages/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── pnpm-lock.yaml
│   └── vite.config.js
├── .github/workflows/ci.yml
├── .env.example
└── README.md
```

## 本地运行

### 1. 后端

Windows PowerShell:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

macOS / Linux:

```bash
cd backend
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

如果 Windows 上 `python.exe` 指向 Microsoft Store 占位入口并报“系统无法访问此文件”，建议关闭系统设置里的 Python App Execution Alias，或安装官方 Python 后重新创建 venv。

### 2. 前端

```bash
cd frontend
pnpm install
pnpm dev
```

默认访问：

```text
http://localhost:5173
```

前端默认请求：

```text
http://localhost:8000
```

如需修改：

```text
VITE_API_BASE_URL=http://localhost:8000
```

## AI 配置

复制 `.env.example` 为 `.env`，填写：

```text
AI_API_KEY=your_api_key_here
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```

也支持使用 `OPENAI_API_KEY`。未配置 key 时，简历提取和匹配评分会使用规则 fallback，系统仍可演示主流程。

## API 说明

### 健康检查

```http
GET /api/health
```

响应：

```json
{
  "status": "ok",
  "service": "CCVV - AI Resume Analyzer API"
}
```

### PDF 文本解析

```http
POST /api/resumes/parse
Content-Type: multipart/form-data
file: resume.pdf
```

响应示例：

```json
{
  "filename": "resume.pdf",
  "resume_hash": "sha256...",
  "page_count": 2,
  "raw_text": "...",
  "cleaned_text_preview": "...",
  "raw_text_length": 4500,
  "cleaned_text_length": 3900,
  "cache_hit": false
}
```

### 简历结构化提取

```http
POST /api/resumes/extract
Content-Type: multipart/form-data
file: resume.pdf
```

响应中的 `data`：

```json
{
  "name": "张三",
  "phone": "13800000000",
  "email": "zhangsan@example.com",
  "address": "上海",
  "job_intention": "Python 后端工程师",
  "expected_salary": "面议",
  "years_of_experience": "3年",
  "education": [],
  "work_experience": [],
  "projects": []
}
```

### JD 分析

```http
POST /api/jobs/analyze
Content-Type: application/json

{
  "jd_text": "负责 Python 后端开发，熟悉 FastAPI、SQL、Docker，本科及以上，3年以上经验。"
}
```

响应：

```json
{
  "jd": {
    "keywords": ["Python", "FastAPI", "SQL", "Docker", "本科", "3年经验"],
    "required_skills": ["Python", "FastAPI", "SQL", "Docker"],
    "required_education": "本科",
    "required_experience_years": 3,
    "core_requirements": []
  }
}
```

### 简历与 JD 匹配

```http
POST /api/resumes/match
Content-Type: multipart/form-data
file: resume.pdf
jd_text: 岗位描述文本
```

响应示例：

```json
{
  "filename": "resume.pdf",
  "resume_hash": "sha256...",
  "jd_hash": "sha256...",
  "page_count": 2,
  "resume": {},
  "jd": {},
  "match": {
    "score": 86,
    "summary": "匹配度高，简历与岗位要求高度一致。",
    "scoring_method": "ai",
    "explanations": ["技能匹配较好。"],
    "matched_keywords": ["Python", "FastAPI"],
    "missing_keywords": ["Docker"],
    "breakdown": {
      "skill_score": 38,
      "education_score": 15,
      "experience_score": 20,
      "project_score": 13
    }
  },
  "cleaned_text_preview": "...",
  "extraction_method": "ai",
  "warnings": [],
  "parse_cache_hit": false,
  "match_cache_hit": false
}
```

`match.scoring_method`：

- `ai`：LLM 评分
- `rule`：规则 fallback 评分

## 缓存机制

缓存采用进程内存实现：

- `resume_hash = sha256(PDF 文件 bytes)`
- `jd_hash = sha256(规范化后的 JD 文本)`
- PDF 解析缓存键：`resume_hash`
- 匹配缓存键：`resume_hash + ":" + jd_hash`

缓存命中字段：

- `cache_hit`
- `parse_cache_hit`
- `match_cache_hit`

该方案简单、可解释；生产环境可替换为 Redis 或对象存储索引。

## 匹配评分逻辑

规则评分总分 100：

- 技能匹配：45 分
- 学历相关性：15 分
- 工作经验相关性：25 分
- 项目经历相关性：15 分

系统优先调用 LLM 进行综合评分。如果 AI key 缺失、请求失败或模型响应异常，则使用规则评分兜底，并在 `warnings` 中返回原因。

## 错误响应格式

统一错误响应：

```json
{
  "code": "BAD_REQUEST",
  "message": "错误说明",
  "details": null
}
```

常见错误：

- 非 PDF：`415 UNSUPPORTED_MEDIA_TYPE`
- 空文件：`400 BAD_REQUEST`
- PDF 无法解析：`422 UNPROCESSABLE_ENTITY`
- 参数校验失败：`422 VALIDATION_ERROR`

## 测试

后端测试：

```bash
cd backend
pytest
```

当前覆盖：

- 文本清洗
- 规则匹配评分
- 健康检查 API

前端构建：

```bash
cd frontend
pnpm build
```

## CI

GitHub Actions 配置位于：

```text
.github/workflows/ci.yml
```

CI 会执行：

- 安装 Python 依赖
- 运行 `pytest`
- 安装前端依赖
- 运行 `pnpm build`

## 部署说明

前端构建产物：

```bash
cd frontend
pnpm build
```

后端部署时需要配置：

- Python 运行环境
- `requirements.txt`
- AI 环境变量
- CORS 允许的前端域名

## 已知限制

- 内存缓存只在单进程内有效，服务重启会丢失。
- 未实现登录、权限和审计。
- PDF 扫描件 OCR 暂不支持。
- LLM 输出质量依赖模型能力和 prompt。
- 规则 fallback 偏保守，复杂简历可能提取不完整。
