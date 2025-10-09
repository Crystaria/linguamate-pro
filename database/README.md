# 数据库设置指南

## Supabase 设置

### 1. 创建 Supabase 项目

1. 访问 [Supabase](https://supabase.com)
2. 创建新项目
3. 记录项目 URL 和 API Key

### 2. 运行数据库架构

1. 在 Supabase Dashboard 中打开 SQL Editor
2. 复制 `schema.sql` 文件内容
3. 执行 SQL 脚本创建表和索引

### 3. 配置环境变量

在 `backend/.env` 文件中设置：

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 4. 数据库表结构

#### learning_records
- 存储用户的学习记录
- 支持文本、图片、对话三种类型
- 包含语言学分析结果

#### exercises
- 存储基于学习记录生成的练习题
- 关联到具体的学习记录

#### chat_records
- 存储与AI的对话记录
- 包含用户消息和AI回复

#### user_stats
- 存储用户学习统计信息
- 跟踪学习进度和等级

### 5. 权限设置

确保在 Supabase 中设置适当的 RLS (Row Level Security) 策略：

```sql
-- 启用 RLS
ALTER TABLE learning_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;

-- 创建策略（示例）
CREATE POLICY "Users can view their own records" ON learning_records
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert their own records" ON learning_records
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);
```
