# -*- coding: utf-8 -*-
import requests
import json
import os
import datetime
import random
import re
from pathlib import Path

# --- 1. 配置区域 (Configuration Phase) ---
# 系统会自动根据这些关键词去寻找猎物
# 在演化阶段，脚本会自动修改这个列表
CONFIG_FILE = "hermit_config.json"
DATA_DIR = "data"
HISTORY_DIR = "data/history"

# 初始配置（如果没有配置文件）
DEFAULT_CONFIG = {
    "generation": 0,
    "keywords": ["python", "rust", "machine-learning", "api", "automation"],
    "sources": [
        "https://pypi.org/rss/updates.xml",
        # 实际项目中可以添加 HackerNews API, GitHub Trending API 等
    ]
}

# 你的收割机 (Affiliate Links)
# [重要]：后期要把这些换成你的真实链接
ADS = [
    {"text": "🚀 Deploy this bot on DigitalOcean ($200 Credit)", "url": "https://m.do.co/c/EXAMPLE"},
    {"text": "🧠 Master Python Automation (Course)", "url": "https://udemy.com/EXAMPLE"},
    {"text": "🛡️ Secure your data with NordVPN", "url": "https://nordvpn.com/EXAMPLE"}
]

# --- 2. 基础设施 (Infrastructure) ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def ensure_dirs():
    Path(HISTORY_DIR).mkdir(parents=True, exist_ok=True)

# --- 3. 采集引擎 (Ingestion Engine) ---
def fetch_pypi_updates(keywords):
    """
    模拟采集 PyPI 更新。
    在真实环境中，这里会解析 XML，为了代码稳定性，这里做简化模拟。
    """
    print(f"[*] Scouting the wasteland for keywords: {keywords}")
    gems = []
    
    # 模拟网络请求 (真实请求 PyPI RSS)
    try:
        # r = requests.get("https://pypi.org/rss/updates.xml", timeout=10)
        # feed = feedparser.parse(r.content) 
        # 这里为了演示 100% 可运行，我们生成 '模拟数据'，
        # 实际使用时请取消 feedparser 注释并解析真实数据。
        
        for kw in keywords:
            # 模拟发现了一些包
            count = random.randint(1, 3)
            for i in range(count):
                gems.append({
                    "name": f"{kw}-tool-{random.randint(100,999)}",
                    "version": f"1.{random.randint(0,9)}.{random.randint(0,9)}",
                    "desc": f"An advanced auto-evolving library for {kw} development.",
                    "score": round(random.random() * 100, 2),
                    "tag": kw,
                    "timestamp": datetime.datetime.now().isoformat()
                })
    except Exception as e:
        print(f"[!] Error fetching data: {e}")
        
    return sorted(gems, key=lambda x: x['score'], reverse=True)

# --- 4. 演化引擎 (Evolution Engine) ---
def evolve(config, gems):
    """
    根据'采集到的数量'来决定明天的策略。
    如果 'rust' 的包变多了，说明趋势在涨，增加权重。
    """
    print("[*] Evolving DNA...")
    
    # 统计今天的热门标签
    tag_counts = {}
    for gem in gems:
        tag = gem['tag']
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
    # 找出最热的标签
    if tag_counts:
        top_tag = max(tag_counts, key=tag_counts.get)
        print(f"[*] Dominant gene today: {top_tag}")
        
        # 突变：如果某个标签太热，我们尝试加入一个相关的新词 (简单模拟)
        if top_tag == "python" and "django" not in config['keywords']:
            config['keywords'].append("django")
            print("[+] Mutation: Added 'django' to search scope.")
            
    config['generation'] += 1
    save_config(config)

# --- 5. 防御与输出 (Defense & Output) ---
def generate_html(gems, config):
    today = datetime.date.today().isoformat()
    
    # 沙葬陷阱 (Sand Burial): 生成随机 CSS 类名防止爬虫
    def rand_class():
        return "cls-" + "".join(random.choices("abcdef0123456789", k=6))
        
    container_cls = rand_class()
    item_cls = rand_class()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hermit Protocol Daily - {today}</title>
        <meta name="description" content="Automated daily tech trends analysis for {', '.join(config['keywords'])}">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f4f4f9; }}
            .{container_cls} {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .{item_cls} {{ border-bottom: 1px solid #eee; padding: 15px 0; }}
            .ad-box {{ background: #fff3cd; color: #856404; padding: 10px; margin-bottom: 20px; border-radius: 4px; font-size: 0.9em; }}
            h1 {{ color: #333; }}
            .tag {{ background: #e1ecf4; color: #39739d; padding: 2px 5px; border-radius: 4px; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <h1>🏺 Hermit Protocol Report: {today}</h1>
        <p>System Generation: {config['generation']} | Keywords: {', '.join(config['keywords'])}</p>
        
        <!-- 经济系统：流量变现 -->
        <div class="ad-box">
            <strong>💎 Sponsored Opportunity:</strong><br>
            <a href="{ADS[0]['url']}">{ADS[0]['text']}</a>
        </div>

        <div class="{container_cls}">
            {''.join([f'''
            <div class="{item_cls}">
                <h3>{g['name']} <span class="tag">{g['tag']}</span></h3>
                <p>{g['desc']}</p>
                <small>Trend Score: {g['score']} | Version: {g['version']}</small>
            </div>
            ''' for g in gems])}
        </div>
        
        <div style="margin-top: 30px; text-align: center; color: #666;">
            <p>Automated by Hermit Protocol v2.0</p>
            <p><a href="{ADS[1]['url']}">{ADS[1]['text']}</a></p>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding='utf-8') as f:
        f.write(html)
    print("[*] Report generated: index.html")

def solidify_history(gems):
    """时间壁垒：保存历史数据"""
    today = datetime.date.today().isoformat()
    filename = f"{HISTORY_DIR}/{today}.json"
    with open(filename, 'w') as f:
        json.dump(gems, f, indent=2)
    print(f"[*] Time Barrier solidified: {filename}")

# --- 主程序 (Main Loop) ---
if __name__ == "__main__":
    ensure_dirs()
    cfg = load_config()
    
    # 1. 采集
    gems = fetch_pypi_updates(cfg['keywords'])
    
    # 2. 演化
    evolve(cfg, gems)
    
    # 3. 输出
    generate_html(gems, cfg)
    solidify_history(gems)
    
    print("[*] Cycle complete.")