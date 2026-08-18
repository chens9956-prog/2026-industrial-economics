import os
import json

base_dir = r'l:\我的云端硬盘\2026产业经济学\glass-calculator-wxapp'

# 1. index.wxml
index_wxml = """<view class="container {{skinMode}}">

  <!-- CUTE ANIMAL EARS DECORATION ON TOP OF CALCULATOR FRAME -->
  <view class="cute-ears-wrapper" wx:if="{{skinMode === 'skin-penguin'}}">
    <view class="penguin-ear left-ear"><view class="inner-ear"></view></view>
    <view class="penguin-beak">🐧</view>
    <view class="penguin-ear right-ear"><view class="inner-ear"></view></view>
  </view>

  <view class="cute-ears-wrapper" wx:if="{{skinMode === 'skin-bear'}}">
    <view class="bear-ear left-ear"></view>
    <view class="bear-face">🐻</view>
    <view class="bear-ear right-ear"></view>
  </view>

  <!-- CALCULATOR MAIN CARD -->
  <view class="calc-card">

    <!-- Skin Switcher Header Controls -->
    <view class="calc-header">
      <view class="title-box">
        <text class="skin-avatar" wx:if="{{skinMode === 'skin-penguin'}}">🐧</text>
        <text class="skin-avatar" wx:elif="{{skinMode === 'skin-bear'}}">🐻</text>
        <text class="skin-avatar" wx:else>🧮</text>
        <text class="title">{{skinTitle}}</text>
      </view>

      <!-- Skin Selector Menu Buttons -->
      <view class="skin-selector">
        <view class="skin-btn {{skinMode === 'skin-penguin' ? 'active' : ''}}" bindtap="onSelectSkin" data-skin="skin-penguin">🐧企鹅</view>
        <view class="skin-btn {{skinMode === 'skin-bear' ? 'active' : ''}}" bindtap="onSelectSkin" data-skin="skin-bear">🐻小熊</view>
        <view class="skin-btn {{skinMode === 'skin-aurora' ? 'active' : ''}}" bindtap="onSelectSkin" data-skin="skin-aurora">🌌赛博</view>
        <view class="skin-btn history-btn" bindtap="onToggleHistory">📜历史</view>
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

# 2. index.js
index_js = """Page({
  data: {
    expression: '',
    result: '0',
    isSciMode: true,
    showHistory: false,
    historyList: [],
    skinMode: 'skin-penguin', // Default cute skin: Penguin Baby
    skinTitle: '企鹅宝宝计算器'
  },

  onLoad() {
    const historyList = wx.getStorageSync('calc_history_v1') || [];
    const skinMode = wx.getStorageSync('calc_skin_v1') || 'skin-penguin';
    this.applySkin(skinMode);
    this.setData({ historyList });
  },

  applySkin(skin) {
    let title = '企鹅宝宝计算器';
    if (skin === 'skin-bear') title = '可爱小熊计算器';
    if (skin === 'skin-aurora') title = '极光赛博计算器';

    this.setData({
      skinMode: skin,
      skinTitle: title
    });
    wx.setStorageSync('calc_skin_v1', skin);
  },

  onSelectSkin(e) {
    const skin = e.currentTarget.dataset.skin;
    this.applySkin(skin);
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

# 3. index.wxss
index_wxss = """/* ==========================================================================
   CUTE ANIMAL SKINS (企鹅宝宝 / 可爱小熊 / 极光赛博)
   ========================================================================== */

/* 1. 企鹅宝宝外套 (Baby Penguin Skin) */
.skin-penguin {
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 40%, #0284c7 100%) !important;
}
.skin-penguin .calc-card {
  background: #ffffff !important;
  border: 4rpx solid #38bdf8 !important;
  border-radius: 48rpx !important;
  box-shadow: 0 20rpx 60rpx rgba(2, 132, 199, 0.4) !important;
  position: relative;
}
.skin-penguin .title { color: #0f172a !important; font-size: 30rpx; font-weight: 800; }
.skin-penguin .calc-display {
  background: #f0f9ff !important;
  border: 3rpx solid #bae6fd !important;
  border-radius: 30rpx !important;
}
.skin-penguin .expression { color: #0369a1 !important; }
.skin-penguin .result { color: #0284c7 !important; }
.skin-penguin .btn-key.num {
  background: #ffffff !important;
  color: #0f172a !important;
  border: 2rpx solid #e0f2fe !important;
  box-shadow: 0 6rpx 0 #bae6fd !important;
  border-radius: 28rpx !important;
}
.skin-penguin .btn-key.sci {
  background: #e0f2fe !important;
  color: #0369a1 !important;
  border: 2rpx solid #bae6fd !important;
  box-shadow: 0 6rpx 0 #7dd3fc !important;
  border-radius: 28rpx !important;
}
.skin-penguin .btn-key.op {
  background: #38bdf8 !important;
  color: #ffffff !important;
  box-shadow: 0 6rpx 0 #0284c7 !important;
  border-radius: 28rpx !important;
}
.skin-penguin .btn-key.equal {
  background: linear-gradient(180deg, #f59e0b, #d97706) !important;
  color: #ffffff !important;
  box-shadow: 0 6rpx 0 #b45309 !important;
  border-radius: 28rpx !important;
}

/* 2. 可爱小熊外套 (Cute Little Bear Skin) */
.skin-bear {
  background: linear-gradient(180deg, #451a03 0%, #78350f 50%, #9a3412 100%) !important;
}
.skin-bear .calc-card {
  background: #fffbeb !important;
  border: 4rpx solid #f59e0b !important;
  border-radius: 48rpx !important;
  box-shadow: 0 20rpx 60rpx rgba(180, 83, 9, 0.4) !important;
}
.skin-bear .title { color: #78350f !important; font-size: 30rpx; font-weight: 800; }
.skin-bear .calc-display {
  background: #fef3c7 !important;
  border: 3rpx solid #fde68a !important;
  border-radius: 30rpx !important;
}
.skin-bear .expression { color: #92400e !important; }
.skin-bear .result { color: #b45309 !important; }
.skin-bear .btn-key.num {
  background: #ffffff !important;
  color: #78350f !important;
  border: 2rpx solid #fef3c7 !important;
  box-shadow: 0 6rpx 0 #fde68a !important;
  border-radius: 28rpx !important;
}
.skin-bear .btn-key.sci {
  background: #fef3c7 !important;
  color: #92400e !important;
  border: 2rpx solid #fde68a !important;
  box-shadow: 0 6rpx 0 #fcd34d !important;
  border-radius: 28rpx !important;
}
.skin-bear .btn-key.op {
  background: #f59e0b !important;
  color: #ffffff !important;
  box-shadow: 0 6rpx 0 #d97706 !important;
  border-radius: 28rpx !important;
}
.skin-bear .btn-key.equal {
  background: linear-gradient(180deg, #ea580c, #c2410c) !important;
  color: #ffffff !important;
  box-shadow: 0 6rpx 0 #9a3412 !important;
  border-radius: 28rpx !important;
}

/* 3. 极光赛博外套 (Aurora Sci-Fi Skin) */
.skin-aurora {
  background: #090d16 !important;
}

/* --- CUTE ANIMAL EARS AT TOP --- */
.cute-ears-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 0 60rpx;
  margin-bottom: -20rpx;
  position: relative;
  z-index: 10;
}
.penguin-ear, .bear-ear {
  width: 70rpx;
  height: 70rpx;
  border-radius: 50rpx 50rpx 0 0;
}
.skin-penguin .penguin-ear {
  background: #0f172a;
  border: 4rpx solid #38bdf8;
  border-bottom: none;
}
.skin-bear .bear-ear {
  background: #78350f;
  border: 4rpx solid #f59e0b;
  border-bottom: none;
}
.penguin-beak, .bear-face {
  font-size: 50rpx;
}

/* --- HEADER & BUTTONS --- */
.calc-card {
  background: rgba(15, 23, 42, 0.95);
  border: 1rpx solid #1e293b;
  border-radius: 36rpx;
  padding: 30rpx;
  box-shadow: 0 20rpx 50rpx rgba(0,0,0,0.5);
}

.calc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
  flex-wrap: wrap;
  gap: 10rpx;
}

.title-box { display: flex; align-items: center; gap: 10rpx; }
.skin-avatar { font-size: 40rpx; }
.title { font-size: 28rpx; font-weight: bold; color: #ffffff; }

.skin-selector { display: flex; gap: 8rpx; }
.skin-btn {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  font-size: 20rpx;
  font-weight: bold;
  padding: 6rpx 14rpx;
  border-radius: 20rpx;
}
.skin-btn.active {
  background: #38bdf8;
  color: #0f172a;
}
.history-btn {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
}

.calc-display {
  background: #020617;
  border: 1rpx solid #1e293b;
  border-radius: 24rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
  text-align: right;
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

.sci {
  background: rgba(30, 41, 59, 0.6);
  color: #a5b4fc;
  font-size: 24rpx;
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

.panel-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}
.panel-title { font-size: 28rpx; font-weight: bold; color: #ffffff; }

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
.h-expr { font-size: 24rpx; color: #94a3b8; font-family: monospace; }
.h-res { font-size: 26rpx; font-weight: bold; color: #38bdf8; font-family: monospace; }
.empty-tip { text-align: center; padding: 40rpx; color: #64748b; font-size: 24rpx; }
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.wxss'), 'w', encoding='utf-8') as f:
    f.write(index_wxss)

print("Updated calculator mini program with Cute Animal Skins (Penguin, Bear, Aurora) successfully!")
