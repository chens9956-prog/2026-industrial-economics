import os
import json

base_dir = r'l:\我的云端硬盘\2026产业经济学\industrial-economics-wxapp'

# --- 1. PAGES / EXAM ---
exam_wxml = """<view class="container">
  <!-- Sticky Header Bar -->
  <view class="sticky-header">
    <view class="info-row">
      <text class="student-info">考生：{{student.id}} - {{student.name}}</text>
      <text class="timer text-amber">剩余时间：{{timerStr}}</text>
    </view>
    <view class="action-row">
      <text class="progress">已答：{{answeredCount}} / 50 题</text>
      <button class="btn-exit" bindtap="onExitExam">🚪 退出考试</button>
    </view>
  </view>

  <!-- Questions List -->
  <view class="questions-list">
    <block wx:for="{{questions}}" wx:key="id" wx:for-index="idx">
      <view class="card q-card">
        <view class="q-header">
          <text class="q-badge">第 {{idx + 1}} 题</text>
          <text class="q-tag">【{{item.chapter}} · 2分】</text>
        </view>
        <text class="q-title">{{item.title}}</text>

        <view class="options-group">
          <block wx:for="{{item.options}}" wx:for-item="opt" wx:key="key">
            <view class="opt-item {{userAnswers[item.id] === opt.key ? 'opt-selected' : ''}}" bindtap="onSelectOption" data-qid="{{item.id}}" data-key="{{opt.key}}">
              <text class="opt-key">{{opt.key}}</text>
              <text class="opt-text">{{opt.text}}</text>
            </view>
          </block>
        </view>
      </view>
    </block>
  </view>

  <!-- Submit Button -->
  <view class="bottom-bar">
    <button class="btn-submit" bindtap="onSubmitExam">确认交卷并查看成绩 (50题)</button>
  </view>
</view>
"""
with open(os.path.join(base_dir, 'pages', 'exam', 'exam.wxml'), 'w', encoding='utf-8') as f:
    f.write(exam_wxml)

