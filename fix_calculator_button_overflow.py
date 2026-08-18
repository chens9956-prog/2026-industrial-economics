import os
import json

base_dir = r'l:\我的云端硬盘\2026产业经济学\glass-calculator-wxapp'

# 1. index.wxml - Replace <button> with <view class="btn-key"> to eliminate native button width overflow!
index_wxml = """<view class="container {{skinMode}}">

  <!-- CUTE ANIMAL DECORATION -->
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
        <image class="app-logo-icon" src="/icon.png" mode="aspectFit" />
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
        <text class="expression">{{subDisplay}}</text>
      </scroll-view>
      <text class="main-screen">{{mainDisplay}}</text>
    </view>

    <!-- Function Mode Tabs -->
    <view class="mode-tabs">
      <text class="tab-item {{isSciMode ? 'active' : ''}}" bindtap="onToggleSciMode">高阶科学函数</text>
      <text class="tab-item {{!isSciMode ? 'active' : ''}}" bindtap="onToggleSciMode">基础计算</text>
    </view>

    <!-- Scientific Function Keys Row (5 Keys) -->
    <view class="keypad-sci" wx:if="{{isSciMode}}">
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="sin(">sin</view>
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="cos(">cos</view>
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="tan(">tan</view>
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="ln(">ln</view>
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="log(">log</view>
    </view>

    <!-- Main Grid Layout (5 Columns x 5 Rows = 25 Key Slots, ALL 5 COLUMNS VISIBLE!) -->
    <view class="keypad-grid">
      <!-- Row 1: AC, DEL, (, ), ÷ -->
      <view class="btn-key func-clear" hover-class="btn-hover" bindtap="onClear">AC</view>
      <view class="btn-key func" hover-class="btn-hover" bindtap="onDelete">DEL</view>
      <view class="btn-key func" hover-class="btn-hover" bindtap="onTapKey" data-val="(">(</view>
      <view class="btn-key func" hover-class="btn-hover" bindtap="onTapKey" data-val=")">)</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="÷">÷</view>

      <!-- Row 2: 7, 8, 9, %, × -->
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="7">7</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="8">8</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="9">9</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="%">%</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="×">×</view>

      <!-- Row 3: 4, 5, 6, ^, - -->
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="4">4</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="5">5</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="6">6</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="^">x^y</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="-">-</view>

      <!-- Row 4: 1, 2, 3, √, + -->
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="1">1</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="2">2</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="3">3</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="√(">√</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="+">+</view>

      <!-- Row 5: 0 (span 2), ., π, = (PROMINENT BRIGHT AMBER '=' BUTTON!) -->
      <view class="btn-key num span-2" hover-class="btn-hover" bindtap="onTapKey" data-val="0">0</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val=".">.</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="π">π</view>
      <view class="btn-key btn-equal" hover-class="btn-hover" bindtap="onCalculate">=</view>
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

# 2. index.wxss - Reset native button overflow & force 5-column grid
index_wxss = """/* ==========================================================================
   5-COLUMN GRID CALCULATOR WITH PERFECT BUTTON OVERFLOW RESET
   ========================================================================== */

page {
  box-sizing: border-box;
}

.container {
  padding: 16rpx;
  min-height: 100vh;
  box-sizing: border-box;
}

.app-logo-icon {
  width: 50rpx;
  height: 50rpx;
  border-radius: 12rpx;
}

.keypad-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10rpx;
  width: 100%;
  box-sizing: border-box;
}

.keypad-sci {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10rpx;
  margin-bottom: 10rpx;
  width: 100%;
  box-sizing: border-box;
}

.btn-key {
  height: 90rpx;
  border-radius: 20rpx;
  font-size: 30rpx;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  min-width: 0 !important;
  box-sizing: border-box !important;
  user-select: none;
}

.btn-hover {
  opacity: 0.7;
  transform: scale(0.96);
}

