-- LinguaMate AI 数据库架构
-- 适用于 Supabase PostgreSQL

-- 学习记录表
CREATE TABLE learning_records (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    content_type VARCHAR(50) NOT NULL CHECK (content_type IN ('text', 'image', 'chat')),
    content TEXT NOT NULL,
    level VARCHAR(20) NOT NULL CHECK (level IN ('beginner', 'intermediate', 'advanced')),
    analysis TEXT,
    image_data TEXT, -- Base64编码的图片数据
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 练习题表
CREATE TABLE exercises (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    record_id UUID REFERENCES learning_records(id) ON DELETE CASCADE,
    exercises TEXT NOT NULL, -- JSON格式的练习题
    level VARCHAR(20) NOT NULL CHECK (level IN ('beginner', 'intermediate', 'advanced')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 对话记录表
CREATE TABLE chat_records (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    level VARCHAR(20) NOT NULL CHECK (level IN ('beginner', 'intermediate', 'advanced')),
    context TEXT, -- 对话上下文
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 用户学习统计表
CREATE TABLE user_stats (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL UNIQUE,
    total_sessions INTEGER DEFAULT 0,
    total_text_analysis INTEGER DEFAULT 0,
    total_image_analysis INTEGER DEFAULT 0,
    total_chat_sessions INTEGER DEFAULT 0,
    current_level VARCHAR(20) DEFAULT 'beginner' CHECK (current_level IN ('beginner', 'intermediate', 'advanced')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引以提高查询性能
CREATE INDEX idx_learning_records_user_id ON learning_records(user_id);
CREATE INDEX idx_learning_records_created_at ON learning_records(created_at DESC);
CREATE INDEX idx_exercises_record_id ON exercises(record_id);
CREATE INDEX idx_chat_records_user_id ON chat_records(user_id);
CREATE INDEX idx_chat_records_created_at ON chat_records(created_at DESC);

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为需要更新时间的表创建触发器
CREATE TRIGGER update_learning_records_updated_at 
    BEFORE UPDATE ON learning_records 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_stats_updated_at 
    BEFORE UPDATE ON user_stats 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入示例数据
INSERT INTO learning_records (user_id, content_type, content, level, analysis) VALUES
('demo_user', 'text', 'The quick brown fox jumps over the lazy dog.', 'beginner', 
'{"vocabulary": ["quick", "brown", "fox", "jumps", "lazy", "dog"], "grammar": "Simple present tense", "analysis": "This is a pangram containing all letters of the alphabet."}'),
('demo_user', 'text', 'Learning a new language opens doors to new cultures and perspectives.', 'intermediate',
'{"vocabulary": ["learning", "language", "opens", "doors", "cultures", "perspectives"], "grammar": "Gerund as subject", "analysis": "Complex sentence with gerund subject and infinitive complement."}');

INSERT INTO chat_records (user_id, user_message, ai_response, level, context) VALUES
('demo_user', 'Hello, how are you?', 'Hello! I''m doing great, thank you for asking. How are you today?', 'beginner', 'greeting practice'),
('demo_user', 'I would like to order a pizza.', 'Great! What kind of pizza would you like? We have margherita, pepperoni, and vegetarian options.', 'intermediate', 'restaurant ordering');
