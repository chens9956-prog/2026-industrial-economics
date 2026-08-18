import os
import json

base_dir = r'l:\我的云端硬盘\2026产业经济学\industrial-economics-wxapp'

with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\questions_data.json', 'r', encoding='utf-8') as f:
    q_data = json.load(f)

# 1. data/questions.js
js_questions = f"module.exports = {json.dumps(q_data, ensure_ascii=False, indent=2)};\n"
with open(os.path.join(base_dir, 'data', 'questions.js'), 'w', encoding='utf-8') as f:
    f.write(js_questions)

# 2. pages/index/index.wxml
index_wxml = """<view class="container">
  <view class="card shadow">
    <view class="header-tag">学籍匹配身份验证</view>
    <view class="title">产业经济学 · 在线随堂考试</view>
    <view class="subtitle">教材：刘志彪《产业经济学》（第3版）前10章</view>

    <view class="form-group">
      <text class="label">学号 (Student ID)</text>
      <input class="input" placeholder="例如：2026010001" bindinput="onInputId" value="{{studentId}}" />
    </view>

    <view class="form-group">
      <text class="label">姓名 (Full Name)</text>
      <input class="input" placeholder="例如：高建刚" bindinput="onInputName" value="{{studentName}}" />
    </view>

    <view class="error-banner" if="{{errorMsg}}">
      <text class="error-text">{{errorMsg}}</text>
    </view>

    <view class="notice-box">
      <text class="notice-title">⚠️ 期中考试须知：</text>
      <text class="notice-item">• 题量及分值：50 道单项选择题（每题2分，满分100分）。</text>
      <text class="notice-item">• 考试时长：75 分钟限时答题，支持中途【退出考试】。</text>
      <text class="notice-item">• 查分限制：提交后最多允许 2 次查分（每次15秒后自动关闭）。</text>
    </view>

    <button class="btn-primary" bindtap="onStartExam">验证身份并开始测试 (50题/75分钟)</button>
  </view>

  <view class="footer-link" bindtap="onNavAdmin">
    <text class="link-text">🔒 教师/管理员控制台入口 (密码: admin126)</text>
  </view>
</view>
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.wxml'), 'w', encoding='utf-8') as f:
    f.write(index_wxml)

# 3. pages/index/index.js
index_js = """const questions = require('../../data/questions.js');

Page({
  data: {
    studentId: '',
    studentName: '',
    errorMsg: ''
  },

  onInputId(e) {
    this.setData({ studentId: e.detail.value.trim() });
  },

  onInputName(e) {
    this.setData({ studentName: e.detail.value.trim() });
  },

  onStartExam() {
    const { studentId, studentName } = this.data;
    if (!studentId || !studentName) {
      this.setData({ errorMsg: '请完整填写学号和姓名！' });
      return;
    }

    // 1. Get Roster
    let roster = wx.getStorageSync('student_roster_v1') || [
      { id: '2026010001', name: '高建刚' },
      { id: '2026010002', name: '李明' },
      { id: '2026010003', name: '王芳' }
    ];

    const matched = roster.find(s => s.id.trim() === studentId && s.name.trim() === studentName);
    if (!matched) {
      this.setData({ errorMsg: '学号与姓名不匹配，或不在允许考试名单中！' });
      return;
    }

    // 2. Check Submission Status
    let submissions = wx.getStorageSync('exam_submissions_v1') || [];
    let record = submissions.find(r => r.id.trim() === studentId);

    if (record) {
      let checkCount = record.scoreCheckedCount || 0;
      if (checkCount >= 2) {
        wx.showModal({
          title: '查分次数上限',
          content: `学号 [${studentId}] ${studentName} 的 2 次查分机会已用尽，无法再次查分！`,
          showCancel: false
        });
        return;
      } else {
        // Increment check count
        checkCount += 1;
        record.scoreCheckedCount = checkCount;
        wx.setStorageSync('exam_submissions_v1', submissions);

        wx.navigateTo({
          url: `/pages/result/result?record=${encodeURIComponent(JSON.stringify(record))}&checkCount=${checkCount}`
        });
        return;
      }
    }

    // 3. First-time Exam
    getApp().globalData.currentStudent = { id: studentId, name: studentName };
    getApp().globalData.userAnswers = {};

    wx.navigateTo({
      url: '/pages/exam/exam'
    });
  },

  onNavAdmin() {
    wx.navigateTo({
      url: '/pages/admin/admin'
    });
  }
})
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.js'), 'w', encoding='utf-8') as f:
    f.write(index_js)

# 4. pages/index/index.wxss
index_wxss = """.header-tag {
  display: inline-block;
  background: rgba(2, 132, 199, 0.15);
  color: #38bdf8;
  border: 1rpx solid rgba(56, 189, 248, 0.3);
  padding: 6rpx 20rpx;
  border-radius: 30rpx;
  font-size: 22rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
}
.title {
  font-size: 36rpx;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 8rpx;
}
.subtitle {
  font-size: 24rpx;
  color: #94a3b8;
  margin-bottom: 30rpx;
}
.form-group {
  margin-bottom: 24rpx;
}
.label {
  display: block;
  font-size: 24rpx;
  font-weight: bold;
  color: #cbd5e1;
  margin-bottom: 10rpx;
}
.input {
  background-color: #020617;
  border: 1rpx solid #1e293b;
  border-radius: 20rpx;
  padding: 20rpx 24rpx;
  color: #ffffff;
  font-size: 28rpx;
}
.error-banner {
  background: rgba(244, 63, 94, 0.15);
  border: 1rpx solid rgba(244, 63, 94, 0.4);
  padding: 16rpx;
  border-radius: 16rpx;
  margin-bottom: 24rpx;
}
.error-text {
  color: #fb7185;
  font-size: 24rpx;
}
.notice-box {
  background: rgba(2, 6, 23, 0.6);
  border: 1rpx solid #1e293b;
  border-radius: 20rpx;
  padding: 20rpx;
  margin-bottom: 30rpx;
}
.notice-title {
  display: block;
  font-size: 24rpx;
  font-weight: bold;
  color: #fbbf24;
  margin-bottom: 10rpx;
}
.notice-item {
  display: block;
  font-size: 22rpx;
  color: #cbd5e1;
  margin-bottom: 6rpx;
}
.footer-link {
  text-align: center;
  margin-top: 20rpx;
}
.link-text {
  font-size: 24rpx;
  color: #818cf8;
  text-decoration: underline;
}
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.wxss'), 'w', encoding='utf-8') as f:
    f.write(index_wxss)

# 5. pages/index/index.json
index_json = {
  "navigationBarTitleText": "身份验证登录"
}
with open(os.path.join(base_dir, 'pages', 'index', 'index.json'), 'w', encoding='utf-8') as f:
    json.dump(index_json, f, ensure_ascii=False, indent=2)

print("Generated index page source successfully!")
