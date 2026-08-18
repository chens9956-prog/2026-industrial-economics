import os
import json

base_dir = r'l:\我的云端硬盘\2026产业经济学\glass-calculator-wxapp'

dirs = [
    base_dir,
    os.path.join(base_dir, 'pages', 'index'),
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# 1. app.json
app_json = {
  "pages": [
    "pages/index/index"
  ],
  "window": {
    "backgroundTextStyle": "dark",
    "navigationBarBackgroundColor": "#0f172a",
    "navigationBarTitleText": "高颜值科学计算器",
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
  "projectname": "glass-calculator-wxapp",
  "description": "高颜值极简科学计算器微信小程序版",
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
app_js = """App({
  globalData: {}
})
"""
with open(os.path.join(base_dir, 'app.js'), 'w', encoding='utf-8') as f:
    f.write(app_js)

# 4. app.wxss
app_wxss = """page {
  background-color: #090d16;
  color: #f8fafc;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  box-sizing: border-box;
}

.container {
  padding: 24rpx;
  min-height: 100vh;
  box-sizing: border-box;
}
"""
with open(os.path.join(base_dir, 'app.wxss'), 'w', encoding='utf-8') as f:
    f.write(app_wxss)

# 5. pages/index/index.wxml
index_wxml = """<view class="container {{themeMode}}">
  <view class="calc-card">
    <!-- Header -->
    <view class="calc-header">
      <view class="title-box">
        <text class="icon">🧮</text>
        <text class="title">科学电子计算器</text>
      </view>
      <view class="actions">
        <button class="btn-sm" bindtap="onToggleHistory">📜 历史 ({{historyList.length}})</button>
        <button class="btn-sm" bindtap="onToggleTheme">🌓 {{themeMode === 'dark' ? '深色' : '浅色'}}</button>
      </view>
    </view>

    <!-- Display Screen -->
    <view class="calc-display">
      <scroll-view scroll-x class="expr-scroll">
        <text class="expression">{{expression || '0'}}</text>
      </scroll-view>
      <text class="result">= {{result}}</text>
    </view>

    <!-- Scientific Function Keys Mode Switcher -->
    <view class="mode-tabs">
      <text class="tab-item {{isSciMode ? 'active' : ''}}" bindtap="onToggleSciMode">科学计算模式</text>
      <text class="tab-item {{!isSciMode ? 'active' : ''}}" bindtap="onToggleSciMode">基础计算模式</text>
    </view>

    <!-- Scientific Buttons Grid -->
    <view class="keypad-sci" wx:if="{{isSciMode}}">
      <button class="btn-key sci" bindtap="onTapKey" data-val="sin(">sin</button>
      <button class="btn-key sci" bindtap="onTapKey" data-val="cos(">cos</button>
      <button class="btn-key sci" bindtap="onTapKey" data-val="tan(">tan</button>
      <button class="btn-key sci" bindtap="onTapKey" data-val="ln(">ln</button>
      <button class="btn-key sci" bindtap="onTapKey" data-val="log(">log</button>

      <button class="btn-key sci" bindtap="onTapKey" data-val="√(">√</button>
      <button class="btn-key sci" bindtap="onTapKey" data-val="^">x^y</button>
      <button class="btn-key sci" bindtap="onTapKey" data-val="π">π</button>
      <button class="btn-key sci" bindtap="onTapKey" data-val="e">e</button>
      <button class="btn-key sci" bindtap="onTapKey" data-val="%">%</button>
    </view>

    <!-- Main Keypad Grid -->
    <view class="keypad-main">
      <button class="btn-key func-clear" bindtap="onClear">AC</button>
      <button class="btn-key func" bindtap="onDelete">DEL</button>
      <button class="btn-key func" bindtap="onTapKey" data-val="(">(</button>
      <button class="btn-key func" bindtap="onTapKey" data-val=")">)</button>
      <button class="btn-key op" bindtap="onTapKey" data-val="÷">÷</button>

      <button class="btn-key num" bindtap="onTapKey" data-val="7">7</button>
      <button class="btn-key num" bindtap="onTapKey" data-val="8">8</button>
      <button class="btn-key num" bindtap="onTapKey" data-val="9">9</button>
      <button class="btn-key op" bindtap="onTapKey" data-val="×">×</button>
      <button class="btn-key op" bindtap="onTapKey" data-val="-">-</button>

      <button class="btn-key num" bindtap="onTapKey" data-val="4">4</button>
      <button class="btn-key num" bindtap="onTapKey" data-val="5">5</button>
      <button class="btn-key num" bindtap="onTapKey" data-val="6">6</button>
      <button class="btn-key op" bindtap="onTapKey" data-val="+">+</button>
      <button class="btn-key equal" bindtap="onCalculate">=</button>

      <button class="btn-key num" bindtap="onTapKey" data-val="1">1</button>
      <button class="btn-key num" bindtap="onTapKey" data-val="2">2</button>
      <button class="btn-key num" bindtap="onTapKey" data-val="3">3</button>
      <button class="btn-key num span-2" bindtap="onTapKey" data-val="0">0</button>
      <button class="btn-key num" bindtap="onTapKey" data-val=".">.</button>
    </view>
  </view>

  <!-- History Drawer Panel -->
  <view class="history-panel" wx:if="{{showHistory}}">
    <view class="panel-header">
      <text class="panel-title">📜 计算历史记录</text>
      <view class="panel-btns">
        <text class="btn-text-danger" bindtap="onClearHistory">清空历史</text>
        <text class="btn-text-close" bindtap="onToggleHistory">关闭</text>
      </view>
    </view>

    <scroll-view scroll-y class="history-list">
      <block wx:for="{{historyList}}" wx:key="index">
        <view class="history-item" bindtap="onSelectHistory" data-item="{{item}}">
          <text class="h-expr">{{item.expr}}</text>
          <text class="h-res">= {{item.res}}</text>
        </view>
      </block>
      <view class="empty-tip" wx:if="{{historyList.length === 0}}">
        <text>暂无历史计算记录</text>
      </view>
    </scroll-view>
  </view>
</view>
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.wxml'), 'w', encoding='utf-8') as f:
    f.write(index_wxml)

# 6. pages/index/index.js
index_js = """Page({
  data: {
    expression: '',
    result: '0',
    isSciMode: true,
    showHistory: false,
    historyList: [],
    themeMode: 'dark'
  },

  onLoad() {
    const historyList = wx.getStorageSync('calc_history_v1') || [];
    const themeMode = wx.getStorageSync('calc_theme_v1') || 'dark';
    this.setData({ historyList, themeMode });
  },

  onToggleTheme() {
    const themeMode = this.data.themeMode === 'dark' ? 'light' : 'dark';
    wx.setStorageSync('calc_theme_v1', themeMode);
    this.setData({ themeMode });
  },

  onToggleSciMode() {
    this.setData({ isSciMode: !this.data.isSciMode });
  },

  onToggleHistory() {
    this.setData({ showHistory: !this.data.showHistory });
  },

  onClearHistory() {
    wx.removeStorageSync('calc_history_v1');
    this.setData({ historyList: [] });
  },

  onSelectHistory(e) {
    const { item } = e.currentTarget.dataset;
    this.setData({
      expression: item.expr,
      result: item.res,
      showHistory: false
    });
  },

  onTapKey(e) {
    const val = e.currentTarget.dataset.val;
    let expr = this.data.expression;
    expr += val;
    this.setData({ expression: expr });
    this.autoEvaluate(expr);
  },

  onClear() {
    this.setData({
      expression: '',
      result: '0'
    });
  },

  onDelete() {
    let expr = this.data.expression;
    if (expr.length > 0) {
      expr = expr.slice(0, -1);
      this.setData({ expression: expr });
      this.autoEvaluate(expr);
    }
  },

  autoEvaluate(expr) {
    if (!expr) {
      this.setData({ result: '0' });
      return;
    }
    try {
      let res = this.evalExpression(expr);
      if (res !== null && !isNaN(res) && isFinite(res)) {
        this.setData({ result: String(res) });
      }
    } catch (e) {}
  },

  onCalculate() {
    const expr = this.data.expression;
    if (!expr) return;
    try {
      let res = this.evalExpression(expr);
      if (res !== null && !isNaN(res) && isFinite(res)) {
        const resStr = String(parseFloat(res.toFixed(8)));
        this.setData({ result: resStr });

        // Push to history
        let historyList = this.data.historyList;
        historyList.unshift({ expr, res: resStr });
        if (historyList.length > 50) historyList = historyList.slice(0, 50);
        wx.setStorageSync('calc_history_v1', historyList);
        this.setData({ historyList });
      } else {
        this.setData({ result: '错误' });
      }
    } catch (e) {
      this.setData({ result: '语法错误' });
    }
  },

  evalExpression(expr) {
    let sanitized = expr
      .replace(/×/g, '*')
      .replace(/÷/g, '/')
      .replace(/π/g, 'Math.PI')
      .replace(/e/g, 'Math.E')
      .replace(/sin\(/g, 'Math.sin(')
      .replace(/cos\(/g, 'Math.cos(')
      .replace(/tan\(/g, 'Math.tan(')
      .replace(/ln\(/g, 'Math.log(')
      .replace(/log\(/g, 'Math.log10(')
      .replace(/√\(/g, 'Math.sqrt(')
      .replace(/\^/g, '**');

    // Handle % as /100
    sanitized = sanitized.replace(/(\d+(\.\d+)?)%/g, '($1/100)');

    try {
      const fn = new Function('return ' + sanitized);
      return fn();
    } catch (err) {
      return null;
    }
  }
})
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.js'), 'w', encoding='utf-8') as f:
    f.write(index_js)

# 7. pages/index/index.wxss
index_wxss = """.calc-card {
  background: rgba(15, 23, 42, 0.95);
  border: 1rpx solid #1e293b;
  border-radius: 36rpx;
  padding: 30rpx;
  box-shadow: 0 20rpx 50rpx rgba(0,0,0,0.5);
}

.theme-light .calc-card {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 20rpx 50rpx rgba(0,0,0,0.1);
}

.calc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.title-box { display: flex; align-items: center; gap: 10rpx; }
.title { font-size: 28rpx; font-weight: bold; color: #ffffff; }
.theme-light .title { color: #0f172a !important; }

.actions { display: flex; gap: 12rpx; }
.btn-sm {
  background: #1e293b;
  color: #38bdf8;
  font-size: 20rpx;
  font-weight: bold;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  margin: 0;
}
.theme-light .btn-sm { background: #e2e8f0; color: #0284c7; }

.calc-display {
  background: #020617;
  border: 1rpx solid #1e293b;
  border-radius: 24rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
  text-align: right;
}
.theme-light .calc-display {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
}

.expr-scroll {
  white-space: nowrap;
  width: 100%;
}
.expression {
  font-size: 32rpx;
  color: #94a3b8;
  font-family: monospace;
}
.theme-light .expression { color: #64748b !important; }

.result {
  display: block;
  font-size: 56rpx;
  font-weight: bold;
  color: #38bdf8;
  font-family: monospace;
  margin-top: 10rpx;
}

.mode-tabs {
  display: flex;
  gap: 20rpx;
  margin-bottom: 20rpx;
}
.tab-item {
  font-size: 22rpx;
  color: #64748b;
  font-weight: bold;
}
.tab-item.active {
  color: #38bdf8;
  border-bottom: 3rpx solid #38bdf8;
}

.keypad-sci, .keypad-main {
  display: grid;
  gap: 14rpx;
}
.keypad-sci {
  grid-template-columns: repeat(5, 1fr);
  margin-bottom: 16rpx;
}
.keypad-main {
  grid-template-columns: repeat(5, 1fr);
}

.btn-key {
  height: 96rpx;
  border-radius: 20rpx;
  font-size: 30rpx;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
}

.num {
  background: #1e293b;
  color: #f8fafc;
}
.theme-light .num {
  background: #f1f5f9 !important;
  color: #0f172a !important;
  border: 1rpx solid #cbd5e1;
}

.sci {
  background: rgba(30, 41, 59, 0.6);
  color: #a5b4fc;
  font-size: 24rpx;
}
.theme-light .sci {
  background: #e0e7ff !important;
  color: #4338ca !important;
}

.op {
  background: rgba(2, 132, 199, 0.2);
  color: #38bdf8;
  font-size: 36rpx;
}

.func {
  background: #334155;
  color: #f8fafc;
  font-size: 24rpx;
}

.func-clear {
  background: rgba(244, 63, 94, 0.2);
  color: #fb7185;
}

.equal {
  background: linear-gradient(135deg, #0284c7, #4f46e5);
  color: #ffffff;
  font-size: 40rpx;
  grid-row: span 2;
  height: 206rpx;
}

.span-2 {
  grid-column: span 2;
}

/* History Panel Drawer */
.history-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #0f172a;
  border-top: 1rpx solid #334155;
  border-radius: 36rpx 36rpx 0 0;
  padding: 30rpx;
  max-height: 60vh;
  z-index: 200;
  box-shadow: 0 -10rpx 40rpx rgba(0,0,0,0.6);
}
.theme-light .history-panel {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}
.panel-title { font-size: 28rpx; font-weight: bold; color: #ffffff; }
.theme-light .panel-title { color: #0f172a !important; }

.panel-btns { display: flex; gap: 20rpx; }
.btn-text-danger { font-size: 24rpx; color: #fb7185; }
.btn-text-close { font-size: 24rpx; color: #38bdf8; font-weight: bold; }

.history-list { max-height: 45vh; }
.history-item {
  background: #020617;
  border: 1rpx solid #1e293b;
  border-radius: 16rpx;
  padding: 20rpx;
  margin-bottom: 12rpx;
  display: flex;
  justify-content: space-between;
}
.theme-light .history-item {
  background: #f8fafc !important;
  border-color: #e2e8f0 !important;
}
.h-expr { font-size: 24rpx; color: #94a3b8; font-family: monospace; }
.h-res { font-size: 26rpx; font-weight: bold; color: #38bdf8; font-family: monospace; }
.empty-tip { text-align: center; padding: 40rpx; color: #64748b; font-size: 24rpx; }
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.wxss'), 'w', encoding='utf-8') as f:
    f.write(index_wxss)

# 8. pages/index/index.json
index_json = { "navigationBarTitleText": "科学电子计算器" }
with open(os.path.join(base_dir, 'pages', 'index', 'index.json'), 'w', encoding='utf-8') as f:
    json.dump(index_json, f, ensure_ascii=False, indent=2)

print("Generated Scientific Calculator WeChat Mini Program project successfully!")
