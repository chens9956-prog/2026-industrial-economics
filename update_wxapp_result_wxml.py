import os

base_dir = r'l:\我的云端硬盘\2026产业经济学\industrial-economics-wxapp'

result_wxml = """<view class="container {{themeClass}}">
  <view class="card">
    <view class="top-row font-mono">
      <button class="btn-theme-toggle" bindtap="onToggleTheme">🌓 {{themeName}}</button>
    </view>

    <text class="res-title">🎉 测试已完成！</text>
    
    <view class="query-notice" wx:if="{{checkCount > 0}}">
      <text class="notice-badge">【查分模式 · 第 {{checkCount}}/2 次】</text>
      <text class="notice-countdown">倒计时 {{countdownSeconds}} 秒后自动关闭</text>
      <text class="notice-desc">只读不可修改答案，最多允许 2 次查分限制。</text>
    </view>

    <!-- 1. TOP SCORE DISPLAY CARD (顶部得分卡片) -->
    <view class="score-card shadow-score top-score">
      <view class="score-col border-right">
        <text class="score-label">您的最终得分</text>
        <text class="score-val">{{record.score}}</text>
        <text class="score-sub">满分 100 分 (40单选+20多选)</text>
      </view>
      <view class="score-col">
        <text class="score-label">用时与正确率</text>
        <text class="acc-val">{{record.accuracy}}</text>
        <text class="score-sub">用时 {{record.duration}}</text>
      </view>
    </view>

    <!-- Details breakdown -->
    <view class="details-title">📋 60道试题明细与解析（全卷100分）</view>
    <block wx:for="{{questions}}" wx:key="id" wx:for-index="idx">
      <view class="detail-card {{(record.userAnswers[item.id] === item.answer) ? 'border-green' : 'border-red'}}">
        <view class="detail-header">
          <text class="q-num">第 {{idx + 1}} 题 / 共60题【{{item.chapter}} · {{item.type === 'multiple' ? '多选' : '单选'}}】</text>
          <text class="status {{(record.userAnswers[item.id] === item.answer) ? 'text-green' : 'text-red'}}">
            {{(record.userAnswers[item.id] === item.answer) ? '✓ 回答正确' : '✕ 回答错误'}}
          </text>
        </view>
        <text class="q-title">{{item.title}}</text>
        <view class="ans-row">
          <text class="ans-item">您的选择：<text class="bold">{{record.userAnswers[item.id] || '未作答'}}</text></text>
          <text class="ans-item">正确答案：<text class="bold text-green">{{item.answer}}</text></text>
        </view>
        <view class="exp-box">
          <text class="exp-text"><text class="exp-tag">权威解析：</text>{{item.explanation}}</text>
        </view>
      </view>
    </block>

    <!-- 2. BOTTOM SCORE DISPLAY CARD (底部得分卡片) -->
    <view class="score-card shadow-score bottom-score">
      <view class="score-col border-right">
        <text class="score-label">您的最终得分</text>
        <text class="score-val">{{record.score}}</text>
        <text class="score-sub">满分 100 分 (40单选+20多选)</text>
      </view>
      <view class="score-col">
        <text class="score-label">用时与正确率</text>
        <text class="acc-val">{{record.accuracy}}</text>
        <text class="score-sub">用时 {{record.duration}}</text>
      </view>
    </view>

    <button class="btn-home" bindtap="onBackHome">返回考场登录首页</button>
  </view>
</view>
"""

with open(os.path.join(base_dir, 'pages', 'result', 'result.wxml'), 'w', encoding='utf-8') as f:
    f.write(result_wxml)

print("Updated result.wxml successfully!")
