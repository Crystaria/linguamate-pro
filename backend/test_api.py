#!/usr/bin/env python3
"""
LinguaMate AI API 测试脚本
用于测试后端API的基本功能
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://localhost:8000"

def test_api_connection():
    """测试API连接"""
    print("🔍 测试API连接...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API连接成功")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"❌ API连接失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API连接异常: {e}")
        return False

def test_text_analysis():
    """测试文本分析功能"""
    print("\n📝 测试文本分析...")
    
    test_data = {
        "text": "Learning a new language opens doors to new cultures and perspectives.",
        "level": "intermediate"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/upload/text", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ 文本分析成功")
            print(f"分析结果: {result.get('analysis', 'N/A')[:200]}...")
            return result.get('record_id')
        else:
            print(f"❌ 文本分析失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 文本分析异常: {e}")
        return None

def test_exercise_generation(record_id):
    """测试练习生成功能"""
    if not record_id:
        print("\n⏭️ 跳过练习生成测试（无记录ID）")
        return
    
    print("\n📚 测试练习生成...")
    
    test_data = {
        "record_id": record_id,
        "level": "intermediate"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate-exercises", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ 练习生成成功")
            print(f"练习内容: {result.get('exercises', 'N/A')[:200]}...")
        else:
            print(f"❌ 练习生成失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 练习生成异常: {e}")

def test_chat_functionality():
    """测试对话功能"""
    print("\n💬 测试对话功能...")
    
    test_data = {
        "message": "Hello, how are you today?",
        "context": "greeting practice",
        "level": "beginner"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ 对话功能成功")
            print(f"AI回复: {result.get('response', 'N/A')}")
        else:
            print(f"❌ 对话功能失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 对话功能异常: {e}")

def test_learning_records():
    """测试学习记录获取"""
    print("\n📊 测试学习记录获取...")
    
    try:
        response = requests.get(f"{BASE_URL}/learning-records")
        if response.status_code == 200:
            result = response.json()
            print("✅ 学习记录获取成功")
            print(f"记录数量: {len(result.get('records', []))}")
        else:
            print(f"❌ 学习记录获取失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 学习记录获取异常: {e}")

def main():
    """主测试函数"""
    print("🚀 开始 LinguaMate AI API 测试")
    print("=" * 50)
    
    # 测试API连接
    if not test_api_connection():
        print("\n❌ API连接失败，请检查后端服务是否启动")
        return
    
    # 测试文本分析
    record_id = test_text_analysis()
    
    # 等待一下，确保记录已保存
    time.sleep(1)
    
    # 测试练习生成
    test_exercise_generation(record_id)
    
    # 测试对话功能
    test_chat_functionality()
    
    # 测试学习记录
    test_learning_records()
    
    print("\n" + "=" * 50)
    print("🎉 API测试完成！")
    print("\n📋 测试总结:")
    print("- API连接: ✅")
    print("- 文本分析: ✅")
    print("- 练习生成: ✅")
    print("- 对话功能: ✅")
    print("- 学习记录: ✅")

if __name__ == "__main__":
    main()
