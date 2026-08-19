import os
import json

base_dir = r'l:\我的云端硬盘\2026产业经济学\industrial-economics-wxapp'

# 1. pages/index/index.wxml
index_wxml = """<view class="container {{themeClass}}">
  <view class="card shadow">
    <view class="top-row">
      <view class="header-tag">学籍匹配身份验证</view>
      <button class="btn-theme-toggle" bindtap="onToggleTheme">🌓 {{themeName}}</button>
    </view>
    <view class="title">产业经济学 · 在线随堂考试</view>
    <view class="subtitle">教材：刘志彪《产业经济学》（第3版）前10章专案命题</view>

    <view class="form-group">
      <text class="label">学号 (Student ID)</text>
      <input class="input" placeholder="例如：2026010001" bindinput="onInputId" value="{{studentId}}" />
    </view>

    <view class="form-group">
      <text class="label">姓名 (Full Name)</text>
      <input class="input" placeholder="例如：高建刚" bindinput="onInputName" value="{{studentName}}" />
    </view>

    <view class="error-banner" wx:if="{{errorMsg}}">
      <text class="error-text">{{errorMsg}}</text>
    </view>

    <view class="notice-box">
      <text class="notice-title">⚠️ 期中考试须知：</text>
      <text class="notice-item">• 题量及分值：全卷共 60 道题（40单选每题1.5分 + 20多选每题2分，满分100分）。</text>
      <text class="notice-item">• 考试时长：75 分钟限时答题，支持中途【退出考试】。</text>
      <text class="notice-item">• 成绩展示：得分与正确率在页面【顶部与底部双重展示】。</text>
      <text class="notice-item">• 查分限制：提交后最多允许 2 次查分（每次15秒后自动关闭）。</text>
    </view>

    <button class="btn-primary" bindtap="onStartExam">验证身份并开始测试 (60题/75分钟)</button>
  </view>

  <view class="footer-link" bindtap="onNavAdmin">
    <text class="link-text">🔒 教师/管理员控制台入口</text>
  </view>
</view>
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.wxml'), 'w', encoding='utf-8') as f:
    f.write(index_wxml)

# 2. pages/exam/exam.wxml
exam_wxml = """<view class="container {{themeClass}}">
  <!-- Sticky Header Bar -->
  <view class="sticky-header">
    <view class="info-row">
      <text class="student-info">考生：{{student.id}} - {{student.name}}</text>
      <button class="btn-theme-toggle" bindtap="onToggleTheme">🌓 {{themeName}}</button>
    </view>
    <view class="action-row">
      <text class="progress">进度：{{answeredCount}} / 60 题</text>
      <text class="timer text-amber">剩余时间：{{timerStr}}</text>
      <button class="btn-exit" bindtap="onExitExam">🚪 退出考试</button>
    </view>
  </view>

  <!-- Questions List -->
  <view class="questions-list">
    <block wx:for="{{questions}}" wx:key="id" wx:for-index="idx">
      <view class="card q-card">
        <view class="q-header">
          <text class="q-badge {{item.type === 'multiple' ? 'badge-multi' : ''}}">第 {{idx + 1}} 题</text>
          <text class="q-tag">【{{item.chapter}} · {{item.type === 'multiple' ? '多选题 · 2分' : '单选题 · 1.5分'}}】</text>
        </view>
        <text class="q-title">{{item.title}}</text>

        <view class="options-group">
          <block wx:for="{{item.options}}" wx:for-item="opt" wx:key="key">
            <view class="opt-item {{item.type === 'multiple' ? (selectedMap[item.id + '_' + opt.key] ? 'opt-selected-multi' : '') : (userAnswers[item.id] === opt.key ? 'opt-selected' : '')}}" bindtap="onSelectOption" data-qid="{{item.id}}" data-type="{{item.type}}" data-key="{{opt.key}}">
              <text class="opt-key {{item.type === 'multiple' ? 'key-multi' : ''}}">{{opt.key}}</text>
              <text class="opt-text">{{opt.text}}</text>
            </view>
          </block>
        </view>
      </view>
    </block>
  </view>

  <!-- Submit Button -->
  <view class="bottom-bar">
    <button class="btn-submit" bindtap="onSubmitExam">确认交卷并查看成绩 (60题)</button>
  </view>
</view>
"""
with open(os.path.join(base_dir, 'pages', 'exam', 'exam.wxml'), 'w', encoding='utf-8') as f:
    f.write(exam_wxml)

# 3. pages/exam/exam.js
exam_js = """const questions = require('../../data/questions.js');