exam_js = """const questions = require('../../data/questions.js');

Page({
  data: {
    student: { id: '', name: '' },
    questions: questions,
    userAnswers: {},
    answeredCount: 0,
    timeRemaining: 75 * 60,
    timerStr: '75:00'
  },

  timerInterval: null,
  timeElapsed: 0,

  onLoad() {
    const student = getApp().globalData.currentStudent || { id: '2026010001', name: '高建刚' };
    this.setData({ student });
    this.startTimer();
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
    const { qid, key } = e.currentTarget.dataset;
    const userAnswers = { ...this.data.userAnswers, [qid]: key };
    const answeredCount = Object.keys(userAnswers).length;
    this.setData({ userAnswers, answeredCount });
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

    let correctCount = 0;
    this.data.questions.forEach(q => {
      if (this.data.userAnswers[q.id] === q.answer) correctCount++;
    });

    const score = correctCount * 2;
    const accuracy = Math.round((correctCount / this.data.questions.length) * 100) + '%';
    const durationMin = Math.floor(this.timeElapsed / 60);
    const durationSec = this.timeElapsed % 60;
    const duration = `${String(durationMin).padStart(2, '0')}:${String(durationSec).padStart(2, '0')}`;

    const record = {
      id: this.data.student.id,
      name: this.data.student.name,
      score,
      accuracy,
      duration,
      userAnswers: this.data.userAnswers,
      scoreCheckedCount: 0,
      timestamp: new Date().toLocaleString('zh-CN', { hour12: false })
    };

    // Save to storage
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

exam_wxss = """.sticky-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(15, 23, 42, 0.95);
  border: 1rpx solid #1e293b;
  border-radius: 24rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
  backdrop-filter: blur(10px);
}
.info-row, .action-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.info-row { margin-bottom: 12rpx; }
.student-info { font-size: 26rpx; font-weight: bold; color: #38bdf8; }
.timer { font-size: 28rpx; font-weight: bold; font-family: monospace; color: #fbbf24; }
.progress { font-size: 24rpx; color: #94a3b8; }
.btn-exit {
  background: rgba(244, 63, 94, 0.2);
  color: #fb7185;
  border: 1rpx solid rgba(244, 63, 94, 0.4);
  font-size: 22rpx;
  font-weight: bold;
  padding: 8rpx 20rpx;
  border-radius: 16rpx;
  margin: 0;
}
.q-card { margin-bottom: 30rpx; }
.q-header { display: flex; align-items: center; gap: 12rpx; margin-bottom: 16rpx; }
.q-badge {
  background: rgba(2, 132, 199, 0.2);
  color: #38bdf8;
  border: 1rpx solid rgba(56, 189, 248, 0.3);
  padding: 4rpx 14rpx;
  border-radius: 12rpx;
  font-size: 22rpx;
  font-weight: bold;
}
.q-tag { font-size: 22rpx; color: #94a3b8; }
.q-title { font-size: 30rpx; font-weight: bold; color: #ffffff; line-height: 1.5; margin-bottom: 24rpx; display: block; }
.opt-item {
  display: flex;
  align-items: center;
  background: #020617;
  border: 1rpx solid #1e293b;
  border-radius: 20rpx;
  padding: 20rpx 24rpx;
  margin-bottom: 16rpx;
}
.opt-selected {
  border-color: #38bdf8;
  background: rgba(2, 132, 199, 0.2);
}
.opt-key {
  width: 48rpx;
  height: 48rpx;
  background: #1e293b;
  color: #ffffff;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
  margin-right: 20rpx;
}
.opt-selected .opt-key {
  background: #0284c7;
}
.opt-text { font-size: 26rpx; color: #e2e8f0; flex: 1; }
.bottom-bar { margin-top: 30rpx; margin-bottom: 40rpx; }
.btn-submit {
  background: #10b981;
  color: #ffffff;
  font-weight: bold;
  border-radius: 24rpx;
  padding: 24rpx;
  font-size: 32rpx;
}
"""
with open(os.path.join(base_dir, 'pages', 'exam', 'exam.wxss'), 'w', encoding='utf-8') as f:
    f.write(exam_wxss)

exam_json = { "navigationBarTitleText": "随堂答题中" }
with open(os.path.join(base_dir, 'pages', 'exam', 'exam.json'), 'w', encoding='utf-8') as f:
    json.dump(exam_json, f, ensure_ascii=False, indent=2)

# --- 2. PAGES / RESULT ---
result_wxml = """<view class="container">
  <view class="card">
    <text class="res-title">🎉 测试已完成！</text>
    
    <view class="query-notice" wx:if="{{checkCount > 0}}">
      <text class="notice-badge">【查分模式 · 第 {{checkCount}}/2 次】</text>
      <text class="notice-countdown">倒计时 {{countdownSeconds}} 秒后自动关闭</text>
      <text class="notice-desc">只读不可修改答案，最多允许 2 次查分限制。</text>
    </view>

    <!-- Details breakdown -->
    <view class="details-title">📋 50道试题明细与解析 (每题2分)</view>
    <block wx:for="{{questions}}" wx:key="id" wx:for-index="idx">
      <view class="detail-card {{record.userAnswers[item.id] === item.answer ? 'border-green' : 'border-red'}}">
        <view class="detail-header">
          <text class="q-num">第 {{idx + 1}} 题 / 共50题【{{item.chapter}}】</text>
          <text class="status {{record.userAnswers[item.id] === item.answer ? 'text-green' : 'text-red'}}">
            {{record.userAnswers[item.id] === item.answer ? '✓ 回答正确 (+2分)' : '✕ 回答错误 (0分)'}}
          </text>
        </view>
        <text class="q-title">{{item.title}}</text>
        <view class="ans-row">
          <text class="ans-item">您的选择：<text class="bold">{{record.userAnswers[item.id] || '未作答'}}</text></text>
          <text class="ans-item">正确答案：<text class="bold text-green">{{item.answer}}</text></text>
        </view>
        <view class="exp-box">
          <text class="exp-text"><text class="exp-tag">解析：</text>{{item.explanation}}</text>
        </view>
      </view>
    </block>

    <!-- Score Card Placed AT THE BOTTOM -->
    <view class="score-card shadow-score">
      <view class="score-col border-right">
        <text class="score-label">您的最终得分</text>
        <text class="score-val">{{record.score}}</text>
        <text class="score-sub">满分 100 分 (50题*2分)</text>
      </view>
      <view class="score-col">
        <text class="score-label">用时与正确率</text>
        <text class="acc-val">{{record.accuracy}}</text>
        <text class="score-sub">用时 {{record.duration}}</text>
      </view>
    </view>

    <button class="btn-primary btn-home" bindtap="onBackHome">返回登录主页</button>
  </view>
</view>
"""
with open(os.path.join(base_dir, 'pages', 'result', 'result.wxml'), 'w', encoding='utf-8') as f:
    f.write(result_wxml)

result_js = """const questions = require('../../data/questions.js');

Page({
  data: {
    record: null,
    checkCount: 0,
    countdownSeconds: 15,
    questions: questions
  },

  timer: null,

  onLoad(options) {
    if (options.record) {
      const record = JSON.parse(decodeURIComponent(options.record));
      const checkCount = parseInt(options.checkCount || 0);
      this.setData({ record, checkCount });

      if (checkCount > 0) {
        this.startCountdown();
      }
    }
  },

  onUnload() {
    if (this.timer) clearInterval(this.timer);
  },

  startCountdown() {
    this.timer = setInterval(() => {
      let sec = this.data.countdownSeconds - 1;
      if (sec <= 0) {
        clearInterval(this.timer);
        wx.navigateBack({ delta: 99 });
        return;
      }
      this.setData({ countdownSeconds: sec });
    }, 1000);
  },

  onBackHome() {
    if (this.timer) clearInterval(this.timer);
    wx.navigateBack({ delta: 99 });
  }
})
"""
with open(os.path.join(base_dir, 'pages', 'result', 'result.js'), 'w', encoding='utf-8') as f:
    f.write(result_js)

result_wxss = """.res-title {
  font-size: 38rpx;
  font-weight: 800;
  color: #ffffff;
  text-align: center;
  display: block;
  margin-bottom: 24rpx;
}
.query-notice {
  background: rgba(251, 191, 36, 0.15);
  border: 1rpx solid rgba(251, 191, 36, 0.4);
  padding: 20rpx;
  border-radius: 20rpx;
  margin-bottom: 30rpx;
}
.notice-badge { font-size: 24rpx; font-weight: bold; color: #fbbf24; display: block; margin-bottom: 8rpx; }
.notice-countdown { font-size: 24rpx; font-weight: bold; color: #f59e0b; display: block; margin-bottom: 6rpx; font-family: monospace; }
.notice-desc { font-size: 20rpx; color: #cbd5e1; display: block; }
.details-title { font-size: 28rpx; font-weight: bold; color: #e2e8f0; border-bottom: 1rpx solid #1e293b; padding-bottom: 16rpx; margin-bottom: 24rpx; }
.detail-card {
  background: #020617;
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
}
.border-green { border: 1rpx solid rgba(16, 185, 129, 0.4); }
.border-red { border: 1rpx solid rgba(244, 63, 94, 0.4); }
.detail-header { display: flex; justify-content: space-between; margin-bottom: 12rpx; }
.q-num { font-size: 22rpx; color: #94a3b8; font-family: monospace; }
.status { font-size: 22rpx; font-weight: bold; font-family: monospace; }
.text-green { color: #34d399; }
.text-red { color: #fb7185; }
.q-title { font-size: 28rpx; font-weight: bold; color: #ffffff; margin-bottom: 16rpx; display: block; }
.ans-row { display: flex; gap: 30rpx; margin-bottom: 12rpx; font-size: 22rpx; color: #94a3b8; }
.bold { font-weight: bold; color: #ffffff; }
.exp-box { background: rgba(15, 23, 42, 0.8); padding: 16rpx; border-radius: 14rpx; border: 1rpx solid #1e293b; }
.exp-text { font-size: 22rpx; color: #94a3b8; line-height: 1.5; }
.exp-tag { color: #38bdf8; font-weight: bold; }
.score-card {
  background: linear-gradient(135deg, #020617, #0f172a);
  border: 1rpx solid rgba(56, 189, 248, 0.4);
  border-radius: 30rpx;
  padding: 30rpx;
  display: flex;
  margin-top: 40rpx;
  margin-bottom: 30rpx;
}
.score-col { flex: 1; text-align: center; }
.border-right { border-right: 1rpx solid #1e293b; }
.score-label { font-size: 24rpx; color: #94a3b8; display: block; margin-bottom: 8rpx; }
.score-val { font-size: 64rpx; font-weight: 800; color: #38bdf8; font-family: monospace; display: block; }
.acc-val { font-size: 40rpx; font-weight: 800; color: #34d399; font-family: monospace; display: block; }
.score-sub { font-size: 20rpx; color: #64748b; display: block; }
.btn-home { margin-top: 20rpx; }
"""
with open(os.path.join(base_dir, 'pages', 'result', 'result.wxss'), 'w', encoding='utf-8') as f:
    f.write(result_wxss)

result_json = { "navigationBarTitleText": "成绩答题卡与解析" }
with open(os.path.join(base_dir, 'pages', 'result', 'result.json'), 'w', encoding='utf-8') as f:
    json.dump(result_json, f, ensure_ascii=False, indent=2)

# --- 3. PAGES / ADMIN ---
admin_wxml = """<view class="container">
  <view class="card" wx:if="{{!isUnlocked}}">
    <text class="title text-center">🔒 教师控制台身份登录</text>
    <view class="form-group pt-4">
      <text class="label">管理员密码</text>
      <input class="input" password placeholder="请输入管理员密码 (admin126)" bindinput="onInputPass" value="{{passVal}}" />
    </view>
    <view class="error-banner" wx:if="{{passError}}">
      <text class="error-text">密码错误，请重新输入！</text>
    </view>
    <button class="btn-primary" bindtap="onAdminLogin">登录教师控制台</button>
  </view>

  <view class="card" wx:else>
    <text class="title">👩‍🏫 教师管理面板</text>

    <!-- Tab Buttons -->
    <view class="tab-bar">
      <button class="tab-btn {{activeTab === 'scores' ? 'tab-active' : ''}}" bindtap="onSwitchTab" data-tab="scores">全班成绩单</button>
      <button class="tab-btn {{activeTab === 'roster' ? 'tab-active' : ''}}" bindtap="onSwitchTab" data-tab="roster">学籍名单管理</button>
    </view>

    <!-- Tab 1: Scores -->
    <view class="tab-content" wx:if="{{activeTab === 'scores'}}">
      <text class="sub-title">已收集到 {{records.length}} 条记录</text>
      <block wx:for="{{records}}" wx:key="id">
        <view class="record-card">
          <view class="r-head">
            <text class="r-name">{{item.id}} - {{item.name}}</text>
            <text class="r-score {{item.score >= 60 ? 'text-green' : 'text-red'}}">{{item.score}}分</text>
          </view>
          <view class="r-body">
            <text class="r-info">正确率: {{item.accuracy}} | 用时: {{item.duration}}</text>
            <text class="r-time">{{item.timestamp}}</text>
          </view>
        </view>
      </block>
      <button class="btn-danger" bindtap="onClearRecords">清空所有成绩记录</button>
    </view>

    <!-- Tab 2: Roster -->
    <view class="tab-content" wx:if="{{activeTab === 'roster'}}">
      <text class="sub-title">编辑学籍白名单 (格式：学号,姓名 每行一条)：</text>
      <textarea class="textarea" value="{{rosterText}}" bindinput="onInputRosterText" rows="6" />
      <button class="btn-primary btn-save" bindtap="onSaveRoster">保存白名单</button>
    </view>
  </view>
</view>
"""
with open(os.path.join(base_dir, 'pages', 'admin', 'admin.wxml'), 'w', encoding='utf-8') as f:
    f.write(admin_wxml)

admin_js = """Page({
  data: {
    isUnlocked: false,
    passVal: '',
    passError: false,
    activeTab: 'scores',
    records: [],
    rosterText: ''
  },

  onInputPass(e) {
    this.setData({ passVal: e.detail.value.trim() });
  },

  onAdminLogin() {
    if (this.data.passVal === 'admin126') {
      this.setData({ isUnlocked: true, passError: false });
      this.loadData();
    } else {
      this.setData({ passError: true });
    }
  },

  loadData() {
    const records = wx.getStorageSync('exam_submissions_v1') || [];
    let roster = wx.getStorageSync('student_roster_v1') || [
      { id: '2026010001', name: '高建刚' },
      { id: '2026010002', name: '李明' },
      { id: '2026010003', name: '王芳' }
    ];
    const rosterText = roster.map(s => `${s.id},${s.name}`).join('\n');
    this.setData({ records, rosterText });
  },

  onSwitchTab(e) {
    this.setData({ activeTab: e.currentTarget.dataset.tab });
  },

  onInputRosterText(e) {
    this.setData({ rosterText: e.detail.value });
  },

  onSaveRoster() {
    const lines = this.data.rosterText.split('\n');
    const newRoster = [];
    lines.forEach(l => {
      const parts = l.split(/[,，\s]+/).filter(Boolean);
      if (parts.length >= 2) newRoster.push({ id: parts[0], name: parts[1] });
    });
    if (newRoster.length === 0) {
      wx.showToast({ title: '格式有误', icon: 'none' });
      return;
    }
    wx.setStorageSync('student_roster_v1', newRoster);
    wx.showToast({ title: `成功保存 ${newRoster.length} 名学生`, icon: 'success' });
  },

  onClearRecords() {
    wx.showModal({
      title: '清空确认',
      content: '确定要清空所有已保存的学生成绩记录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.removeStorageSync('exam_submissions_v1');
          this.setData({ records: [] });
        }
      }
    });
  }
})
"""
with open(os.path.join(base_dir, 'pages', 'admin', 'admin.js'), 'w', encoding='utf-8') as f:
    f.write(admin_js)

admin_wxss = """.tab-bar { display: flex; gap: 20rpx; margin-bottom: 24rpx; }
.tab-btn { flex: 1; background: #020617; color: #94a3b8; border: 1rpx solid #1e293b; border-radius: 16rpx; font-size: 24rpx; font-weight: bold; }
.tab-active { background: #0284c7; color: #ffffff; border-color: #38bdf8; }
.sub-title { font-size: 24rpx; color: #94a3b8; display: block; margin-bottom: 16rpx; }
.record-card { background: #020617; border: 1rpx solid #1e293b; border-radius: 16rpx; padding: 20rpx; margin-bottom: 16rpx; }
.r-head { display: flex; justify-content: space-between; margin-bottom: 8rpx; }
.r-name { font-size: 28rpx; font-weight: bold; color: #ffffff; }
.r-score { font-size: 28rpx; font-weight: bold; font-family: monospace; }
.r-body { display: flex; justify-content: space-between; font-size: 20rpx; color: #64748b; }
.textarea { background: #020617; border: 1rpx solid #1e293b; border-radius: 16rpx; padding: 20rpx; color: #ffffff; font-size: 24rpx; font-family: monospace; width: 100%; box-sizing: border-box; margin-bottom: 20rpx; }
.btn-danger { background: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1rpx solid rgba(244, 63, 94, 0.4); font-size: 24rpx; font-weight: bold; margin-top: 30rpx; }
.btn-save { margin-top: 10rpx; }
"""
with open(os.path.join(base_dir, 'pages', 'admin', 'admin.wxss'), 'w', encoding='utf-8') as f:
    f.write(admin_wxss)

admin_json = { "navigationBarTitleText": "教师控制台" }
with open(os.path.join(base_dir, 'pages', 'admin', 'admin.json'), 'w', encoding='utf-8') as f:
    json.dump(admin_json, f, ensure_ascii=False, indent=2)

print("Generated remaining native WeChat Mini Program pages (exam, result, admin) successfully!")
