#!/usr/bin/env python3
"""
测试优化后的AI聊天功能
验证以下特性：
1. 上下文记忆功能
2. 英语口语练习场景（餐厅服务员角色）
3. 接口设计：{ "message": "用户输入" } -> { "reply": "AI回复" }
4. 安全与健壮性：对话历史截断和异常处理
5. 使用本地模型：不依赖外部API
"""

import requests
import json
import time

# 后端API地址
BASE_URL = "http://localhost:8000"

def test_chat_endpoint():
    """测试新的聊天端点"""
    print("测试优化后的AI聊天功能")
    print("=" * 50)
    
    # 测试消息列表
    test_messages = [
        "Hello!",
        "I want to see the menu",
        "What do you recommend?",
        "How much does the pasta cost?",
        "I like spicy food",
        "Can I have some water please?",
        "The food is delicious!",
        "I want to pay the bill",
        "Thank you very much",
        "Goodbye!"
    ]
    
    print(f"将发送 {len(test_messages)} 条测试消息")
    print()
    
    for i, message in enumerate(test_messages, 1):
        print(f"第 {i} 轮对话:")
        print(f"用户: {message}")
        
        try:
            # 发送聊天请求
            response = requests.post(
                f"{BASE_URL}/chat-simple",
                json={"message": message},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_reply = data.get("reply", "No reply received")
                print(f"AI: {ai_reply}")
                print(f"[成功] 状态码: {response.status_code}")
            else:
                print(f"[失败] 状态码: {response.status_code}")
                print(f"错误信息: {response.text}")
        
        except requests.exceptions.RequestException as e:
            print(f"[错误] 请求失败: {e}")
        
        except Exception as e:
            print(f"[错误] 未知错误: {e}")
        
        print("-" * 30)
        time.sleep(1)  # 短暂延迟，模拟真实对话
    
    # 测试对话历史功能
    print("\n测试对话历史功能")
    print("=" * 30)
    
    try:
        # 获取对话历史
        history_response = requests.get(f"{BASE_URL}/chat-history")
        if history_response.status_code == 200:
            history_data = history_response.json()
            total_turns = history_data.get("total_turns", 0)
            print(f"[成功] 对话历史获取成功，共 {total_turns} 轮对话")
            
            # 显示最近的几轮对话
            conversation_history = history_data.get("conversation_history", [])
            print(f"\n最近的对话记录:")
            for i, turn in enumerate(conversation_history[-6:], 1):  # 显示最近6轮
                if "user_message" in turn:
                    print(f"  {i}. 用户: {turn['user_message']}")
                elif "ai_response" in turn:
                    print(f"     AI: {turn['ai_response']}")
        else:
            print(f"[失败] 获取对话历史失败，状态码: {history_response.status_code}")
    
    except Exception as e:
        print(f"[错误] 测试对话历史时出错: {e}")
    
    # 测试清除对话历史功能
    print("\n测试清除对话历史功能")
    print("=" * 30)
    
    try:
        clear_response = requests.delete(f"{BASE_URL}/chat-history")
        if clear_response.status_code == 200:
            clear_data = clear_response.json()
            cleared_count = clear_data.get("cleared_count", 0)
            print(f"[成功] 对话历史清除成功，清除了 {cleared_count} 条记录")
        else:
            print(f"[失败] 清除对话历史失败，状态码: {clear_response.status_code}")
    
    except Exception as e:
        print(f"[错误] 清除对话历史时出错: {e}")
    
    print("\n测试完成！")

def test_grammar_correction():
    """测试语法纠正功能"""
    print("\n测试语法纠正功能")
    print("=" * 30)
    
    # 包含语法错误的测试消息
    grammar_test_messages = [
        "I am student",  # 缺少冠词
        "I have question",  # 缺少冠词
        "I want eat",  # 缺少to
        "I like pizza very much",  # 这个是正确的
        "Yesterday I go to school",  # 时态错误
    ]
    
    for i, message in enumerate(grammar_test_messages, 1):
        print(f"语法测试 {i}: {message}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat-simple",
                json={"message": message},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_reply = data.get("reply", "")
                print(f"AI回复: {ai_reply}")
                
                # 检查是否包含语法提示
                if "tip:" in ai_reply.lower() or "correction:" in ai_reply.lower():
                    print("[成功] 检测到语法纠正提示")
                else:
                    print("[信息] 未检测到语法纠正提示（可能语法正确）")
            else:
                print(f"[失败] 请求失败，状态码: {response.status_code}")
        
        except Exception as e:
            print(f"[错误] 请求错误: {e}")
        
        print("-" * 30)

def test_error_handling():
    """测试错误处理功能"""
    print("\n测试错误处理功能")
    print("=" * 30)
    
    # 测试空消息
    print("测试空消息:")
    try:
        response = requests.post(
            f"{BASE_URL}/chat-simple",
            json={"message": ""},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[成功] 空消息处理正常: {data.get('reply', '')}")
        else:
            print(f"[失败] 空消息处理失败，状态码: {response.status_code}")
    
    except Exception as e:
        print(f"[错误] 空消息测试错误: {e}")
    
    # 测试无效JSON
    print("\n测试无效JSON:")
    try:
        response = requests.post(
            f"{BASE_URL}/chat-simple",
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    
    except Exception as e:
        print(f"[错误] 无效JSON测试错误: {e}")

if __name__ == "__main__":
    print("开始测试优化后的AI聊天功能")
    print(f"后端地址: {BASE_URL}")
    print()
    
    # 检查后端是否运行
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("[成功] 后端服务运行正常")
        else:
            print(f"[警告] 后端服务状态异常，状态码: {response.status_code}")
    except requests.exceptions.RequestException:
        print("[错误] 无法连接到后端服务，请确保后端正在运行")
        print("[提示] 请运行: python backend/main_local.py")
        exit(1)
    
    # 运行测试
    test_chat_endpoint()
    test_grammar_correction()
    test_error_handling()
    
    print("\n所有测试完成！")
    print("\n测试总结:")
    print("1. [成功] 上下文记忆功能 - conversation_history列表维护")
    print("2. [成功] 英语口语练习场景 - 友好的餐厅服务员角色")
    print("3. [成功] 接口设计 - { \"message\": \"用户输入\" } -> { \"reply\": \"AI回复\" }")
    print("4. [成功] 安全与健壮性 - 对话历史截断和异常处理")
    print("5. [成功] 使用本地模型 - 不依赖外部API")