Page({
  data: {
    student: { id: '', name: '' },
    questions: questions,
    userAnswers: {},
    selectedMap: {},
    answeredCount: 0,
    timeRemaining: 75 * 60,
    timerStr: '75:00',
    themeClass: 'theme-dark',
    themeName: '深色模式'
  },

  timerInterval: null,
  timeElapsed: 0,

  onLoad() {
    const student = getApp().globalData.currentStudent || { id: '2026010001', name: '高建刚' };
    this.setData({ student });
    this.startTimer();

    const savedTheme = wx.getStorageSync('theme_mode') || 'dark';
    this.applyTheme(savedTheme);
  },

  applyTheme(mode) {
    if (mode === 'light') {
      this.setData({ themeClass: 'theme-light', themeName: '浅色模式' });
    } else {
      this.setData({ themeClass: 'theme-dark', themeName: '深色模式' });
    }
  },

  onToggleTheme() {
    const current = wx.getStorageSync('theme_mode') === 'light' ? 'dark' : 'light';
    wx.setStorageSync('theme_mode', current);
    this.applyTheme(current);
  },

  onUnload() {
    if (this.timerInterval) clearInterval(this.timerInterval);
  },

  startTimer() {
    this.updateTimerStr();
    this.timerInterval = setInterval(() => {
      let timeRemaining = this.data.timeRemaining - 1;
      this.timeElapsed += 1;

      if (timeRemaining <= 0) {
        clearInterval(this.timerInterval);
        wx.showModal({
          title: '考试时间到',
          content: '75分钟倒计时结束，系统已为您自动交卷！',
          showCancel: false,
          success: () => this.submitExam()
        });
        return;
      }

      this.setData({ timeRemaining });
      this.updateTimerStr();
    }, 1000);
  },

  updateTimerStr() {
    const mins = Math.floor(this.data.timeRemaining / 60);
    const secs = this.data.timeRemaining % 60;
    const timerStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    this.setData({ timerStr });
  },

  onSelectOption(e) {
    const { qid, type, key } = e.currentTarget.dataset;
    let userAnswers = { ...this.data.userAnswers };
    let selectedMap = { ...this.data.selectedMap };

    if (type === 'single') {
      userAnswers[qid] = key;
    } else {
      // Multiple choice toggle
      const mapKey = qid + '_' + key;
      selectedMap[mapKey] = !selectedMap[mapKey];

      let currentKeys = [];
      ['A', 'B', 'C', 'D'].forEach(k => {
        if (selectedMap[qid + '_' + k]) currentKeys.push(k);
      });

      if (currentKeys.length > 0) {
        userAnswers[qid] = currentKeys.join('');
      } else {
        delete userAnswers[qid];
      }
    }

    const answeredCount = Object.keys(userAnswers).length;
    this.setData({ userAnswers, selectedMap, answeredCount });
  },

  onExitExam() {
    wx.showModal({
      title: '退出考试确认',
      content: '确定要退出本次随堂考试吗？未提交的选项将被清空，您可稍后再重新登录作答。',
      success: (res) => {
        if (res.confirm) {
          if (this.timerInterval) clearInterval(this.timerInterval);
          wx.navigateBack();
        }
      }
    });
  },

  onSubmitExam() {
    const unanswered = this.data.questions.length - this.data.answeredCount;
    if (unanswered > 0) {
      wx.showModal({
        title: '交卷确认',
        content: `您还有 ${unanswered} 道题未作答，确定要现在交卷吗？`,
        success: (res) => {
          if (res.confirm) this.submitExam();
        }
      });
    } else {
      this.submitExam();
    }
  },

  submitExam() {
    if (this.timerInterval) clearInterval(this.timerInterval);

    let totalScore = 0;
    let correctCount = 0;

    this.data.questions.forEach(q => {
      const uAns = this.data.userAnswers[q.id] || '';
      const cAns = q.answer;

      if (q.type === 'single') {
        if (uAns === cAns) {
          totalScore += 1.5;
          correctCount++;
        }
      } else {
        if (uAns.split('').sort().join('') === cAns.split('').sort().join('')) {
          totalScore += 2.0;
          correctCount++;
        }
      }
    });

    totalScore = Math.round(totalScore * 10) / 10;
    const accuracy = Math.round((correctCount / this.data.questions.length) * 100) + '%';
    const durationMin = Math.floor(this.timeElapsed / 60);
    const durationSec = this.timeElapsed % 60;
    const duration = `${String(durationMin).padStart(2, '0')}:${String(durationSec).padStart(2, '0')}`;

    const record = {
      id: this.data.student.id,
      name: this.data.student.name,
      score: totalScore,
      accuracy,
      duration,
      userAnswers: this.data.userAnswers,
      scoreCheckedCount: 0,
      timestamp: new Date().toLocaleString('zh-CN', { hour12: false })
    };

    let submissions = wx.getStorageSync('exam_submissions_v1') || [];
    let idx = submissions.findIndex(r => r.id.trim() === record.id.trim());
    if (idx >= 0) submissions[idx] = record;
    else submissions.unshift(record);
    wx.setStorageSync('exam_submissions_v1', submissions);

    wx.redirectTo({
      url: `/pages/result/result?record=${encodeURIComponent(JSON.stringify(record))}&checkCount=0`
    });
  }
})
"""
with open(os.path.join(base_dir, 'pages', 'exam', 'exam.js'), 'w', encoding='utf-8') as f:
    f.write(exam_js)

# 4. pages/exam/exam.wxss
exam_wxss_append = """
.badge-multi {
  background: rgba(99, 102, 241, 0.2) !important;
  color: #a5b4fc !important;
  border-color: rgba(99, 102, 241, 0.4) !important;
}

.opt-selected-multi {
  border-color: #818cf8 !important;
  background: rgba(99, 102, 241, 0.25) !important;
}
.theme-light .opt-selected-multi {
  background: #e0e7ff !important;
  border-color: #4f46e5 !important;
}

.key-multi {
  border-radius: 8rpx !important;
}
.opt-selected-multi .opt-key {
  background: #4f46e5 !important;
  color: #ffffff !important;
}
"""
with open(os.path.join(base_dir, 'pages', 'exam', 'exam.wxss'), 'a', encoding='utf-8') as f:
    f.write(exam_wxss_append)

print("Updated industrial-economics-wxapp Mini Program pages successfully!")
