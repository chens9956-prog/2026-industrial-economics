import os
import json

base_dir = r'l:\我的云端硬盘\2026产业经济学\industrial-economics-wxapp'

dirs = [
    base_dir,
    os.path.join(base_dir, 'pages', 'index'),
    os.path.join(base_dir, 'pages', 'exam'),
    os.path.join(base_dir, 'pages', 'result'),
    os.path.join(base_dir, 'pages', 'admin'),
    os.path.join(base_dir, 'data'),
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# 1. app.json
app_json = {
  "pages": [
    "pages/index/index",
    "pages/exam/exam",
    "pages/result/result",
    "pages/admin/admin"
  ],
  "window": {
    "backgroundTextStyle": "dark",
    "navigationBarBackgroundColor": "#0f172a",
    "navigationBarTitleText": "产业经济学随堂测试",
    "navigationBarTextStyle": "white"
  },
  "style": "v2",
  "sitemapLocation": "sitemap.json"
}

with open(os.path.join(base_dir, 'app.json'), 'w', encoding='utf-8') as f:
    json.dump(app_json, f, ensure_ascii=False, indent=2)

# 2. project.config.json
proj_json = {
  "miniprogramRoot": "./",
  "projectname": "industrial-economics-exam-wxapp",
  "description": "产业经济学50题75分钟微信小程序随堂测试系统",
  "appid": "touristappid",
  "setting": {
    "urlCheck": False,
    "es6": True,
    "postcss": True,
    "minified": True
  },
  "compileType": "miniprogram"
}

with open(os.path.join(base_dir, 'project.config.json'), 'w', encoding='utf-8') as f:
    json.dump(proj_json, f, ensure_ascii=False, indent=2)

# 3. app.js
app_js = """// 微信小程序全局 App 逻辑
App({
  globalData: {
    currentStudent: null,
    userAnswers: {},
    timeElapsed: 0,
    adminPassword: 'admin126'
  }
})
"""
with open(os.path.join(base_dir, 'app.js'), 'w', encoding='utf-8') as f:
    f.write(app_js)

# 4. app.wxss
app_wxss = """/* 全局样式定义 */
page {
  background-color: #020617;
  color: #f8fafc;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  box-sizing: border-box;
}

.container {
  padding: 30rpx;
}

.btn-primary {
  background: linear-gradient(to right, #0284c7, #4f46e5);
  color: #ffffff;
  font-weight: bold;
  border-radius: 20rpx;
  text-align: center;
  padding: 24rpx;
  font-size: 32rpx;
}

.card {
  background-color: #0f172a;
  border: 1rpx solid #1e293b;
  border-radius: 30rpx;
  padding: 40rpx;
  margin-bottom: 30rpx;
}
"""
with open(os.path.join(base_dir, 'app.wxss'), 'w', encoding='utf-8') as f:
    f.write(app_wxss)

print("Created base WeChat Mini Program config successfully!")