.btn-equal {
  background: linear-gradient(135deg, #f59e0b, #d97706) !important;
  color: #ffffff !important;
  font-size: 44rpx !important;
  font-weight: 800 !important;
  box-shadow: 0 6rpx 0 #b45309 !important;
  border-radius: 20rpx !important;
}

.main-screen {
  display: block;
  font-size: 52rpx;
  font-weight: bold;
  color: #38bdf8;
  font-family: monospace;
  margin-top: 6rpx;
  min-height: 64rpx;
}

/* 1. 企鹅宝宝外套 (Baby Penguin Skin) */
.skin-penguin {
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 40%, #0284c7 100%) !important;
}
.skin-penguin .calc-card {
  background: #ffffff !important;
  border: 4rpx solid #38bdf8 !important;
  border-radius: 40rpx !important;
  box-shadow: 0 16rpx 50rpx rgba(2, 132, 199, 0.4) !important;
  position: relative;
}
.skin-penguin .title { color: #0f172a !important; font-size: 28rpx; font-weight: 800; }
.skin-penguin .calc-display {
  background: #f0f9ff !important;
  border: 2rpx solid #bae6fd !important;
  border-radius: 24rpx !important;
}
.skin-penguin .expression { color: #0369a1 !important; }
.skin-penguin .main-screen { color: #0284c7 !important; }
.skin-penguin .btn-key.num {
  background: #ffffff !important;
  color: #0f172a !important;
  border: 2rpx solid #e0f2fe !important;
  box-shadow: 0 4rpx 0 #bae6fd !important;
}
.skin-penguin .btn-key.sci {
  background: #e0f2fe !important;
  color: #0369a1 !important;
  border: 2rpx solid #bae6fd !important;
  box-shadow: 0 4rpx 0 #7dd3fc !important;
}
.skin-penguin .btn-key.op {
  background: #38bdf8 !important;
  color: #ffffff !important;
  box-shadow: 0 4rpx 0 #0284c7 !important;
}

/* 2. 可爱小熊外套 (Cute Little Bear Skin) */
.skin-bear {
  background: linear-gradient(180deg, #451a03 0%, #78350f 50%, #9a3412 100%) !important;
}
.skin-bear .calc-card {
  background: #fffbeb !important;
  border: 4rpx solid #f59e0b !important;
  border-radius: 40rpx !important;
  box-shadow: 0 16rpx 50rpx rgba(180, 83, 9, 0.4) !important;
}
.skin-bear .title { color: #78350f !important; font-size: 28rpx; font-weight: 800; }
.skin-bear .calc-display {
  background: #fef3c7 !important;
  border: 2rpx solid #fde68a !important;
  border-radius: 24rpx !important;
}
.skin-bear .expression { color: #92400e !important; }
.skin-bear .main-screen { color: #b45309 !important; }
.skin-bear .btn-key.num {
  background: #ffffff !important;
  color: #78350f !important;
  border: 2rpx solid #fef3c7 !important;
  box-shadow: 0 4rpx 0 #fde68a !important;
}
.skin-bear .btn-key.sci {
  background: #fef3c7 !important;
  color: #92400e !important;
  border: 2rpx solid #fde68a !important;
  box-shadow: 0 4rpx 0 #fcd34d !important;
}
.skin-bear .btn-key.op {
  background: #f59e0b !important;
  color: #ffffff !important;
  box-shadow: 0 4rpx 0 #d97706 !important;
}
.skin-bear .btn-key.btn-equal {
  background: linear-gradient(180deg, #ea580c, #c2410c) !important;
  color: #ffffff !important;
  box-shadow: 0 4rpx 0 #9a3412 !important;
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
  padding: 0 50rpx;
  margin-bottom: -16rpx;
  position: relative;
  z-index: 10;
}
.penguin-ear, .bear-ear {
  width: 60rpx;
  height: 60rpx;
  border-radius: 40rpx 40rpx 0 0;
}
.skin-penguin .penguin-ear {
  background: #0f172a;
  border: 3rpx solid #38bdf8;
  border-bottom: none;
}
.skin-bear .bear-ear {
  background: #78350f;
  border: 3rpx solid #f59e0b;
  border-bottom: none;
}
.penguin-beak, .bear-face {
  font-size: 40rpx;
}

/* --- HEADER & BUTTONS --- */
.calc-card {
  background: rgba(15, 23, 42, 0.95);
  border: 1rpx solid #1e293b;
  border-radius: 36rpx;
  padding: 20rpx;
  box-shadow: 0 20rpx 50rpx rgba(0,0,0,0.5);
  width: 100%;
  box-sizing: border-box;
}

.calc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
  flex-wrap: wrap;
  gap: 10rpx;
}

.title-box { display: flex; align-items: center; gap: 10rpx; }
.title { font-size: 26rpx; font-weight: bold; color: #ffffff; }

.skin-selector { display: flex; gap: 6rpx; }
.skin-btn {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  font-size: 18rpx;
  font-weight: bold;
  padding: 4rpx 10rpx;
  border-radius: 16rpx;
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
  border-radius: 20rpx;
  padding: 16rpx 20rpx;
  margin-bottom: 16rpx;
  text-align: right;
}

.expr-scroll {
  white-space: nowrap;
  width: 100%;
}
.expression {
  font-size: 22rpx;
  color: #94a3b8;
  font-family: monospace;
}

.mode-tabs {
  display: flex;
  gap: 16rpx;
  margin-bottom: 14rpx;
}
.tab-item {
  font-size: 20rpx;
  color: #64748b;
  font-weight: bold;
}
.tab-item.active {
  color: #38bdf8;
  border-bottom: 2rpx solid #38bdf8;
}

.num {
  background: #1e293b;
  color: #f8fafc;
}

.sci {
  background: rgba(30, 41, 59, 0.6);
  color: #a5b4fc;
  font-size: 22rpx;
}

.op {
  background: rgba(2, 132, 199, 0.2);
  color: #38bdf8;
  font-size: 32rpx;
}

.func {
  background: #334155;
  color: #f8fafc;
  font-size: 22rpx;
}

.func-clear {
  background: rgba(244, 63, 94, 0.2);
  color: #fb7185;
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

print("Fixed button width overflow and updated equal button rendering!")
