const questions = require('../../data/questions.js');

Page({
  data: {
    studentId: '',
    studentName: '',
    errorMsg: '',
    themeClass: 'theme-dark',
    themeName: '深色模式'
  },

  onLoad() {
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
        checkCount += 1;
        record.scoreCheckedCount = checkCount;
        wx.setStorageSync('exam_submissions_v1', submissions);

        wx.navigateTo({
          url: `/pages/result/result?record=${encodeURIComponent(JSON.stringify(record))}&checkCount=${checkCount}`
        });
        return;
      }
    }

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
